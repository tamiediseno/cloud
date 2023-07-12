from django.contrib import admin
from real_estate.property import Property,Booking, Sale, StandForSale,PropertyImage,Bid
from .models import AccessKey
from real_estate.rental_property import RentalProperty
from real_estate.profile import Profile
from real_estate.transaction import Transaction
from real_estate.seller import Seller
from real_estate.currency import Currency
from real_estate.tenant import Tenant

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_for_sale', 'is_for_rent', 'is_stand_for_sale')
    list_filter = ('is_for_sale', 'is_for_rent', 'is_stand_for_sale')
    search_fields = ('name', 'description')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'start_date', 'end_date', 'total_cost')
    list_filter = ('start_date', 'end_date')
    search_fields = ('user__username', 'property__name')
    actions = ['mark_as_validated']

    def mark_as_validated(self, request, queryset):
        queryset.update(is_payment_validated=True)
        self.message_user(request, f'{queryset.count()} bookings were successfully marked as validated.')

    mark_as_validated.short_description = "Mark selected bookings as validated"

class SaleAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'date_of_sale', 'total_cost')
    list_filter = ('date_of_sale',)
    search_fields = ('user__username', 'property__name')

class StandForSaleAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'date_of_sale', 'total_cost')
    list_filter = ('date_of_sale',)
    search_fields = ('user__username', 'property__name')

admin.site.register(Property, PropertyAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(StandForSale, StandForSaleAdmin)
admin.site.register(PropertyImage)
admin.site.register(Bid)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('property', 'buyer_name', 'buyer_email', 'buyer_phone_number', 'is_buying', 'is_renting')
    list_filter = ('is_buying', 'is_renting')
    search_fields = ('property__name', 'buyer_name')

admin.site.register(Currency)
admin.site.register(AccessKey)

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Seller)
admin.site.register(Tenant)
admin.site.register(RentalProperty)
admin.site.register(Profile)
