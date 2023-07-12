import random
import string
from rest_framework import generics, permissions
from django.http import JsonResponse
from django.http import HttpResponseNotAllowed
from django.http import HttpResponse
from twilio.rest import Client
from django.http import JsonResponse
from .models import AccessKey
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from real_estate.property import Property, PropertyImage
from real_estate.property import Booking, Sale, StandForSale
from real_estate.transaction import Transaction
from real_estate.seller import Seller
from real_estate.currency import Currency
from real_estate.tenant import Tenant
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.views.generic import DetailView
from django.forms import formset_factory
from .forms import PropertyImageForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .forms import BidForm
from .forms import BookingForm, SaleForm, StandForSaleForm
from .forms import AccessKeyLoginForm, AccessKeyCreationForm
from .serializers import PropertySerializer,SaleSerializer,TransactionSerializer,SellerSerializer,CurrencySerializer,TenantSerializer

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import PropertyForm
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView






class MainPageView(TemplateView):
    template_name = 'main/property_create.html'


class PropertyListView(ListView):
    model = Property
    template_name = 'main/property_list.html'





class PropertyDetailView(DetailView):
    model = Property
    template_name = 'main/property_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        property = self.get_object()
        if property.is_for_rent:
            context['form'] = BookingForm()
        elif property.is_stand_for_sale:
            context['form'] = StandForSaleForm()
        elif property.is_for_sale:
            context['form'] = SaleForm()
        return context

    def post(self, request, *args, **kwargs):
        property = self.get_object()
        if property.is_for_rent:
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.property = property
                booking.user = request.user
                booking.save()
                url = reverse('booking_detail', args=[booking.pk])
                return redirect(url)
        elif property.is_stand_for_sale:
            form = StandForSaleForm(request.POST)
            if form.is_valid():
                stand_for_sale = form.save(commit=False)
                stand_for_sale.property = property
                stand_for_sale.user = request.user
                stand_for_sale.save()
                url = reverse('standforsale_detail', args=[stand_for_sale.pk])
                return redirect(url)
        elif property.is_for_sale:
            form = SaleForm(request.POST)
            if form.is_valid():
                sale = form.save(commit=False)
                sale.property = property
                sale.user = request.user
                sale.save()
                url = reverse('sale_detail', args=[sale.pk])
                return redirect(url)
        return super().get(request, *args, **kwargs)






class PropertyCreateView(CreateView):
    model = Property
    template_name = 'form_create/property_create_data.html'
    fields = [ 'description', 'price', 'currency', 'is_for_sale', 'is_for_rent', 'is_stand_for_sale', 'room_size', 'number_of_rooms', 'location', 'city', 'bills_included_water_electricity','solar_generator_rental_fee','solar_generator_purchase_price','bidding_start_time','bidding_end_time',]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # create a formset for PropertyImage forms with 3 forms
        PropertyImageFormSet = formset_factory(PropertyImageForm, extra=3)
        context['image_formset'] = PropertyImageFormSet()

        return context

    def form_valid(self, form):
        # set a default value for the name field
        form.instance.name = get_user_model().objects.first()

        # create a formset for PropertyImage forms
        PropertyImageFormSet = formset_factory(PropertyImageForm)
        image_formset = PropertyImageFormSet(self.request.POST, self.request.FILES)

        if image_formset.is_valid():
            # save the property object
            property = form.save()

            # save the property image objects
            for image_form in image_formset:
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.property = property
                    image.save()

            # redirect to success page
            return redirect('property_list')
        else:
            return self.form_invalid(form)



class PropertyUpdateView(UpdateView):
    model = Property
    template_name = 'property_update.html'
    fields = [ 'description', 'price', 'currency', 'image', 'is_for_sale', 'is_for_rent', 'is_stand_for_sale', 'room_size', 'number_of_rooms', 'location', 'city', 'bills_included_water_electricity']

class PropertyDeleteView(DeleteView):
    model = Property
    template_name = 'property_delete.html'
    success_url = reverse_lazy('property_list')
class BookingListView(ListView):
    model = Booking
    template_name = 'booking_list.html'

class BookingDetailView(DetailView):
    model = Booking
    template_name = 'booking_detail.html'

class BookingCreateView(CreateView):
    model = Booking
    template_name = 'booking_create.html'
    fields = ['user', 'property', 'start_date', 'end_date', 'total_cost', 'is_cancelled', 'proof_of_payment', 'is_payment_validated']

class BookingUpdateView(UpdateView):
    model = Booking
    template_name = 'booking_update.html'
    fields = ['user', 'property', 'start_date', 'end_date', 'total_cost', 'is_cancelled', 'proof_of_payment', 'is_payment_validated']

