from django.contrib import admin
from .models import Fund
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
import json
import logging
from .forms import JSONImportForm


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    change_list_template = "admin/funds_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-json/', self.import_json),
        ]
        return my_urls + urls

    def import_json(self, request):
        if request.method == "POST":
            form = JSONImportForm(request.POST, request.FILES)
            if form.is_valid():
                json_file = request.FILES['json_file']
                name_field = form.cleaned_data['name_field']
                funder_field = form.cleaned_data['funder_field']
                amount_field = form.cleaned_data['amount_field']
                eligibility_text_field = form.cleaned_data['eligibility_text_field']
                link_field = form.cleaned_data['link_field']

                try:
                    data = json.load(json_file)
                    if not isinstance(data, list):
                        raise ValueError("JSON data must be a list of objects")

                    imported_count = 0
                    for item in data:
                        # Add more field validation if necessary
                        if all(field in item for field in
                               [name_field, funder_field, amount_field, eligibility_text_field, link_field]):
                            Fund.objects.create(
                                name=item.get(name_field),
                                funder=item.get(funder_field),
                                max_fund_amount=item.get(amount_field),
                                eligibility_text=item.get(eligibility_text_field),
                                link=item.get(link_field)
                            )
                            imported_count += 1
                        else:
                            raise ValueError("One or more fields are missing in the JSON data")

                    self.message_user(request, f"Successfully imported {imported_count} funds")
                    return HttpResponseRedirect("..")
                except json.JSONDecodeError:
                    self.message_user(request, "Invalid JSON file", level='ERROR')
                except Exception as e:
                    logging.exception("Error importing JSON")
                    self.message_user(request, f"Error importing JSON: {str(e)}", level='ERROR')
        else:
            form = JSONImportForm()

        return render(request, "admin/json_import.html", context={'form': form})
