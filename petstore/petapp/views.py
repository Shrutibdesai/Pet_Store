from django.shortcuts import render, redirect
from petapp.models import Pet, Cart, Order
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q 
import razorpay
import random
from django.core.mail import send_mail

# Create your views here.
def home(request):
   context={}
   data = Pet.objects.all()
   context['pets']=data
   return render(request,'index.html',context)

def showPetDetails(request,rid):
   context={}
   data = Pet.objects.get(id=rid)
   context['pet']=data
   return render(request,'details.html',context)

def registerUser(request):
   if request.method =="GET":
      return render(request,'register.html')
   else:      
      # 1. capture the values entered by user
      u = request.POST['username']
      if User.objects.filter(username=u).exists():
         context={'error':'Username already registered!! Please enter a different username for registration. '}
         return render(request,'register.html',context)
      else:
         e = request.POST['email']
         p = request.POST['password']
         cp = request.POST['confirmpassword']
         # form validation
         if u=='' or e=='' or p=='' or cp=='':
            context={'error':'all fields are compulsory'}
            return render(request,'register.html',context)
         elif p != cp :
            context={'error':'Pasword and Confirm Password must be same'}
            return render(request,'register.html',context)
         else:
            #2.  insert in db
            # u = User.objects.create(username=u,password=p,email=e)
            # u.save()
            # above code will insert user details in table, but password is in plain text and not encrypted
            #use below code so as to encrypt the password, for security
            u = User.objects.create(username=u,email=e)
            u.set_password(p)# for password encryption
            u.save()  
            # context = {'success':'Registred successfully , plz login'} 
            messages.success(request,'Registered successfully, Please login')
            return redirect('/login')
         
def userLogin(request):
   if request.method == "GET":
      return render(request,'login.html')
   else:
      # login activity
      u = request.POST['username']
      p = request.POST['password']
      auth = authenticate(username=u, password=p)
      print('logged in user:',auth)
      if auth == None: # user not verified
         context={'error':'Please provide correct details to login'}
         return render(request,'login.html',context)
      else: # user is verified
         login(request,auth)
         return redirect('/')
      
def userLogout(request):  
   logout(request)
   messages.success(request,'User Logged out successfully !!')
   return redirect('/')

def addToCart(request,petid):
   userid = request.user.id 
   if userid is None:
      context={'error':'Please login, so as to add your favourite Pet in your cart!!'}
      return render(request,'login.html',context)
   else:
      user = User.objects.get(id = userid)
      pet = Pet.objects.get(id=petid) 
      cart = Cart.objects.create(uid=user, pid=pet)
      cart.save()
      messages.success(request,'Pet added to cart successfully !!')
      return redirect('/')     
   
def showUserCart(request):
   user = request.user
   cart = Cart.objects.filter(uid = user.id )
   totalBill = 0
   for c in cart:
      totalBill += c.pid.price * c.quantity
   count = len(cart)
   context={}
   context['cart']=cart
   context['total']=totalBill
   context['count']=count  
   return render(request,'showcart.html',context)

def removeCart(request,cartid):
   cart = Cart.objects.filter(id = cartid)
   cart.delete()
   messages.success(request,'Pet removed from your cart!!')
   return redirect('/showcart')

def updateCart(request, opr, cartid):
   cart = Cart.objects.filter(id=cartid)   
   if opr == '1':
      cart.update(quantity = cart[0].quantity+1)
   else: #opr=='0'
      cart.update(quantity = cart[0].quantity-1)
   return redirect('/showcart')   
   
def searchByType(request, pet_type):
   petList = Pet.objects.filter(type=pet_type)
   context={'pets':petList}
   return render(request,'index.html',context)

def searchByRange(request):
   # url : /range?min=24000&max=28000
   min = request.GET['min']
   max = request.GET['max']
   c1 = Q(price__gte = min)
   c2 = Q(price__lte = max)
   petList = Pet.objects.filter(c1 & c2)
   context={'pets':petList}
   return render(request,'index.html',context)

def sortByPrice(request,dir):
   col=''
   if dir == 'asc':
      col='price'
   else : # dir='desc'
      col='-price'
   # print("sort Direction:",dir)
   # print(col)
   petList = Pet.objects.all().order_by(col)
   context={'pets':petList}
   return render(request,'index.html',context)

def confirmOrder(request):
   user = request.user
   cart = Cart.objects.filter(uid = user.id )
   totalBill = 0
   for c in cart:
      totalBill += c.pid.price * c.quantity
   count = len(cart)
   context={}
   context['cart']=cart
   context['total']=totalBill
   context['count']=count  
   return render(request,'confirmorder.html',context)

def makepayment(request):
   user = request.user 
   userCart = Cart.objects.filter(uid = user.id )
   totalBill = 0
   for c in userCart:
      totalBill += c.pid.price * c.quantity
   
   # client = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))
   client = razorpay.Client(auth=("rzp_test_jUMUt8q0Zgt1Jc", "ez3IEjbskPudiBZKob2LY7kN"))
   data = { "amount": totalBill*100, "currency": "INR", "receipt": "" }
   payment = client.order.create(data=data)
   context={'data':payment}
   print(payment)
   return render(request,'pay.html',context)

def placeOrder(request):
   # 1. place order (insert order details in order table)
   user = request.user
   myCart = Cart.objects.filter(uid = user.id)
   oId = random.randrange(10000,99999)
   # verify if its not existing in db
   for cart in myCart:
      order = Order.objects.create(orderId = oId, uid = cart.uid, pid = cart.pid, quantity = cart.quantity)
      order.save()
   # 2. clear Cart
   myCart.delete()  
   
   # 3. sending gmail 
   message = 'Your order id is'+str(oId)
   custEmail = request.user.email
   send_mail(
      "Order placed successfully!!",
      message,
      "samruddhi@itvedant.com",
      [custEmail],
      fail_silently=False,
   )
   return redirect('/')