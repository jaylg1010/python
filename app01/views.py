from django.shortcuts import render,HttpResponse
from app01 import models
from django.forms import ModelForm


# Create your views here.


# 登录函数
def login(request):
    username=request.POST.get("username")
    password=request.POST.get("password")

    user=models.UserInfo.objects.filter(username=username,password=password)
    stu=models.Student.objects.filter(username=username,password=password)
    if user:
        questionnaire_list=models.Questionnaire.objects.all()
        return render(request,"Userinfo_Index.html",{"questionnaire_list":questionnaire_list})
    elif stu:
        return render(request,"Student_Index.html")
    else:
        return render(request,"login.html")


# 问题的ModelForm
class Question_Modelform(ModelForm):
    class Meta:
        model=models.Question
        fields = ['caption','type']

# 单选的ModelForm
class Option_Modelform(ModelForm):
    class Meta:
        model=models.Option
        fields = ['name','score']



# # 编辑问卷函数，普通方法使用modelform与列表来返回到前端
# def edit_questionnaire(request,questionnaire_id):
#     # 查找这个问卷是否有问题
#     que_list=models.Question.objects.filter(questionnaire_id=questionnaire_id)
#     if not que_list:
#         form_list=[]
#         form = Question_Modelform()
#         form_list.append(form)
#     else:
#         form_list=[]
#         for que in que_list:
#             form=Question_Modelform(instance=que)
#             form_list.append(form)
#     return render(request,"Edit_Questionnaire.html",{"form_list":form_list})



# # 编辑问卷函数，普通方法使用modelform与yield来返回到前端
# def edit_questionnaire(request,questionnaire_id):
#     # 查找这个问卷是否有问题
#     que_list=models.Question.objects.filter(questionnaire_id=questionnaire_id)
#     def inner():
#         if not que_list:
#             form = Question_Modelform()
#             yield form
#         else:
#             for que in que_list:
#                 form=Question_Modelform(instance=que)
#                 yield form
#     return render(request,"Edit_Questionnaire.html",{"form_list":inner()})



# 编辑问卷函数，普通方法使用modelform与yield来返回到前端,构建字典返回到前端可以添加属性
def edit_questionnaire(request,questionnaire_id):
    # 查找这个问卷是否有问题
    que_list=models.Question.objects.filter(questionnaire_id=questionnaire_id)
    def inner():
        if not que_list:
            form = Question_Modelform()
            yield {"form":form,"obj":None,"option_class":'hide',"options":None}
        else:
            for que in que_list:
                form=Question_Modelform(instance=que)
                temp={"form":form,"obj":que,"option_class":'hide',"options":None}
                if que.type==2:
                    temp['option_class']=''
                    # 获取所有的单选的选项
                    def inner_loop(que):
                        option_list=models.Option.objects.filter(question=que)
                        print("++++++++++++++++++++++",option_list)
                        for option in option_list:
                            yield {"form":Option_Modelform(instance=option),"obj":option}
                    temp["options"]=inner_loop(que)
                yield temp
    return render(request,"Edit_Questionnaire.html",{"form_list":inner()})
