from django import forms
from .models import ReviewRating



class ReviewForm(forms.ModelForm):

    image = forms.FileField(required=False)

    class Meta:

        model = ReviewRating

        fields = ['subject', 'review', 'rating', 'image']
