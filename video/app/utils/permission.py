# cofing:utf-8

# permission.py 专门用作验证

import functools

from django.shortcuts import redirect, reverse

# 这里的装饰器主要用于后台用户验证
def dashboard_auth(func):

    @functools.wraps(func)
    def wrapper(self, request, *args, **kwargs):
        
        user = request.user
        # 如果它没有登陆或者它不是超级管理员 就将其移交登录页并在完成登陆后跳转回之前想要的页面
        # 否则让其执行函数
        if not user.is_authenticated or not user.is_superuser:
            return redirect('{}?to={}'.format(reverse('dashboard_login'), request.path))

        return func(self, request, *args, **kwargs)

    return wrapper



            





