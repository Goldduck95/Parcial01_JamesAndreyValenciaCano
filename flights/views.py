from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Avg, Count
from .models import Flight

# Home Page View
class HomePageView(TemplateView):
    template_name = 'flights/home.html'

# Flight Form
class FlightForm(forms.ModelForm):
    name = forms.CharField(required=True, max_length=255)
    type = forms.ChoiceField(
        choices=Flight.FLIGHT_TYPES,
        required=True
    )
    price = forms.IntegerField(required=True)

    class Meta:
        model = Flight
        fields = ['name', 'type', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('El precio debe ser mayor que cero.')
        return price

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name.strip()) == 0:
            raise ValidationError('El nombre no puede estar vacío.')
        return name.strip()

# Flight Registration View
class FlightCreateView(View):
    template_name = 'flights/create.html'

    def get(self, request):
        form = FlightForm()
        viewData = {}
        viewData["title"] = "Registrar Vuelo"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flight_success')
        else:
            viewData = {}
            viewData["title"] = "Registrar Vuelo"
            viewData["form"] = form
            return render(request, self.template_name, viewData)

# Flight Success View
class FlightSuccessView(TemplateView):
    template_name = 'flights/success.html'

# Flight List View
class FlightListView(View):
    template_name = 'flights/list.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Lista de Vuelos"
        viewData["subtitle"] = "Vuelos registrados en el sistema"
        # Order by price (ascending - menor precio primero)
        viewData["flights"] = Flight.objects.all().order_by('price')
        return render(request, self.template_name, viewData)

# Flight Statistics View
class FlightStatsView(View):
    template_name = 'flights/stats.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Estadísticas de Vuelos"
        viewData["subtitle"] = "Resumen estadístico del sistema"
        
        # Count flights by type
        nacional_count = Flight.objects.filter(type='Nacional').count()
        internacional_count = Flight.objects.filter(type='Internacional').count()
        
        # Average price for national flights
        nacional_avg_price = Flight.objects.filter(type='Nacional').aggregate(
            avg_price=Avg('price')
        )['avg_price']
        
        if nacional_avg_price is None:
            nacional_avg_price = 0
        
        viewData["nacional_count"] = nacional_count
        viewData["internacional_count"] = internacional_count
        viewData["nacional_avg_price"] = round(nacional_avg_price, 2)
        
        return render(request, self.template_name, viewData)