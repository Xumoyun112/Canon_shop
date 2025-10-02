from django import forms
from .models import Sale, Speska, Product

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["product", "quantity", "description"]
        widgets = {
            "product": forms.Select(attrs={"class": "product-select form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'rows': 4,
                'placeholder': 'Mahsulot haqida izoh yozing...'
            }),
        }

    def clean_quantity(self):
        qty = self.cleaned_data["quantity"]
        product = self.cleaned_data.get("product")
        if product and qty > product.stock:
            raise forms.ValidationError("Skladda yetarli mahsulot yo‘q!")
        return qty

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "unit", "price", "stock", "supplier"]