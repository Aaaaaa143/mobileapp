from django.shortcuts import render,redirect
from django.views.generic import View
from mobile.models import Mobiles
from mobile.forms import MobileForm,RegistrationForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,login,logout
from django.utils.decorators  import method_decorator

# decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not  request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
    


# localhost:8000/mobiles/all/

@method_decorator(signin_required,name="dispatch")
class MobileListView(View):

    
    def get(self,request,*args,**kwargs):
        # print(request.GET)#{brand:samsang}
        qs=Mobiles.objects.all() 
        if "brand" in request.GET:
            brand=request.GET.get("brand")
            qs=qs.filter(brand__iexact=brand) #iexact=>case insensitive

        if "display" in request.GET:
            display=request.GET.get("display")
            qs=qs.filter(display=display)

        if "price_lt" in request.GET:
            amount=request.GET.get("price_lt")
            qs=qs.filter(price__lte=amount)
        
        return render(request,'mobile_list.html',{'data':qs})
    

# localhost"8000/mobiles/{id}/

@method_decorator(signin_required,name="dispatch")
class MobileDetailView(View):

    def get(self,request,*args,**kwargs):
        # if not request.user.is_authenticated:
        #     return redirect("signin")
        
        print(kwargs)
        id=kwargs.get("pk")
        qs=Mobiles.objects.get(id=id)
        return render(request,"mobile_detail.html",{"data":qs})

# localhost"8000/mobiles/{id}/remove

@method_decorator(signin_required,name="dispatch")
class MobileDeleteView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Mobiles.objects.get(id=id).delete()
        messages.success(request,"mobile details deleted...!")
        return redirect("mobile-all")
    

# /localhost:8000/mobiles/add/
# get=>mobile_add.html form
# post=>

@method_decorator(signin_required,name="dispatch")
class MobileCreateView(View):

    def get(self,request,*args,**kwargs):
        form=MobileForm()
        return render(request,"mobile_add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=MobileForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request," new mobile is added... ")
            return redirect("mobile-all")
        else:
            messages.error(request,"error.....can't create mobile data...")
            return render(request,"mobile_add.html",{"form":form})


# localhost:8000/{id}/change/

@method_decorator(signin_required,name="dispatch")
class MobileUpdateView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Mobiles.objects.get(id=id)
        form=MobileForm(instance=obj)
        return render(request,"mobile_edit.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Mobiles.objects.get(id=id)
        form=MobileForm(request.POST,instance=obj,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"mobile data successfully updated...")
            return redirect("mobile-all")
        else :
            messages.error(request,"can't update mobile data...")
            return render(request,"mobile_edit.html",{"form":form})
        


class SignUpView(View):

    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)

        if form.is_valid():
            #form.save()#User.objects.create(**form.cleaned_data)
            User.objects.create_user(**form.cleaned_data)

            messages.success(request,"account created successfully")
            return render(request,"register.html",{"form":form})
        else:
            messages.error(request,"failed to create an account")
            return render(request,"register.html",{"form":form})

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pswd=form.cleaned_data.get("password")
            print(uname,pswd)
            user_object=authenticate(request,username=uname,password=pswd)
            if user_object:
                print("valid credentials")
                #section starts
                login(request,user_object)
                print(request.user) #fetch user details
                return redirect("mobile-all")

            else:
                print("invalid credentials")
            return render(request,"login.html",{"form":form})
        else:
            return render(request,"login.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
