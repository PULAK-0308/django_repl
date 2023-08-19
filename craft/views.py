from math import ceil

from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import  render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.views.generic import View
from django.contrib import messages
from .models import Product,Orders,OrderUpdate,Contact
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import generate_token
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import razorpay

keyid='rzp_test_FYqvo67zNk6DSr'
keySecret='Pl4QMyOBjXMbg7NkjohzBQf4'




#email-pj@gmail.com
#password-100
#email-jpp@gmail.com
#password-200



# Create your views here.

def index(request):
    
    return render(request,'index.html')

def signup(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'signup.html')                   
        try:
            if User.objects.get(username=email):
                # return HttpResponse("email already exist")
                messages.info(request,"Email is Taken")
                return render(request,'signup.html')
        except Exception as identifier:
            pass
        user = User.objects.create_user(email,email,password)
        user.is_active=False
        user.save()
        email_subject="Activate Your Account"
        message=render_to_string('activate.html',{
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)

        })

        # email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
        # email_message.send()
        messages.success(request,f"Activate Your Account by clicking the link in your gmail {message}")
        return redirect('login')
    return render(request,"signup.html")


class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account Activated Successfully")
            return redirect('login')
        return render(request,'activatefail.html')

def handlelogin(request):
    if request.method=="POST":

        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username,password=userpassword)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('mainpage')

        else:
            messages.error(request,"Invalid Credentials")
            return redirect('login')

    return render(request,'login.html')  






def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('login')


class RequestResetEmailView(View):
    def get(self,request):
        return render(request,'request-reset-email.html')
    
    def post(self,request):
        email=request.POST['email']
        user=User.objects.filter(email=email)

        if user.exists():
            # current_site=get_current_site(request)
            email_subject='[Reset Your Password]'
            message=render_to_string('reset-user-password.html',{
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0])
            })

            # email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            # email_message.send()

            messages.info(request,f"WE HAVE SENT YOU AN EMAIL WITH INSTRUCTIONS ON HOW TO RESET THE PASSWORD {message} " )
            return render(request,'request-reset-email.html')

class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if  not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Reset Link is Invalid")
                return render(request,'request-reset-email.html')

        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request,'set-new-password.html',context)

    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'set-new-password.html',context)
        
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Success Please Login with NewPassword")
            return redirect('login')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something Went Wrong")
            return render(request,'set-new-password.html',context)

        return render(request,'set-new-password.html',context)
     
@login_required(login_url="login")
def mainpage(request):
    return render(request,'mainpage.html')

@login_required(login_url="login")
def dreamcatchers(request):
    products=Product.objects.all()
    
    allProds=[]
    catprods=Product.objects.values('category','id')
    #print(catprods)
    cats={item['category'] for item in catprods}
    #print("categories are ",cats)
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        print(prod)
        n=len(prod)
        nslides=n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nslides),nslides])
        #print(allProds) 
    params={'allProds':allProds}
    return render(request,'dreamcatchers.html',params)

# @login_required(login_url="loginuser")
# def resinproducts(request):
#     products=Product.objects.all()
#     print(products)
#     return render(request,'resinproducts.html',context={'products':products})

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('login')

    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        Order = Orders(items_json=items_json,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        print(amount)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        update.save()
        thank = True
# # PAYMENT INTEGRATION

        amount=int(amount)*100
        client = razorpay.Client(auth=(keyid,keySecret))
        callback_url='http://127.0.0.1:8000/handlerequest'

        data = { "amount":amount, "currency": "INR", "receipt": str(Order.order_id),
                "notes":{
                    "name":"craftcatcher",
                    "Payment for":"crafte items",
                    "Name":Order.name,
                    "Email":Order.email,
                    "Phone":Order.phone
                }}
        payment = client.order.create(data=data)
        print(payment)
        return render(request,'payment.html',{'payment':payment,'callback_url':callback_url,'Order.name':Order.name,'Order.email':Order.email,'Order.phone':Order.phone})

    return render(request, 'checkout.html')

@csrf_exempt
def handlerequest(request):
    if request.method=="POST":
        payment_id=request.POST.get('razorpay_payment_id')
        order_id=request.POST.get('razorpay_order_id')
        signature=request.POST.get('razorpay_signature')
        print(payment_id,order_id,signature)
    
    return render(request,'dreamcatchers.html')
    
        
def contact(request):
    
    thank=False
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank=True
    
    return render(request,'contact.html',{'thank':thank})


def gallery(request):
    return render(request,'gallery.html')