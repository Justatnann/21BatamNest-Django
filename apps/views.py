from django.shortcuts import redirect, render
import pathlib
from django.http import HttpResponse, HttpRequest
from .models import Product, Event, Payment_Method, Invoice
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import json
import pandas as pd
import joblib
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Sum, Count
from django.forms.models import model_to_dict
import numpy as np
from .forms import LoginForm, AddProductForm, AddEventForm, AddPaymentMethodForm, AddInvoiceForm, PredictionForm
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def index(request: HttpRequest)-> HttpRequest:
    auth = auth_check(request)
    if auth is not None:

       
        form = PredictionForm()

        
        return render(request, "apps/guest.html", { 'form': form})
    return redirect('dashboard')

def login(request: HttpResponse ) -> HttpResponse:
    if(request.method == "POST"):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(request=request, username=request.POST['Username'], password=request.POST['Password'])
            
            if user is not None:
                auth_login(request, user)
                print(request.user.is_authenticated)
                return redirect("dashboard", )

            form.add_error(None, "Invalid username or password")
        else:
           return render(request, "apps/login.html", {"form": form}) 
    else:
        form = LoginForm()
    return render(request, "apps/login.html", {"form": form})


def log_out(request: HttpRequest) -> HttpResponse:
    auth = auth_check(request)
    if auth is not None:
        return auth
    auth_logout(request)
    return redirect("login")

def dashboard(request: HttpRequest) -> HttpResponse:

    auth = auth_check(request)
    print(request.user)
    if auth is not None:
        return auth
    sales_per_product = Invoice.objects.values('product__product_name').annotate(total_sales=Sum('total_price'))
    sales_per_event = Invoice.objects.values('event__event_name').annotate(total_sales=Sum('total_price'))
    sales_per_customer = Invoice.objects.values('customer').annotate(total_sales=Sum('total_price'))
    payment_method_usage = Invoice.objects.values('payment_method').annotate(count=Count('id'))
    payment_method = Payment_Method.objects.all()
    sales_per_date = Invoice.objects.values('date').annotate(total_sales=Sum('total_price'))

    # Prepare data for JSON
    sales_per_product_data = {
        'labels': [item['product__product_name'] for item in sales_per_product],
        'data': [item['total_sales'] for item in sales_per_product]
    }
    sales_per_event_data = {
        'labels': [item['event__event_name'] for item in sales_per_event],
        'data': [item['total_sales'] for item in sales_per_event]
    }
    sales_per_customer_data = {
        'labels': [item['customer'] for item in sales_per_customer],
        'data': [item['total_sales'] for item in sales_per_customer]
    }
    payment_method_usage_data = {
        'labels': [item['payment_method'] for item in payment_method_usage],
        'data': [item['count'] for item in payment_method_usage]
    }
    sales_per_date_data = {
        'labels': [item['date'].strftime('%Y-%m-%d') for item in sales_per_date],
        'data': [item['total_sales'] for item in sales_per_date]
    }

    context = {
        'sales_per_product': json.dumps(sales_per_product_data),
        'sales_per_event': json.dumps(sales_per_event_data),
        'sales_per_customer': json.dumps(sales_per_customer_data),
        'payment_method_usage': json.dumps(payment_method_usage_data),
        'sales_per_date': json.dumps(sales_per_date_data),
    }

    pm = []
    for x in payment_method:
        pm.append(x.payment_method)
    return render(request, "apps/index.html", {'context': context, 'payment': payment_method})


def product(request : HttpRequest) -> HttpResponse:
    product = Product.objects.all()
    auth = auth_check(request)
    if auth is not None:
        return auth
    return render(request, "apps/product.html", {'products': product})


def create_product(request  : HttpRequest) -> HttpResponse:
    
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    if request.method == "POST":
        form = AddProductForm(request.POST)
        if form.is_valid():
            product = Product(
                product_name=request.POST['product_name'],
                description=request.POST['description'], 
                price=request.POST['price'], 
)
            product.save()
            return redirect("product")
    
    else:
        form = AddProductForm()
    return render(request, "apps/add_product.html", {"form": form})


def update_product(request: HttpRequest, id) -> HttpResponse:
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    product = Product.objects.get(id=id)
    if request.method == "POST":
        form = AddProductForm(request.POST)
        if form.is_valid():
            product.product_name = request.POST['product_name']
            product.description = request.POST['description']
            product.price = request.POST['price']
            
            product.save()
            return redirect("product")
    else:
        form = AddProductForm(initial={
            'product_name': product.product_name,
            'description': product.description,
            'price': product.price,

        })
    return render(request, "apps/update_product.html", {"form": form})   

