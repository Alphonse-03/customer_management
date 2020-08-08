from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .form import ProductForm,OrderFormEdit,OrderFormCreate,CustomerForm
from .filters import OrderFilterCustomer,OrderFilterDashboard
from .form import RegistraionForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import authenticated,admin_only,allowed_users
from django.contrib.auth.models import Group

# # Create your views here.
@login_required(login_url='login')
@admin_only

def home(request):

	customer=Customer.objects.all()
	order=Order.objects.all()
	total_order=Order.objects.count()
	total_order_delivered=Order.objects.filter(status="Delivered").count()
	total_number_of_pending=Order.objects.filter(status="Pending").count()
	myFilter=OrderFilterDashboard(request.GET,queryset=order)
	order=myFilter.qs

	content={"customers":customer,"orders":order,
			 "total_number_of_order":total_order,
			 "total_number_of_order_delivered":total_order_delivered,
			 "total_number_of_order_pending":total_number_of_pending,
			 "myFilter":myFilter}

	return render(request, 'accounts/dashboard.html',content)


@login_required(login_url='login')
@admin_only
def products(request):

	products=Product.objects.all()

	return render(request, 'accounts/products.html',{"products":products})

@login_required(login_url='login')
def customer(request,pk):

	customers=Customer.objects.get(id=pk)
	order=customers.order_set.all()
	number_of_orders=order.count()
	myFilter=OrderFilterCustomer(request.GET,queryset=order)
	order=myFilter.qs
	return render(request, 'accounts/customer.html',{"customers":customers,"orders":order,"number_of_orders":number_of_orders,"myFilter":myFilter})

#product
@login_required(login_url='login')
@admin_only
def create_product(request):

	if request.user.is_staff:
		form=ProductForm()
		if request.method == 'POST':
			form=ProductForm(request.POST)
			if form.is_valid:
				form.save()
				return redirect("products")
	else:
		return HttpResponse("you are not authorised")
	return render(request,"accounts/createproduct.html",{"form":form})

@login_required(login_url='login')
@admin_only
def delete_product(request,pk):
	product=Product.objects.get(id=pk).name
	p=Product.objects.get(id=pk)
	if request.method == 'POST':
		p.delete()
		return redirect("products")
	return render(request,'accounts/product_delete.html',{"product":product})

@login_required(login_url='login')
@admin_only
def update_product(request,pk):
	product=Product.objects.get(id=pk).name
	p=Product.objects.get(id=pk)
	form=ProductForm(instance=p)
	if request.method == 'POST':
		form=ProductForm(request.POST,instance=p)
		if form.is_valid():
			form.save()
			return redirect("products")
	return render(request,'accounts/product_update.html',{"product":product,"form":form})


#order
@login_required(login_url='login')
@admin_only
def delete_order(request,pk):
	order=Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect("home")
	return render(request,'accounts/delete_order.html',{"order":order})


@login_required(login_url='login')  
@admin_only
def update_order(request,pk):
	order=Order.objects.get(id=pk)
	form=OrderFormEdit(instance=order)
	if request.method == 'POST':
		form=OrderFormEdit(request.POST,instance=order)
		if form.is_valid():
			form.save()
			return redirect("home")
	return render(request,'accounts/update_order.html',{"form":form})


@login_required(login_url='login')
@admin_only
def create_order(request):
	form=OrderFormCreate()
	if request.method == 'POST':
		form=OrderFormCreate(request.POST)
		if form.is_valid:
			form.save()
			return redirect("home")
	return render(request,"accounts/create_order.html",{"form":form})

#customer


@login_required(login_url='login')
@admin_only
def create_customer(request):
	form=CustomerForm()
	if request.method == 'POST':
		form=CustomerForm(request.POST)
		if form.is_valid:
			form.save()
			return redirect("home")
	return render(request,"accounts/create_customer.html",{"form":form})



@login_required(login_url='login')
@admin_only
def delete_customer(request,pk):
	customer=Customer.objects.get(id=pk)
	if request.method == 'POST':
		customer.delete()
		return redirect("home")
	return render(request,'accounts/delete_customer.html',{"customer":customer})

@login_required(login_url='login')
@admin_only
def update_customer(request,pk):
	customer=Customer.objects.get(id=pk)
	form=CustomerForm(instance=customer)
	if request.method == 'POST':
		print(customer)
		print(form)
		form=CustomerForm(request.POST,instance=customer)
		if form.is_valid():
			form.save()
			return redirect("home")
	return render(request,'accounts/update_customer.html',{"form":form,"customer":customer})


@login_required(login_url='login')
@admin_only
def create_order_customer(request,pk):
	form=OrderFormCreate(initial={"customer":Customer.objects.get(id=pk)})
	if request.method == 'POST':
		form=OrderFormCreate(request.POST)
		if form.is_valid:
			form.save()
			return redirect("home")
	return render(request,"accounts/create_order.html",{"form":form})

@authenticated
def login_page(request):
	if request.method =='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect("home")
		else:
			messages.warning(request,"wrong credentials")
	return render(request,"accounts/login.html")

@authenticated
def registration_page(request):
	form=RegistraionForm()
	if request.method == 'POST':
		form=RegistraionForm(request.POST)
		if form.is_valid():
			user=form.save()
			username = form.cleaned_data.get('username')
			group=Group.objects.get(name='customer')
			
			user.groups.add(group)
			Customer.objects.create(
				user=user,
				name=user.username,
			)
			return redirect("login")
		else:
			messages.warning(request,"sorry something went wrong try again")
	return render(request,"accounts/registration.html",{"form":form})

def logoutUser(request):
	logout(request)
	return redirect("login")



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def user_profile(request):
	items=request.user.customer.order_set.all()
	total_order=items.count()
	total_order_delivered=items.filter(status="Delivered").count()
	total_number_of_pending=items.filter(status="Pending").count()
	return render(request,"accounts/user.html",{'products':items,
		 "total_number_of_order":total_order,
		 "total_number_of_order_delivered":total_order_delivered,
		 "total_number_of_order_pending":total_number_of_pending})

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customer_profile(request):
	customer=request.user.customer

	form=CustomerForm(instance=customer)
	if request.method == 'POST':
		form=CustomerForm(request.POST,request.FILES,instance=customer)
		if form.is_valid():
			form.save()	
			return redirect("customer_profile")
	return render(request,"accounts/customer_settings.html",{'form':form})

