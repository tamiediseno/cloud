from django.utils import timezone
from django.conf import settings
from django.db import models
from django.utils.text import camel_case_to_spaces
from real_estate.currency import Currency
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


from django.utils import timezone
from django.core.exceptions import ValidationError
from real_estate.utils import send_sms  # Import the send_sms function from utils.py


class Property(models.Model):
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True)
    image = models.ImageField(upload_to='media/', blank=True)
    is_for_sale = models.BooleanField(default=False, blank=True)
    is_for_rent = models.BooleanField(default=False, blank=True)
    is_stand_for_sale = models.BooleanField(default=False, blank=True)
    room_size = models.CharField(max_length=100, blank=True)
    number_of_rooms = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    bills_included_water_electricity = models.BooleanField(default=False, blank=True)

    # Add fields for solar generator
    solar_generator_rental_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    solar_generator_purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Add fields for bidding
    bidding_start_time = models.DateTimeField(blank=True, null=True)
    bidding_end_time = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.is_for_sale and (self.is_for_rent or self.is_stand_for_sale):
            raise ValueError("A property cannot be for sale and for rent or stand for sale at the same time")
        if self.is_for_rent and (self.is_for_sale or self.is_stand_for_sale):
            raise ValueError("A property cannot be for rent and for sale or stand for sale at the same time")
        if self.is_stand_for_sale and (self.is_for_sale or self.is_for_rent):
            raise ValueError("A property cannot be stand for sale and for sale or for rent at the same time")
        super().save(*args, **kwargs)

    def get_time_remaining(self):
        if self.bidding_end_time:
            time_remaining = self.bidding_end_time - timezone.now()
            return time_remaining.total_seconds()
        return None

    def get_highest_bid(self):
        highest_bid = self.bids.order_by('-amount').first()
        return highest_bid

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = 'Property'


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    is_main = models.BooleanField(default=False)


class Bid(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        if self.property_id and self.property.bidding_end_time and timezone.now() > self.property.bidding_end_time:
            raise ValidationError('The bidding period for this property has ended.')

    def save(self, *args, **kwargs):
    # Check if this is a new bid
     if not self.pk:
        # Check if the bidding period has ended
        if self.property.bidding_end_time and timezone.now() > self.property.bidding_end_time:
            # Check if this bid is higher than the current highest bid
            highest_bid = self.property.get_highest_bid()
            if not highest_bid or self.amount > highest_bid.amount:
                # Send an SMS to the user
                send_sms(
                    to=self.user.phone_number,
                    body=f'Congratulations! Your bid of {self.amount} on property {self.property} has been accepted.'
                )
     super().save(*args, **kwargs)



class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    # Add fields for solar generator
    rent_solar_generator = models.BooleanField(default=False)
    buy_solar_generator = models.BooleanField(default=False)

    is_cancelled = models.BooleanField(default=False)
    proof_of_payment = models.FileField(upload_to='media/', null=True, blank=True)
    is_payment_validated = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if not self.is_payment_validated:
            raise ValidationError('The payment for this booking has not been validated.')
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError('The start date must be before the end date.')
            overlapping_bookings = Booking.objects.filter(
                property=self.property,
                start_date__lt=self.end_date,
                end_date__gt=self.start_date
            ).exclude(pk=self.pk)
            if overlapping_bookings.exists():
                raise ValidationError('This property is not available for the selected dates.')

        # Validate solar generator options
        if self.rent_solar_generator and not self.property.solar_generator_rental_fee:
            raise ValidationError('This property does not have a solar generator available for rent.')
        if self.buy_solar_generator and not self.property.solar_generator_purchase_price:
            raise ValidationError('This property does not have a solar generator available for purchase.')

    def save(self, *args, **kwargs):
        # Check if the payment has been validated
        if self.is_payment_validated and not Booking.objects.filter(pk=self.pk).exists():
            # Send an SMS to the user
            send_sms(
                to=self.user.phone_number,
                body=f'Your payment for booking {self.property} has been accepted. Thank you!'
            )

        self.full_clean()

        # Add cost of solar generator rental or purchase to total cost
        if self.rent_solar_generator:
            self.total_cost += self.property.solar_generator_rental_fee
        elif self.buy_solar_generator:
            self.total_cost += self.property.solar_generator_purchase_price

        super().save(*args, **kwargs)

class Sale(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    date_of_sale = models.DateField(default=timezone.now)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    proof_of_payment = models.FileField(upload_to='media/', null=True, blank=True)
    is_payment_validated = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if not self.is_payment_validated:
            raise ValidationError('The payment for this sale has not been validated.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def generate_receipt(self):
        receipt = f'Receipt for sale by {self.user} for {self.property} on {self.date_of_sale} for {self.total_cost}'
        return receipt

    def __str__(self):
        return f'{self.user} sale for {self.property} on {self.date_of_sale} for {self.total_cost}'

class StandForSale(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    date_of_sale = models.DateField(default=timezone.now)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    proof_of_payment = models.FileField(upload_to='media/', null=True, blank=True)
    is_payment_validated = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if not self.is_payment_validated:
            raise ValidationError('The payment for this stand for sale has not been validated.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def generate_receipt(self):
        receipt = f'Receipt for stand for sale by {self.user} for {self.property} on {self.date_of_sale} for {self.total_cost}'
        return receipt

    def __str__(self):
        return f'{self.user} stand for sale for {self.property} on {self.date_of_sale} for {self.total_cost}'
