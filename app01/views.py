from django.shortcuts import render,HttpResponse
from app01 import models
from django.forms import ModelForm
from django.http import JsonResponse

import json
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
    if request.method=="GET":
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
                            # print("++++++++++++++++++++++",option_list)
                            for option in option_list:
                                yield {"form":Option_Modelform(instance=option),"obj":option}
                        temp["options"]=inner_loop(que)
                    yield temp
        return render(request,"Edit_Questionnaire.html",{"form_list":inner()})
    elif request.method=="POST":
        ret={"status":True,"msg":None,"data":None}
        try:
            data = json.loads(request.body.decode("utf-8"))
            print(data)

            # 从数据库中取到所有的问题的ID
            question_list=models.Question.objects.filter(questionnaire_id=questionnaire_id).all()
            question_id_list=[question_obj.id for question_obj in question_list]

            # 取到数据中的所有的问题ID
            post_id_list=[int(post_obj.get("pid")) for post_obj in data if post_obj.get("pid")]

            # 取得数据中与数据库中的差集，数据库中有，数据没有删除；数据库没有，数据有新增；都有的更新
            del_question_id=set(question_id_list)-set(post_id_list)
            for id in del_question_id:
                models.Question.objects.filter(id=id).delete()
                models.Option.objects.filter(question_id=id).delete()

            # 循环数据中的数据ID，如果为空则新增
            for item_obj in data:
                if not item_obj.get("pid"):
                    new_question_obj=models.Question.objects.create(caption=item_obj["title"],type=int(item_obj["type"]),questionnaire_id=questionnaire_id)
                    if int(item_obj["type"]) == 2:
                        for option_dic in item_obj["options"]:
                            models.Option.objects.create(name=option_dic["title"],score=int(option_dic["val"]),question=new_question_obj)

                # 如果在数据库中，就更新
                elif int(item_obj.get("pid")) in question_id_list:
                    print("这是要更新的问题的ID",int(item_obj.get("pid")))
                    models.Question.objects.filter(id=int(item_obj.get("pid"))).update(caption=item_obj.get("title"),type=item_obj.get("type"))
                    if not item_obj.get("options"):
                        models.Option.objects.filter(question_id=int(item_obj.get("pid"))).delete()
                    else:
                        models.Option.objects.filter(question_id=int(item_obj.get("pid"))).delete()
                        for option_dic in item_obj.get("options"):
                            models.Option.objects.create(name=option_dic["title"],score=int(option_dic["val"]),question_id=int(item_obj.get("pid")))
        except Exception as e:
            ret["msg"]=e
            ret["status"]=False
        return JsonResponse(ret)

"""
id=[1,2,3]
data=[
    {'pid': '1', 'title': '最近对自己的学习状态打多少分', 'type': '1', 'options': []},
    {'pid': '2', 'title': '自己对编程是否有兴趣', 'type': '2', 'options': [
        {'id': '4', 'title': '有', 'val': '10'},
        {'id': '5', 'title': '没有', 'val': '30'},
        {'id': '6', 'title': '根本没有', 'val': '100'}
    ]},
    {'pid': '3', 'title': '对自己最近的学习评价', 'type': '3', 'options': []},
    {'pid': '', 'title': '鲁刚帅不帅？', 'type': '2', 'options': [
        {'id': '', 'title': '帅', 'val': '100'},
        {'id': '', 'title': '不帅', 'val': '1000'}]
     }
]
"""