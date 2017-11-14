#_author:"gang"
#date: 2017/11/7

def init_permission(user,request):
    """
    获得用户登录的url权限
    把权限加到session中
    :param user:
    :param request:
    :return:
    """
    permission_list=user.roles.values("permission__title","permission__url","permission__is_menu")
    print("{{{{{{{{{{}}}}}}}}}}}",permission_list)

    url_list=[]
    for item in permission_list:
        url_list.append(item["permission__url"])

    print("+_+_+_+_+_+_+_+_+_+_+_+_",url_list)
    request.session["permission_url_list"]=url_list