from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from real_estate.property import Property,Booking, Sale, StandForSale,PropertyImage
from django.forms import DateTimeInput
from real_estate.property import Bid

from real_estate.property import Property
from .models import AccessKey

class AccessKeyLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AccessKey
        fields = ('username', 'password')

class AccessKeyCreationForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=30)

    class Meta:
        model = AccessKey
        fields = ('username', 'email', 'phone_number')





class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'description',
            'price',
            'image',
            'is_for_sale',
            'is_for_rent',
            'is_stand_for_sale',
            'room_size',
            'number_of_rooms',
            'location',
            'city',
            'bills_included_water_electricity',

            # Add fields for solar generator
            'solar_generator_rental_fee',
            'solar_generator_purchase_price',

            # Add fields for bidding
            'bidding_start_time',
            'bidding_end_time'
        ]
        error_messages = {
            field: {'required': ''} for field in fields
        }










class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'total_cost', 'is_cancelled', 'proof_of_payment']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['date_of_sale', 'total_cost', 'proof_of_payment', ]

class StandForSaleForm(forms.ModelForm):
    class Meta:
        model = StandForSale
        fields = ['date_of_sale', 'total_cost', 'proof_of_payment', ]
        
        


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'is_main']
        


# forms.py



class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