def delete_product(request: HttpRequest, id) -> HttpResponse:
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    product = Product.objects.get(id=id)
    product.delete()
    return redirect("apps/product")

def event(request: HttpRequest) -> HttpResponse:
    events = Event.objects.all()
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    return render(request, "apps/event.html", {'event': events,})

def create_event(request: HttpRequest) -> HttpResponse:
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    if request.method == "POST":
        form = AddEventForm(request.POST)
        if form.is_valid():
            event = Event(
                event_name=request.POST['event_name'],
                description=request.POST['description'], 
)
            event.save()
            return redirect("event")
    
    else:
        form = AddEventForm()
    return render(request, "apps/add_event.html", {"form": form})

def update_event(request: HttpRequest, id) -> HttpResponse:
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    event = Event.objects.get(id=id)
    if request.method == "POST":
        form = AddEventForm(request.POST)
        if form.is_valid():
            event.event_name = request.POST['event_name']
            event.description = request.POST['description']
            
            event.save()
            return redirect("event")
    else:
        form = AddEventForm(initial={
            'event_name': event.event_name,
            'description': event.description,
        })
    return render(request, "apps/update_event.html", {"form": form}) 

def delete_event(request: HttpRequest, id) -> HttpResponse:
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    event = Event.objects.get(id=id)
    event.delete()
    return redirect("event")

def payment_method(request: HttpRequest) -> HttpResponse:
    payment_method = Payment_Method.objects.all()
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    return render(request, "apps/payment.html", {'payment': payment_method,})

def create_payment_method(request: HttpRequest) -> HttpResponse:
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    if request.method == "POST":
        form = AddPaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method = Payment_Method(
                payment_method=request.POST['payment_method'],
                account_number=request.POST['account_number'], 
)
            payment_method.save()
            return redirect("payment")
    
    else:
        form = AddPaymentMethodForm()
    return render(request, "apps/add_payment.html", {"form": form})

def update_payment_method(request: HttpRequest, id) -> HttpResponse:
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    payment_method = Payment_Method.objects.get(id=id)
    if request.method == "POST":
        form = AddPaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method.payment_method = request.POST['payment_method']
            payment_method.account_number = request.POST['account_number']
            
            payment_method.save()
            return redirect("payment")
    else:
        form = AddPaymentMethodForm(initial={
            'payment_method': payment_method.payment_method,
            'account_number': payment_method.account_number,
        })
    return render(request, "apps/update_payment.html", {"form": form})

def delete_payment_method(request: HttpRequest, id) -> HttpResponse:
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    payment_method = Payment_Method.objects.get(id=id)
    payment_method.delete()
    return redirect("payment")

def invoice(request: HttpRequest) -> HttpResponse:
    invoice = Invoice.objects.all()
    listinvoice = []
    for i in invoice:
        invoices = {
            'id': i.id,
            'product': i.product.product_name,
            'event': i.event.event_name,
            'quantity': i.quantity,
            'total_price': i.total_price,
            'date': i.date,
            'discount': i.discount,
            'payment_method': i.payment_method,
            'customer': i.customer,
            'sales': i.sales,
        }
        listinvoice.append(invoices)

    
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    return render(request, "apps/invoice.html", {'invoice': listinvoice,})

def create_invoice(request: HttpRequest) -> HttpResponse:
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    if request.method == "POST":
        form = AddInvoiceForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            selected_product = Product.objects.get(id=product)
            event = form.cleaned_data['event']
            selected_event = Event.objects.get(id=event)
            quantity = form.cleaned_data['quantity']
            total_price = form.cleaned_data['total_price']
            discount = form.cleaned_data['discount']
            payment_method = form.cleaned_data['payment_method']
            customer = form.cleaned_data['customer']
            sales = form.cleaned_data['sales']
            invoice = Invoice(
                product=selected_product,
                event=selected_event,
                quantity=quantity,
                total_price=total_price,
                discount=discount,
                payment_method=payment_method,
                customer=customer,
                sales=sales,)
            invoice.save()
            
            print(invoice.event.event_name)
            # date_mm_dd_yyyy = request.POST['date']

            # # Convert mm/dd/yyyy to dd/mm/yyyy format
            # date_parts = date_mm_dd_yyyy.split('-')
            # date_dd_mm_yyyy = f"{date_parts[2]}/{date_parts[1]}/{date_parts[0]}"
            # print(date_dd_mm_yyyy)
            return redirect("invoice")
    
    else:
        products = Product.objects.all()
        product_data = {product.id: product.price for product in products}
        form = AddInvoiceForm()
    return render(request, "apps/add_invoice.html", {"product":products, "product_data": product_data, "form": form})

