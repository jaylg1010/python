from django.shortcuts import render,redirect,HttpResponse
from app01 import models
from django.contrib import auth
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User
# Create your views here.

def index(request):

    #通过request.user可以获取当前的登录用户，然后验证用户
    # print("====requestuser",request.user)
    if request.user.is_authenticated():
        bookList= models.Book.objects.all()

        #制作分页
        paginator=Paginator(bookList,5)  #每页显示的数目
        page_range=paginator.page_range
        num=request.GET.get("page",1)
        bookList=paginator.page(num)
        print("+++++++",bookList,num)

        return render(request,"index.html",{"bookList":bookList,"page_range":page_range,"num":int(num)})
    else:
        return redirect("/login/")

def delBook(request,bookid):
    models.Book.objects.filter(nid=bookid).delete()
    return redirect("/index/")

def editBook(request,bookid):
    if request.method=="GET":
        book=models.Book.objects.get(nid=bookid)
        publishlist = models.Publish.objects.all()
        authorlist = models.Author.objects.all()
        editauthor=book.author.all().values_list("id")
        l=[]
        for i in editauthor:
            l.append(i[0])
        return render(request, "editBook.html", {"book": book,"authorlist":authorlist,"publishlist":publishlist,"l":l})
    else:
        title=request.POST.get("ntitle")
        publicDate=request.POST.get("npublicDate")
        price=request.POST.get("nprice")
        publish_id = request.POST.get("npublish")
        publish = models.Publish.objects.get(id=publish_id)
        author_id = request.POST.getlist("nauthor")
        book_obj=models.Book.objects.get(nid=bookid)
        models.Book.objects.filter(nid=bookid).update(title=title,publicDate=publicDate,price=price,publish=publish)
        authorL = []
        for authorid in author_id:
            author = models.Author.objects.get(id=authorid)
            authorL.append(author)
        book_obj.author.clear()
        book_obj.author.add(*authorL)
        return redirect("/index/")

def addBook(request):
    if request.method=="POST":
        title = request.POST.get("ntitle")
        author_id = request.POST.getlist("nauthor")
        publicDate = request.POST.get("npublicDate")
        price = request.POST.get("nprice")
        publish_id=request.POST.get("npublish")
        publish=models.Publish.objects.get(id=publish_id)
        book_obj=models.Book.objects.create(title=title,publicDate=publicDate,publish=publish,price=price)
        authorL=[]
        for authorid in author_id:
            author=models.Author.objects.get(id=authorid)
            authorL.append(author)
        book_obj.author.add(*authorL)
        return redirect("/index/")
    else:
        authorlist = models.Author.objects.all()
        publishlist=models.Publish.objects.all()
        return render(request,"addBook.html",{"authorlist":authorlist,"publishlist":publishlist})


def login(request):
    #从数据库读取数据，并且制造cookie来验证登录
    # if request.method=="GET":
    #     return render(request,"login.html")
    # else:
    #     username=request.POST.get("username")
    #     password=request.POST.get("passwoed")
    #     ret=models.Loginuser.objects.filter(sqlusername=username,sqlpassword=password)
    #     if ret:
    #         obj=redirect("/index/")
    #         obj.set_cookie("is_login",True,20)
    #         return obj
    #     else:
    #         return render(request,"login.html")

    #通过验证模块来验证登录
    if request.method=="GET":
        return render(request,"login.html")
    else:
        username=request.POST.get("username")
        password=request.POST.get("password")
        print("username",username,"password",password)
        user=auth.authenticate(username=username,password=password)
        print("======user",user)
        if user:
            auth.login(request,user)
            return redirect("/index/")
        else:
            info="账号或密码错误"
            return render(request, "login.html",{"info":info})



def authorindex(request):
    # is_login = request.COOKIES.get("is_login", None)
    # if is_login:
    if request.user.is_authenticated():
        authorList=models.Author.objects.all()
        return render(request,"authorindex.html",{"authorList":authorList})
    else:
        return redirect("/login/")

def delAuthor(request,deauthor_id):
    models.Author.objects.filter(id=deauthor_id).delete()
    return redirect("/authorindex/")

def addAuthor(request):
    if request.method=="POST":
        name=request.POST.get("nname")
        age=request.POST.get("nage")
        tel=request.POST.get("ntel")
        add=request.POST.get("nadd")
        author_obj=models.Author.objects.create(name=name,age=age)
        models.Authordetal.objects.create(tel=tel,addr=add,author=author_obj)
        return redirect("/authorindex/")
    else:
        return render(request,"addAuthor.html")

def editAuthor(request,edit_author_id):
    if request.method=="GET":
        author_obj=models.Author.objects.get(id=edit_author_id)
        return render(request,"editAuthor.html",{"author_obj":author_obj})
    else:
        name=request.POST.get("nname")
        age=request.POST.get("nage")
        tel=request.POST.get("ntel")
        addr=request.POST.get("nadde")


        author_obj = models.Author.objects.filter(id=edit_author_id).update(name=name, age=age)
        models.Authordetal.objects.filter(author=edit_author_id).update(tel=tel,addr=addr)

        return redirect("/authorindex/")


def publishIndex(request):
    # is_login = request.COOKIES.get("is_login", None)
    # if is_login:
    if request.user.is_authenticated():
        pubList=models.Publish.objects.all()
        return render(request,"publishIndex.html",{"pubList":pubList})
    else:
        return render(request, "login.html")

def addPublish(request):
    if request.method=="POST":
        name=request.POST.get("nname")
        addr=request.POST.get("naddr")
        models.Publish.objects.create(name=name,addr=addr)
        return redirect("/publishIndex/")
    return render(request,"addpublish.html")


def delPublish(request,delpub_id):
    models.Publish.objects.get(id=delpub_id).delete()
    return redirect("/publishIndex/")


def editPublish(request,editpub_id):
    if request.method=="GET":
        pub=models.Publish.objects.get(id=editpub_id)
        return render(request,"editpublish.html",{"pub":pub})
    else:
        name=request.POST.get("nname")
        addr=request.POST.get("naddr")

        models.Publish.objects.filter(id=editpub_id).update(name=name,addr=addr)
        return redirect("/publishIndex/")


def log_out(request):
    auth.logout(request)
    return redirect("/login/")

def reg(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        User.objects.create_user(username=username,password=password)
        return redirect("/login/")

    return render(request,"reg.html")