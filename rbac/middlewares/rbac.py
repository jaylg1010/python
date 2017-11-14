#_author:"gang"
#date: 2017/11/7
import re

from django.shortcuts import redirect,render,HttpResponse
from django.conf import settings

"""
设置中间件
设置白名单，限制谁可以不用验证session，可以直接过去
并且匹配URL权限
"""

class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

class RbacMiddleware(MiddlewareMixin):
    def process_request(self,request):
        current_url=request.path_info
        # print("+++++++++++++++",current_url)

        for url in settings.VALID_URL:
            if re.match(url,current_url):
                return None

        permision_list=request.session.get("permission_url_list")

        print("________________________",permision_list)
        if not permision_list:
            return redirect("/login/")

        flag=False
        for db_url in permision_list:
            regax="^{0}$".format(db_url)
            print("||||||||||||||||||||||||",regax)
            if re.match(regax,current_url):
                flag=True
                break

        if not flag:
            return HttpResponse("无权访问")