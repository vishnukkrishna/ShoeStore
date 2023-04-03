from django import forms
from .models import userAddress
from django.core.validators import RegexValidator


class AddressForm(forms.ModelForm):

    name_validator = RegexValidator(r'^[a-zA-Z ]*$', 'Name must contain only letters and spaces')
    text_validator = RegexValidator(r'^[a-zA-Z0-9 ,-]*$', 'Field must contain only letters, digits, spaces, commas, and hyphens')

    class Meta:

        model = userAddress

        fields = ['full_name','phone_number','house_name', 'landmark', 'city',  'pincode', 'district', 'state', 'country']
    
    def __init__(self, *args, **kwargs):

        super(AddressForm, self).__init__(*args, **kwargs )

        self.fields['house_name'].widget.attrs['placeholder'] = 'Enter House name'

        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form","placeholder":"Full Name"}
        )
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control mb-2 account-form","pattern":"[0-9]{10}","placeholder":"Phone Number"}
        )


        self.fields['landmark'].widget.attrs['placeholder'] = 'Enter Your Landmark'

        self.fields['city'].widget.attrs['placeholder'] = 'Enter Your City'

        self.fields['pincode'].widget.attrs['placeholder'] = 'Enter Your Pincode'

        self.fields['district'].widget.attrs['placeholder'] = 'Enter Your District'

        self.fields['state'].widget.attrs['placeholder'] = 'Enter Your State'

        self.fields['country'].widget.attrs['placeholder'] = 'Enter Your Country'
        

        for field in self.fields:

            self.fields[field].widget.attrs['class'] = ' form-control form-control-lg form-label ml-5'

    def clean_full_name(self):
        name = self.cleaned_data['full_name']
        self.name_validator(name)
        return name
    
    def clean_house_name(self):
        house_name = self.cleaned_data['house_name']
        self.text_validator(house_name)
        return house_name
    
    def clean_landmark(self):
        landmark = self.cleaned_data['landmark']
        self.text_validator(landmark)
        return landmark
    
    def clean_city(self):
        city = self.cleaned_data['city']
        self.text_validator(city)
        return city
    
    def clean_district(self):
        district = self.cleaned_data['district']
        self.text_validator(district)
        return district
    
    def clean_state(self):
        state = self.cleaned_data['state']
        self.text_validator(state)
        return state
    
    def clean_country(self):
        country = self.cleaned_data['country']
        self.text_validator(country)
        return country
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit():
            raise forms.ValidationError('Phone number must contain only digits')
        return phone_number
        
    def clean_pincode(self):
        pincode = self.cleaned_data['pincode']
        if not pincode.isdigit() or len(pincode) != 6:
            raise forms.ValidationError('Invalid pin code')
        return pincode
