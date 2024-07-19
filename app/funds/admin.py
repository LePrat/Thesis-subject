import json
import logging
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path
from django.utils.html import format_html, strip_tags
from django.utils.text import Truncator
from needle.location_finder import finder
from .forms import JSONImportForm
from .models import Fund


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    """
    A custom Django admin class for managing Fund objects.

    This class extends the default `ModelAdmin` class and provides the following functionalities:
    """
    change_list_template = "admin/funds/change_list.html"
    change_form_template = "admin/funds/change_form.html"
    list_display = ('name', 'funder', 'location', 'nationality', 'truncated_eligibility_text', 'max_fund_amount')

    def get_urls(self):
        """
        Extends the default admin URLs for the Fund model.
        """
        urls = super().get_urls()
        my_urls = [
            path('import-json/', self.import_json),
        ]
        return my_urls + urls

    @staticmethod
    def truncated_eligibility_text(obj):
        plain_text = strip_tags(obj.eligibility_text)
        truncated = Truncator(plain_text).words(10, truncate='...')
        return format_html('<span title="{}">{}</span>', obj.eligibility_text, truncated)

    def import_json(self, request):
        """
        Handles importing fund data from a user-uploaded JSON file.

        This method is triggered when a user visits the `/admin/funds/import-json/` URL. It allows users to:
        - Upload a JSON file containing fund data.
        - Map fields from the JSON file to corresponding fields in the Fund model using a form (`JSONImportForm`).

        The method validates the uploaded file format (JSON), checks for missing fields, and performs additional validation.
        If successful, it creates `Fund` objects from the valid data and displays a success message.

        This functionality streamlines the process of adding multiple funds to the database at once.
        """
        if request.method == "POST":
            # If the request method is POST, process the form submission
            form = JSONImportForm(request.POST, request.FILES)
            if form.is_valid():
                # Extract form data
                json_file = request.FILES['json_file']
                name_field = form.cleaned_data['name_field']
                funder_field = form.cleaned_data['funder_field']
                amount_field = form.cleaned_data['amount_field']
                eligibility_text_field = form.cleaned_data['eligibility_text_field']
                link_field = form.cleaned_data['link_field']

                try:
                    # Load JSON data from the uploaded file
                    data = json.load(json_file)

                    # Ensure the JSON data is a list of objects
                    if not isinstance(data, list):
                        raise ValueError("JSON data must be a list of objects")

                    imported_count = 0
                    for item in data:
                        # Check if all required fields are present in each item
                        if all(field in item for field in
                               [name_field, funder_field, amount_field, eligibility_text_field, link_field]):
                            # Create a new Fund object with the data from the JSON
                            Fund.objects.create(
                                name=item.get(name_field),
                                funder=item.get(funder_field),
                                max_fund_amount=item.get(amount_field),
                                eligibility_text=item.get(eligibility_text_field),
                                link=item.get(link_field)
                            )
                            imported_count += 1
                        else:
                            # Raise an error if any required field is missing
                            raise ValueError("One or more fields are missing in the JSON data")

                    # Display success message and redirect
                    self.message_user(request, f"Successfully imported {imported_count} funds")
                    return HttpResponseRedirect("..")
                except json.JSONDecodeError:
                    # Handle invalid JSON format
                    self.message_user(request, "Invalid JSON file", level='ERROR')
                except Exception as e:
                    # Log any other exceptions and display error message
                    logging.exception("Error importing JSON")
                    self.message_user(request, f"Error importing JSON: {str(e)}", level='ERROR')
        else:
            # If the request method is GET, display the empty form
            form = JSONImportForm()

        # Render the import form template
        return render(request, "admin/json_import.html", context={'form': form})

    def response_change(self, request, obj):
        """
            Handle the response after changes to the object, including custom actions.

            This method overrides the default ModelAdmin response_change to add custom
            functionality for the 'Execute location & nationality finder' button.
            If the button is clicked, the finder script runs on the object and displays a success message.
        """
        if "_execute-finder" in request.POST:
            result = finder(obj.eligibility_text)
            if ";" in result:
                location, nationality = result.split(";")
                message = f"Script executed. Result: [Location]: {location}, [Nationality]: {nationality}"
                self.message_user(request, message)
                obj.location = location
                obj.nationality = nationality
                obj.save()
                return HttpResponseRedirect(".")
            else:
                self.message_user(request, f"Script executed. Result: {result}", level='ERROR')
        return super().response_change(request, obj)