class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'booking_delete.html'
    success_url = reverse_lazy('booking_list')

class SaleListView(ListView):
    model = Sale
    template_name = 'sale_list.html'

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sale_detail.html'

class SaleCreateView(CreateView):
    model = Sale
    template_name = 'sale_create.html'
    fields = ['user', 'property', 'date_of_sale', 'total_cost', 'proof_of_payment', 'is_payment_validated']

class SaleUpdateView(UpdateView):
    model = Sale
    template_name = 'sale_update.html'
    fields = ['user', 'property', 'date_of_sale', 'total_cost', 'proof_of_payment', 'is_payment_validated']

class SaleDeleteView(DeleteView):
    model = Sale
    template_name = 'sale_delete.html'
    success_url = reverse_lazy('sale_list')

class StandForSaleListView(ListView):
    model = StandForSale
    template_name = 'standforsale_list.html'

class StandForSaleDetailView(DetailView):
    model = StandForSale
    template_name = 'standforsale_detail.html'

class StandForSaleCreateView(CreateView):
    model = StandForSale
    template_name = 'standforsale_create.html'
    fields = ['user', 'property', 'date_of_sale', 'total_cost', 'proof_of_payment', 'is_payment_validated']

class StandForSaleUpdateView(UpdateView):
    model = StandForSale
    template_name = 'standforsale_update.html'
    fields = ['user', 'property', 'date_of_sale', 'total_cost', 'proof_of_payment', 'is_payment_validated']

class StandForSaleDeleteView(DeleteView):
    model = StandForSale
    template_name = 'standforsale_delete.html'
    success_url = reverse_lazy('standforsale_list')

class MyLoginView(LoginView):
    template_name = 'auth/my_login.html'
    form_class = AccessKeyLoginForm

class MyRegistrationView(FormView):
    template_name = 'auth/my_registration.html'
    form_class = AccessKeyCreationForm
    success_url = '/registration-success/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)





















class PropertiesCreateView(generics.CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

class PropertyListViews(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    http_method_names = ['get']


class SaleCreateView(generics.CreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

class SaleListView(generics.ListAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    http_method_names = ['get']

class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    http_method_names = ['get']    


class SellerCreateView(generics.CreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

class SellerListView(generics.ListAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    http_method_names = ['get']

class CurrencyCreateView(generics.CreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

class CurrencyListView(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    http_method_names = ['get']  

class CurrencyCreateView(generics.CreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

class TenantListView(generics.ListAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    http_method_names = ['get']   

class TenantCreateView(generics.CreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']





def generate_access_key(request):
    if request.method == 'POST':
        # Get the user's information from the request
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        # Print the values to the console
        print(f'Username: {username}')
        print(f'Email: {email}')
        print(f'Phone Number: {phone_number}')

        # Generate a random 6-digit access key
        access_key = ''.join(random.choices(string.digits, k=6))

        # Create an AccessKey object and save it to the database
        access_key_obj = AccessKey(username=username, email=email, phone_number=phone_number, access_key=access_key)
        access_key_obj.save()

        # Return the generated access key in the response
        data = {'access_key': access_key}
        return JsonResponse(data)
    else:
        # Handle GET requests
        return HttpResponse('GET request received')



def verify_access_key(request):
    # Get the user's information from the request
    username = request.POST.get('username')
    email = request.POST.get('email')
    phone_number = request.POST.get('phone_number')
    access_key = request.POST.get('access_key')

    # Check if an AccessKey object exists with the provided information
    try:
        access_key_obj = AccessKey.objects.get(username=username,phone_number=phone_number, email=email, access_key=access_key)
        is_verified = True
    except AccessKey.DoesNotExist:
        is_verified = False

    # Return the verification result in the response
    data = {'is_verified': is_verified}
    return JsonResponse(data)
    




from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages

class MakeBidView(LoginRequiredMixin, FormView):
    template_name = 'form_create/make_bid.html'
    form_class = BidForm

    def form_valid(self, form):
        property_id = self.kwargs['property_id']
        print(Property.objects.filter(pk=property_id).exists())
        property = get_object_or_404(Property, pk=property_id)
        print(form.cleaned_data)
        bid = form.save(commit=False)
        bid.user = self.request.user
        bid.property = property
        bid.save()
        print(bid.pk)
        messages.success(self.request, 'Your bid has been placed.')
        return super().form_valid(form)

    def get_success_url(self):
        property_id = self.kwargs['property_id']
        return reverse('property_detail', args=[property_id])







    
