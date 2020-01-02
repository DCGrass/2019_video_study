# coding:utf-8

from django.views.generic import View
from django.shortcuts import redirect, reverse
from django.contrib.auth import login, authenticate, logout  # 登陆、认证
from django.contrib.auth.models import User
from django.core.paginator import Paginator  # 分页
from app.libs.base_render import render_to_response # mako的render
from app.utils.permission import dashboard_auth  # 登陆验证装饰器

# 登陆
class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        
        # 如果已经登陆 跳转首页 dir(request.user)
        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))
            
        to = request.GET.get('to', '')
        
        
        data = {'error': '', 'to': to}
        
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        to = request.GET.get('to', '')

        data = {}

        # 看是否存在符合的对象
        exists = User.objects.filter(username=username).exists()
        data['error'] = '没有该用户~'

        if not exists:
            return render_to_response(request, self.TEMPLATE, data=data)

        # 认证 认证失败=> user值为None
        user = authenticate(username=username, password=password)

        if not user:
            data['error'] = '密码错误~'
            return render_to_response(request, self.TEMPLATE, data=data)
        
        # 是否是管理员
        if not user.is_superuser:
            data['error'] = '你无权登陆~'
            return render_to_response(request, self.TEMPLATE, data=data)

        # 登陆
        login(request, user)
        
        if to:
            return redirect(to)

        return redirect(reverse('dashboard_index'))


# 注销
class Logout(View):

    def get(self,request):
        logout(request)

        return redirect(reverse('dashboard_login'))

      
# 管理员
class AdminManager(View):
    TEMPLATE = 'dashboard/auth/admin.html'

    @dashboard_auth
    def get(self, request):
        
        data = {}

        # users = User.objects.filter(is_superuser=True)
        users = User.objects.all()
        # print(users) # <QuerySet [<User: admin>]>
        # data['users'] = users

        page = request.GET.get('page', 1) 
        p = Paginator(users, 1)  # 默认每页两个
        totol_page = p.num_pages  # 总页数
        if int(page) <= 1:
            page = 1
    
        current_page = p.get_page(int(page))  # 当前页码
        current_page_obj = current_page.object_list  # 当前页有哪些对象

        data = {
            'users': current_page_obj, 
            'total': totol_page,
            'current_page': int(page)
        }

        return render_to_response(request, self.TEMPLATE, data=data)


# 更新管理员状态
class UpdateAdminStatus(View):

    def get(self, request):

        status = request.GET.get('status', 'on')

        # print('status:', status)
        _status = True if status == "on" else False
        request.user.is_superuser = _status  # request.user指的是当前登陆的用户
        user_id = request.GET.get('user_id','')
        # print('user_id:', user_id)

        # print(request.user.id)
        user = User.objects.filter(id=user_id).exclude(id=request.user.id)
        # print('user',user)
        user.update(is_superuser=_status)
        # request.user.save()  # 在这里,数据库中实际修改的是当前登陆用户的user对象的管理员状态

        return redirect(reverse('admin_manager'))





        

        