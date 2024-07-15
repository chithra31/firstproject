from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from .models import Product , Viewproduct, Cart
from django.http import HttpResponse
from django.template import loader
import json
from django.http import  JsonResponse




def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("login")

def register(request):
  if request.method=='POST':
        name=request.POST["username"]
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]

        if password1==password2:        
            user=User.objects.create_user(username=name,email=email,password=password1)
            user.is_staff=True
            user.is_superuser=True
            user.save()
            messages.success(request,'Your account has been created successfully')
            return redirect('login')
        else:
            messages.warning(request,'Password Mismatching...!!!')
            return redirect('register')        
  else:
        form=CreateUserForm()        
        return render(request,"register.html",{'form':form})


def profile(request):
   return render(request,"profile.html")


def loginpage(request):
  details = Product.objects.all().values()
  template = loader.get_template('loginpage.html')
  context = {
    'details': details,
  }
  return HttpResponse(template.render(context, request))

def loginpageview(request,name):
  if(Product.objects.filter(name=name,status=0)):
    products=Product.objects.filter(name=name,status=0).first()
    return render(request,"pdetails.html",{"products":products})
  else:
    messages.error(request,"No Such Product Found")
    return redirect('loginpage')
   
def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      #print(request.user.id)
      product_status=Product.objects.get(id=product_id)
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Cart'}, status=200)
        else:
          if product_status.quantity>=product_qty:
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'Product Added to Cart'}, status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)



def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"cart.html",{"cart":cart})
  else:
    return redirect("/")

def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")
