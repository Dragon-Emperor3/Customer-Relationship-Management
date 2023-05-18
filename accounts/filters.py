import django_filters
from django_filters import DateFilter, CharFilter
from django import forms

from .models import *

class FilterOrder(django_filters.FilterSet):
    
    start_date= DateFilter(field_name='date_created', lookup_expr= 'gte', label='Start Date',
                           widget= forms.TextInput(attrs={'class': 'form-control-50 ', 'placeholder':' Greater than or Equal to'}))
    end_date= DateFilter(field_name='date_created', lookup_expr= 'lte', label='End Date',
                         widget=forms.TextInput(attrs={'class': 'form-control-50', 'placeholder':' Lesser than or Equal to'}))
    note= CharFilter(field_name='note', lookup_expr='icontains',label='Note',
                     widget= forms.TextInput(attrs={'class': 'form-control-50'}),)
    
    
    
    class Meta():
        model= Order
        fields= '__all__'
        exclude= ['customer', 'date_created']
        widgets={
            'product': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }