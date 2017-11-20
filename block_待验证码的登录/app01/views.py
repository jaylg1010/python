from django.shortcuts import render,HttpResponse,redirect
from django.conf import settings
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib import auth
import json
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
import random

from app01 import models

# Create your views here.


# login function
def login(request):
    if request.is_ajax():

        name = request.POST.get('username')
        pwd = request.POST.get('pwd')
        validCode = request.POST.get('validCode')
        print("_+_+_+_+_+", name)
        print("_+_+_+_+_+", pwd)
        print("_+_+_+_+_+", validCode)
        print("+_+_+_+_+_",request.session.get("validCode"))

        login_response={"is_login":False,"error_msg":None}
        if validCode.upper() == request.session.get("validCode").upper():
            user=auth.authenticate(username=name,password=pwd)
            if user:
                login_response["is_login"]=True
                auth.login(request,user)
            else:
                login_response["error_msg"] = "username or password error"
        else:
            login_response["error_msg"]="validCode error"

        return HttpResponse(json.dumps(login_response))

    return render(request,'login.html')

# blog home
def blog(request):
    return render(request,'blog.html')


# 注册form表单
class RegisterForm(Form):
    email=fields.EmailField(
        required=True,
        error_messages={
            'required':'邮箱不能为空',
        },
        validators=[RegexValidator('\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}','邮箱格式不对')],
        widget=widgets.EmailInput(attrs={"type": "email", "class": "form-control", "id": "id_email", "placeholder": "需要通过邮件激活账号"})
    )

    telephone=fields.IntegerField(
        required=True,
        error_messages={
            'required':'手机号不能为空',
        },
        validators=[RegexValidator('0?(13|14|15|18)[0-9]{9}','手机格式不对')],
        widget=widgets.NumberInput(attrs={"type": "number", "class": "form-control", "id": "id_telephone", "placeholder": "激活账户需要手机短信验证"})
    )

    username=fields.CharField(
        required=True,
        min_length=4,
        error_messages={
            'required':'用户名不能为空',
            'min_length':'用户名不能小于4位',
        },
        widget = widgets.TextInput(attrs={"type":"text","class":"form-control","id":"id_username","placeholder":"登录用户名"})
    )

    nickname=fields.CharField(
        required=True,
        min_length=2,
        error_messages={
            'required':'昵称不能为空',
            'min_length':'昵称不能小于2位',
        },
        widget=widgets.TextInput(attrs={"type": "text", "class": "form-control", "id": "id_nickname", "placeholder": "昵称"})
    )

    password=fields.CharField(
        required=True,
        min_length=8,
        max_length=20,
        error_messages={
            'required':'密码不能为空',
            'min_length':'密码长度最小为8位',
            'max_length':'密码最大长度为20位'
        },
        widget=widgets.PasswordInput(attrs={"type": "password", "class": "form-control", "id": "id_password", "placeholder": "密码"})
    )

    confirm_password=fields.CharField(
        required=True,
        min_length=8,
        max_length=20,
        error_messages={
            'required':'密码不能为空',
            'min_length':'密码长度最小为8位',
            'max_length':'密码最大长度为20位'
        },
        widget=widgets.PasswordInput(attrs={"type": "password", "class": "form-control", "id": "id_confirm_password", "placeholder": "确认密码"})
    )


    def clean_email(self):
        email=self.cleaned_data['email']
        is_exit=models.UserInfo.objects.filter(email=email).first()
        if is_exit:
            raise ValidationError('该邮箱已存在')
        return email

    def clean_telephone(self):
        telephone=self.cleaned_data['telephone']
        is_exit=models.UserInfo.objects.filter(telephone=telephone)
        if is_exit:
            raise ValidationError('该手机号码已经注册')
        return telephone

    def clean_username(self):
        username=self.cleaned_data['username']
        is_exit=models.UserInfo.objects.filter(username=username).first()
        if is_exit:
            raise ValidationError('该账户已经存在')
        return username

    def clean_nickname(self):
        nickname=self.cleaned_data['nickname']
        is_exit=models.UserInfo.objects.filter(nickname=nickname).first()
        if is_exit:
            raise ValidationError('该昵称已经被占用，请更换')
        return nickname

    # def clean(self):
    #     password=self.cleaned_data['password']
    #     confirm_password=self.cleaned_data['confirm_password']
    #     if password == confirm_password:
    #         return password
    #     else:
    #         raise ValidationError('两次密码不正确，请重新输入')

# register function
def register(request):
    """注册功能"""
    if request.method == "GET":
        form=RegisterForm()
        return render(request,'register.html',{'form':form})
    else:
        form=RegisterForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            models.UserInfo.objects.create(email=form.cleaned_data['email'],telephone=form.cleaned_data['telephone'],username=form.cleaned_data['username'],
                                           nickname=form.cleaned_data['nickname'],password=form.cleaned_data['password'])
        return render(request,'register.html',{'form':form})

# Production verification code
def get_verify(request):
    """通过PIL模块，获取图片，字体；生成随机图片返回前端"""
    img=Image.new(mode="RGB",size=(170,50),color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    draw=ImageDraw.Draw(img,"RGB")
    font=ImageFont.truetype("app01/static/font/kumo.ttf",25)


    valid_list=[]
    for i in range(5):
        random_num=str(random.randint(0,9))
        random_lower_letter=chr(random.randint(65,90))
        random_upper_letter=chr(random.randint(97,122))

        # 干扰线
        x1 = random.randint(50, 70)
        y1 = random.randint(0, 80)
        x2 = random.randint(20, 500)
        y2 = random.randint(10, 1000)
        x3 = random.randint(200,800)
        x4 = random.randint(3000,4000)

        draw.line((x1,y1,x2,y2))

        random_char=random.choice([random_num,random_lower_letter,random_upper_letter])
        draw.text([5+i*24,10],random_char,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),font=font)

        valid_list.append(random_char)



    f=BytesIO()
    img.save(f,"png")
    data=f.getvalue()

    valid_str="".join(valid_list)
    request.session['validCode']=valid_str

    return HttpResponse(data)



def logout(request):
    auth.logout(request)

    return redirect("/login/")
