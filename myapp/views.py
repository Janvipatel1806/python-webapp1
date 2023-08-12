from django.shortcuts import render,redirect
from .models import User,SUser,Additem,Wishlist,Cart
import requests
import random
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from django.http import JsonResponse
# Create your views here.
stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000'

@csrf_exempt
def create_checkout_session(request):
	amount=int(json.load(request)['post_data'])
	final_amount=amount*100


	session = stripe.checkout.Session.create(
 		payment_method_types=['card'],
 		line_items=[{
 			'price_data': {
 				'currency': 'inr',
 				'product_data': {
 					'name': 'Intro to Django Course',
 					},
 				'unit_amount': final_amount,
 				},
			'quantity': 1,
 			}],
		mode='payment',
 		success_url=YOUR_DOMAIN + '/success.html',
 		cancel_url=YOUR_DOMAIN + '/cancel.html',)
	return JsonResponse({'id': session.id})



def success(request):
	#user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(pstatus=False)
	for i in carts:
		i.pstatus=True
		i.save()


	carts=Cart.objects.filter(pstatus=False)
	request.session['ccount']=len(carts)
	return render(request,'success.html')

def cancel(request):
 return render(request,'cancel.html')

def myorder(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,pstatus=True)
	return render(request,'myorder.html',{'carts':carts})

def validate_signup(request):
	email=request.GET.get('email')
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
	}

	return JsonResponse(data)

def index(request):
	return render(request,'index.html')
def blog(request):
	return render(request,'blog.html')
def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['lpassword']:
				request.session['email']=user.email
				request.session['fname']=user.fname
				wishlists=Wishlist.objects.filter(user=user)
				request.session['count']=len(wishlists)
				carts=Cart.objects.filter(user=user,pstatus=False)
				request.session['ccount']=len(carts)
				return render(request,'index.html')
			else:
				msg="Invalied Password "
				return render(request,'login.html',{'msg':msg})
		except:
			msg="Email is not registered"
			return render(request,'login.html',{'msg':msg})


	else:
		return render(request,'login.html')
def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email is already registered"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
				fname=request.POST['fname'],
				lname=request.POST['lname'],
				email=request.POST['email'],
				mobile=request.POST['mobile'],
				password=request.POST['password']
				)
				return render(request,'login.html')
			else:
				msg="Password & confirm password doesn't matched"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')
def logout(request):
	try:
		del request.session['fname']
		del request.session['email']
		del request.session['count']
		del request.session['ccount']
		return render(request,'login.html')
	except:
		return render(request,'login.html')
def change_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.session['email'])
			if user.password==request.POST['old']:
				if request.POST['npassword']==request.POST['cnpassword']:
					user.password=request.POST['npassword']
					user.save()
					return render(request,'login.html')
				else:
					msg="Password and confirm password doesn't matched"
					return render(request,'change_password.html',{'msg':msg})
			else:
				msg="Old password is wrong"
				return render(request,'change_password.html',{'msg':msg})
		except:
			return render(request,'logout.html')


	else:
		return render(request,'change_password.html')

def forgotpassword(request):
	if request.method=="POST":
		mobile=request.POST['mobile']
		url = "https://www.fast2sms.com/dev/bulkV2"
		otp=random.randint(1000,9999)
		querystring = {"authorization":"gsBNi3zF1atJTHPw2moMDyeK5nSAZUbr6WRudG8lYfkqjpQXvV1UaPGu9Afh3Bm6qskIYlKgL4yr8tdJ","variables_values":str(otp),"route":"otp","numbers":str(mobile)}
		headers = {'cache-control': "no-cache"}
		response = requests.request("GET", url, headers=headers, params=querystring)
		print(response.text)
		return render(request,'otp.html',{'mobile':mobile,'otp':otp})
	else:
		return render(request,'forgotpassword.html')

def verifyotp(request):
	mobile=request.POST['mobile']
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	if otp==uotp:
		return render(request,'newpassword.html',{'mobile':mobile})
	else:
		msg="Invalied OTP"
		return render(request,'otp.html',{'mobile':mobile,'otp':otp,'msg':msg})
def newpassword(request):
	mobile=request.POST['mobile']
	np=request.POST['npassword']
	cnp=request.POST['cnpassword']
	if np==cnp:
		user=User.objects.get(mobile=mobile)
		user.password=np
		user.save()
		msg="Password updated successfully"
		return render(request,'login.html',{'msg':msg})
	else:
		msg="Password & confirm password doesn't matched"
		return render(request,'newpassword.html',{'msg':msg})

