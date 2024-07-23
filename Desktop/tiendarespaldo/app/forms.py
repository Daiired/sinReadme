from django import forms
from .models import Contacto, Producto,Alimento, CategoriaAlimento, Dieta,LibreDeAlimento, AlimentoDieta, AlimentoLibreDe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import MaxSizeFileValidator
from django.forms import ValidationError

class ContactoForm (forms.ModelForm):

    #nombre = forms.CharField(widget = forms.TextInput(attrs={"class":"form-control"}))

    class Meta: 
        model = Contacto
        fields =["nombre", "correo", "tipo_consulta", "mensaje","avisos"]
        #fields = '__all__'

class AlimentoForm(forms.ModelForm):
    class Meta: 
        model = Alimento
        fields ='__all__'

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = CategoriaAlimento
        fields = '__all__'
      
class DietaForm(forms.ModelForm):
    class Meta:
        model = Dieta
        fields = '__all__'

class LibreForm(forms.ModelForm):
    class Meta:
        model = LibreDeAlimento
        fields = '__all__'

class AlimentoDietaForm(forms.ModelForm):
    class Meta:
        model = AlimentoDieta
        fields = '__all__'

class AlimentoLibreDeForm(forms.ModelForm):
    class Meta:
        model = AlimentoLibreDe
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields =['username', "first_name", "last_name", "email", "password1", "password2"]

class ProductoForm(forms.ModelForm):

    nombre = forms.CharField(min_length=3, max_length=50)
    precio = forms.IntegerField(min_value=1, max_value=1500000)
    imagen = forms.ImageField(required=False, validators=[MaxSizeFileValidator(max_file_size=2)])


    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        existe = Producto.objects.filter (nombre__iexact=nombre). exists()

        if existe:
            raise ValidationError("Este nombre ya existe")
        return nombre

    class Meta:
        model= Producto
        fields= '__all__'

        widgets ={
            "fecha_fabricacion": forms.SelectDateWidget()
        }


