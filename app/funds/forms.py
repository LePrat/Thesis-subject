from django import forms


class JSONImportForm(forms.Form):
    json_file = forms.FileField(label='Select a JSON file')

    # Add fields to map JSON keys to model fields
    name_field = forms.CharField(label='JSON key for Fund Name', initial='name')
    funder_field = forms.CharField(label='JSON key for Funder', initial='funder')
    amount_field = forms.CharField(label='JSON key for Fund Amount', initial='max_fund_amount')
    eligibility_text_field = forms.CharField(label='JSON key for Eligibility Text', initial='eligibility_note')
    link_field = forms.CharField(label='JSON key for Link', initial='funder_url')

    def clean_json_file(self):
        file = self.cleaned_data['json_file']
        if not file.name.endswith('.json'):
            raise forms.ValidationError('File is not JSON type')
        return file