def ssignup(request):
	if request.method=="POST":
		try:
			SUser.objects.get(email=request.POST['email'])
			msg="Email is already registered"
			return render(request,'ssignup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				SUser.objects.create(
				fname=request.POST['fname'],
				lname=request.POST['lname'],
				email=request.POST['email'],
				mobile=request.POST['mobile'],
				password=request.POST['password']
				)
				return render(request,'slogin.html')
			else:
				msg="Password & confirm password doesn't matched"
		return render(request,'ssignup.html',{'msg':msg})
	else:
		return render(request,'ssignup.html')
def slogin(request):
	if request.method=="POST":
		try:
			user=SUser.objects.get(email=request.POST['email'])
			if user.password==request.POST['lpassword']:
				request.session['email']=user.email
				request.session['fname']=user.fname
				return render(request,'sindex.html')
			else:
				msg="Invalied Password "
				return render(request,'slogin.html',{'msg':msg})
		except:
			msg="Email is not registered"
			return render(request,'slogin.html',{'msg':msg})
	else:
		return render(request,'slogin.html')


def slogout(request):
	try:
		del request.session['fname']
		del request.session['email']
		return render(request,'slogin.html')
	except:
		return render(request,'slogin.html')
def sindex(request):
	return render(request,'sindex.html')

def seller_add_product(request):
	seller=SUser.objects.get(email=request.session['email'])
	if request.method=="POST":
		Additem.objects.create(
			seller=seller,
			price=request.POST['price'],
			brand=request.POST['brand'],
			size=request.POST['size'],
			pic=request.FILES['pic']
			)
		return render(request,'seller-add-product.html')
	else:
		return render(request,'seller-add-product.html')
def seller_view_product(request):

 	seller=SUser.objects.get(email=request.session['email'])
 	additem=Additem.objects.filter(seller=seller)
 	return render(request,'seller-view-product.html',{'additem':additem})

def seller_product_details(request,pk):
	product=Additem.objects.get(pk=pk)
	return render(request,'seller-product-details.html',{'product':product})
def product_details(request,pk):
	wishlist_flag=0
	cart_flag=0
	product=Additem.objects.get(pk=pk)
	user=User.objects.get(fname=request.session['fname'])
	try:
		Wishlist.objects.get(user=user,product=product)
		wishlist_flag=1
	except:
		pass
	
	try:
		Cart.objects.get(user=user,product=product)
		cart_flag=1
	except:
		pass
	return render(request,'product-details.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})
	
def seller_edit_product(request,pk):
	product=Additem.objects.get(pk=pk)
	if request.method=="POST":
		product.price=request.POST['price']
		product.brand=request.POST['brand']
		product.size=request.POST['size']
		try:
			product.pic=request.FILES['pic']
		except:
			pass
		product.save()
		msg="Updated successfully"
		return render(request,'seller-edit-product.html',{'product':product,'msg':msg})
	else:
		return render(request,'seller-edit-product.html',{'product':product})
def seller_delete_product(request,pk):
	product=Additem.objects.get(pk=pk)
	product.delete()
	return redirect('seller-view-product')
def category(request):
	additem=Additem.objects.all()
	return render(request,'category.html',{'additem':additem})
def add_to_wishlist(request,pk):
	product=Additem.objects.get(pk=pk)
	user=User.objects.get(fname=request.session['fname'])
	Wishlist.objects.create(user=user,product=product)
	return redirect('wishlist')

def wishlist(request):
	user=User.objects.get(fname=request.session['fname'])
	wishlists=Wishlist.objects.filter(user=user)
	request.session['count']=len(wishlists)
	return render(request,'wishlist.html',{'wishlists':wishlists})

def remove_from_wishlist(request,pk):
	product=Additem.objects.get(pk=pk)
	user=User.objects.get(fname=request.session['fname'])
	wishlist=Wishlist.objects.get(user=user,product=product)
	wishlist.delete()
	return redirect('wishlist')




def add_to_cart(request,pk):
	product=Additem.objects.get(pk=pk)
	user=User.objects.get(fname=request.session['fname'])
	Cart.objects.create(
		user=user,
		product=product,
		price=product.price,
		qty=1,
		total=product.price,
		)
	return redirect('cart')

def cart(request):
	net_price=0
	user=User.objects.get(fname=request.session['fname'])
	carts=Cart.objects.filter(user=user,pstatus=False)
	for i in carts:
		net_price=net_price+i.total
	request.session['ccount']=len(carts)
	return render(request,'cart.html',{'carts':carts,'net_price':net_price})

def remove_from_cart(request,pk):
	product=Additem.objects.get(pk=pk)
	user=User.objects.get(fname=request.session['fname'])
	carts=Cart.objects.get(user=user,product=product)
	carts.delete()
	return redirect('cart')

def cqty(request):
	pk=int(request.POST['pk'])
	qty=int(request.POST['qty'])
	cart=Cart.objects.get(pk=pk)
	cart.total=cart.price*qty
	cart.qty=qty
	cart.save()
	return redirect('cart')