def update_invoice(request: HttpRequest, id) -> HttpResponse:
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    invoice = Invoice.objects.get(id=id)
    if request.method == "POST":
        form = AddInvoiceForm(request.POST)
        if form.is_valid():
            invoice.product = Product.objects.get(id=form.cleaned_data['product'])
            invoice.event = Event.objects.get(id=form.cleaned_data['event'])
            invoice.quantity = form.cleaned_data['quantity']
            invoice.total_price = form.cleaned_data['total_price']
            invoice.discount = form.cleaned_data['discount']
            invoice.payment_method = form.cleaned_data['payment_method']
            invoice.customer = form.cleaned_data['customer']
            invoice.sales = form.cleaned_data['sales']
            invoice.save()
            return redirect("invoice")
    else:
        form = AddInvoiceForm(initial={
            'product': invoice.product.id,
            'event': invoice.event.id,
            'quantity': invoice.quantity,
            'total_price': invoice.total_price,
            'discount': invoice.discount,
            'payment_method': invoice.payment_method,
            'customer': invoice.customer,
            'sales': invoice.sales,
        })
        products = Product.objects.all()
        product_data = {product.id: product.price for product in products}
    return render(request, "apps/update_invoice.html", {"product":products, "product_data": product_data, "form": form})


def view_invoice(request: HttpRequest, id) -> HttpResponse:
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    invoice = Invoice.objects.get(id=id)
    payment_method = Payment_Method.objects.get(id=invoice.payment_method)
    listinvoice = {
        'id': invoice.id,
        'product': invoice.product.product_name,
        'event': invoice.event.event_name,
        'quantity': invoice.quantity,
        'total_price': invoice.total_price,
        'date': invoice.date,
        'discount': invoice.discount,
        'payment_method': payment_method.payment_method,
        'customer': invoice.customer,
        'sales': invoice.sales,
    }
    print(invoice.payment_method)
    return render(request, "apps/detail_invoice.html", {"invoice": listinvoice})


def delete_invoice(request: HttpRequest, id) -> HttpResponse:
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    invoice = Invoice.objects.get(id=id)
    invoice.delete()
    return redirect("invoice")

def prediction_page(request: HttpRequest) -> HttpResponse:
    auth = auth_check(request)
    if auth is not None:
        return auth
    
    pf = PredictionForm()
    return render(request, "apps/prediction.html", {"form": pf})

model_path = pathlib.Path(__file__).resolve().parent.parent /'apps' / 'model' / 'MachineLearningProject.joblib'
model = joblib.load(model_path)

@csrf_exempt
def prediction(request: HttpRequest) -> HttpResponse:
    item = Product.objects.all()
    
    if request.method == 'POST':
        data = json.loads(request.body)
    
    # Extracting features from the date
        date = datetime.strptime(data.get('date'), '%d/%m/%Y')  # Assuming date is the 7th feature
        day_of_week = date.weekday()
        month = date.month
        year = date.year
    
        event = Event.objects.get(id=data.get('event')).event_name
    
    # Convert the Event object to a dictionary
        

    # Prepare the prediction data for all items
        prediction_data = []
        for item_name in item:
            data_instance = {
                'Event': event,  # Use the dictionary representation of Event
                'Item': item_name.product_name,
                'DayOfWeek': day_of_week,
                'Month': month,
                'Year': year,
            }
            prediction_data.append(data_instance)

        # Convert the prediction data list to a DataFrame
        prediction_df = pd.DataFrame(prediction_data)

        # Predict the demand for all items during the specified event
        predicted_demand = model.predict(prediction_df)

        # Add the predicted demand to the DataFrame
        prediction_df['Predicted_Demand'] = predicted_demand

        # Round the predicted demand to the nearest integer
        prediction_df['Predicted_Demand'] = prediction_df['Predicted_Demand'].round()

        # Sort the DataFrame by the predicted demand in descending order
        prediction_df = prediction_df.sort_values(by='Predicted_Demand', ascending=False)

        # Select only the top 5 predictions
        top5_predictions = prediction_df.head(10)

        # Convert the top 5 predictions to a dictionary for JSON response
        prediction_result = top5_predictions.to_dict(orient='records')
            

        return JsonResponse({'prediction_result': prediction_result})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def auth_check(request):
    
    if not request.user.is_authenticated:
        return redirect("login")
    
    return None
