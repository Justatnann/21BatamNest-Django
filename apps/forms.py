from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Button
from crispy_bootstrap5.bootstrap5 import Field

from view.settings import DATE_INPUT_FORMATS

from .models import Event, Payment_Method, Product, Salesman


class LoginForm(forms.Form):
    Username = forms.CharField(label="Username", max_length=45, required=True)
    Password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper: FormHelper = FormHelper(self)
        self.helper.layout = Layout(
            Field("Username", wrapper_class="form-group mb-4", ) ,
            Field("Password", wrapper_class="form-group mb-4", ) ,
            Div(
                Submit("submit", "Login",  css_class="btn-primary btn-user btn-block"),
                ),
        ) 


class AddProductForm(forms.Form):
    product_name = forms.CharField(label="Product Name", max_length=100, required=True)
    description = forms.CharField(label="Description", max_length=300, required=False)
    price = forms.IntegerField(label="Price", required=True)
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper: FormHelper = FormHelper(self)
        self.helper.layout = Layout(
            Field("product_name", wrapper_class="form-group mb-4", ) ,
            Field("description", wrapper_class="form-group mb-4", ) ,
            Field("price", wrapper_class="form-group mb-4", ) ,
            
            Div(
                Submit("submit", "Submit",  css_class="btn-primary btn-user"),
                Button("cancel", "Cancel", onclick="location.href = '/product'", css_class="btn-danger"),  
                ),
            
                
        )

class AddEventForm(forms.Form):
    event_name = forms.CharField(label="Event Name", max_length=100, required=True)
    description = forms.CharField(label="Description", max_length=300, required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper: FormHelper = FormHelper(self)
        self.helper.layout = Layout(
            Field("event_name", wrapper_class="form-group mb-4", ) ,
            Field("description", wrapper_class="form-group mb-4", ) ,
            Div(
                Submit("submit", "Submit",  css_class="btn-primary btn-user"),
                Button("cancel", "Cancel", onclick="location.href = '/event'", css_class="btn-danger"),  
                ),
        )

class AddPaymentMethodForm(forms.Form):
    payment_method = forms.CharField(label="Payment Method", max_length=100, required=True)
    account_number = forms.CharField(label="Account Number", max_length=100, required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper: FormHelper = FormHelper(self)
        self.helper.layout = Layout(
            Field("payment_method", wrapper_class="form-group mb-4", ) ,
            Field("account_number", wrapper_class="form-group mb-4", ) ,
            Div(
                Submit("submit", "Submit",  css_class="btn-primary btn-user"),
                Button("cancel", "Cancel", onclick="location.href = '/payment'", css_class="btn-danger"),  
                ),
        )

class AddInvoiceForm(forms.Form):
    quantity = forms.IntegerField(label="Quantity", required=True)
    total_price = forms.IntegerField(label="Total Price", required=True)
    discount = forms.IntegerField(label="Discount", required=True)
    customer = forms.CharField(label="Customer", max_length=100, required=True)
    sales = forms.CharField(label="Sales", max_length=100, required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        products = list(Product.objects.all().values_list("id", "product_name"))
        products.insert(0, ('', '-'))
        self.fields["product"] = forms.CharField(widget=forms.Select(choices=products, attrs={'class': 'select form-control'}))

        events = list(Event.objects.all().values_list("id", "event_name"))
        events.insert(0, ('', '-'))
        self.fields['event'] = forms.CharField(widget=forms.Select(choices=events, attrs={'class': 'select form-control'}))

        payment_methods = list(Payment_Method.objects.all().values_list("id", "payment_method"))
        payment_methods.insert(0, ('', '-'))
        self.fields['payment_method'] = forms.CharField(widget=forms.Select(choices=payment_methods, attrs={'class': 'select form-control'}))

        sales = list(Salesman.objects.all().values_list("id", "name"))
        sales.insert(0, ('', '-'))
        self.fields['sales'] = forms.CharField(widget=forms.Select(choices=sales, attrs={'class': 'select form-control'}))

        self.helper: FormHelper = FormHelper(self)
        self.helper.layout = Layout(
            Field("product", wrapper_class="form-group mb-4", ) ,
            Field("event", wrapper_class="form-group mb-4", ) ,
            Field("quantity", wrapper_class="form-group mb-4", ) ,
            Field("discount", wrapper_class="form-group mb-4", ) ,
            Field("total_price", wrapper_class="form-group mb-4", ) ,   
            Field("payment_method", wrapper_class="form-group mb-4", ) ,
            Field("customer", wrapper_class="form-group mb-4", ) ,
            Field("sales", wrapper_class="form-group mb-4", ) ,
            Div(
                Submit("submit", "Submit",  css_class="btn-primary btn-user"),
                Button("cancel", "Cancel", onclick="location.href = '/invoice'", css_class="btn-danger"),  
                ),
        )
        self.fields['total_price'].widget.attrs['readonly'] = True

class PredictionForm(forms.Form):
    
    date = forms.DateField(
        label="Date",
        input_formats=['%d/%m/%Y'],  # Define the acceptable input format
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'date-input'
        }))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        events = list(Event.objects.all().values_list("id", "event_name"))
        events.insert(0, ('', '-'))
        self.fields['event'] = forms.CharField(widget=forms.Select(choices=events, attrs={'class': 'select form-control'}))

        self.helper: FormHelper = FormHelper(self)
        self.helper.layout = Layout(
            Field("event", wrapper_class="form-group mb-4", ) ,
            Field("date", wrapper_class="form-group mb-4", ) ,
          
        )

class SalesmanForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, required=True)
    age = forms.IntegerField(label="Age", required=True)
    number = forms.CharField(label="Number", max_length=100, required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper: FormHelper = FormHelper(self)
        self.helper.layout = Layout(
            Field("name", wrapper_class="form-group mb-4", ) ,
            Field("age", wrapper_class="form-group mb-4", ) ,
            Field("number", wrapper_class="form-group mb-4", ) ,
            Div(
                Submit("submit", "Submit",  css_class="btn-primary btn-user"),
                Button("cancel", "Cancel", onclick="location.href = '/salesman'", css_class="btn-danger"),  
            ),  
        )