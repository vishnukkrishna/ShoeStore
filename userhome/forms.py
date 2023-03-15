from django import forms
from .models import userAddress


class AddressForm(forms.ModelForm):

    class Meta:

        model = userAddress

        fields = ['house_name', 'landmark', 'city',  'pincode', 'district', 'state', 'country']
    
    def __init__(self, *args, **kwargs):

        super(AddressForm, self).__init__(*args, **kwargs )

        self.fields['house_name'].widget.attrs['placeholder'] = 'Enter House name'

        self.fields['landmark'].widget.attrs['placeholder'] = 'Enter Your Landmark'

        self.fields['city'].widget.attrs['placeholder'] = 'Enter Your City'

        self.fields['pincode'].widget.attrs['placeholder'] = 'Enter Your Pincode'

        self.fields['district'].widget.attrs['placeholder'] = 'Enter Your District'

        self.fields['state'].widget.attrs['placeholder'] = 'Enter Your State'

        self.fields['country'].widget.attrs['placeholder'] = 'Enter Your Country'
        

        for field in self.fields:

            self.fields[field].widget.attrs['class'] = ' form-control form-control-lg form-label ml-5'