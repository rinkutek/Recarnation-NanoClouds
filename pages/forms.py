# forms.py
from django import forms
from cars.models import Car
from ckeditor.widgets import CKEditorWidget

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'car_title', 'state', 'city', 'color', 'model', 'year', 'condition', 'price',
            'description', 'car_photo', 'car_photo_1', 'car_photo_2', 'car_photo_3', 'car_photo_4',
            'features', 'body_style', 'engine', 'transmission', 'interior', 'miles', 'doors',
            'passengers', 'vin_no', 'milage', 'fuel_type', 'no_of_owners'
        ]
    
    # Customize widgets for better UI/UX
    car_title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.ChoiceField(choices=Car.state_choice, widget=forms.Select(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    color = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    model = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    year = forms.ChoiceField(choices=Car.year_choice, widget=forms.Select(attrs={'class': 'form-control'}))
    condition = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.NumberInput(attrs={'class': 'form-control'})
    description = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control'}))
    car_photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    car_photo_1 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    car_photo_2 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    car_photo_3 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    car_photo_4 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    features = forms.MultipleChoiceField(choices=Car.features_choices, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}))
    body_style = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    engine = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    transmission = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    interior = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    miles = forms.NumberInput(attrs={'class': 'form-control'})
    doors = forms.ChoiceField(choices=Car.door_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    passengers = forms.NumberInput(attrs={'class': 'form-control'})
    vin_no = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    milage = forms.NumberInput(attrs={'class': 'form-control'})
    fuel_type = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    no_of_owners = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #is_featured = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

