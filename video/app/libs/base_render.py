# coding:utf-8

# base_render.py：对mako模板的定义 mako模板初始化
# mako中的上下文指的主要是渲染模板所需要的信息

from mako.lookup import TemplateLookup # 引入mako的一些配置文件
from django.template import RequestContext # 请求上下文
from django.conf import settings
from django.template.context import Context
from django.http import HttpResponse  # 返回一些字符串的内容

# 仿照django render的模板写进来的 data是一些字典数据 
def render_to_response(request, template, data=None):
    context_instance = RequestContext(request)  # 定义上下文的实例
    path = settings.TEMPLATES[0]['DIRS'][0]  # 引入模板的位置，即从setting中拿到template的地址

    lookup = TemplateLookup(
        directories=[path],  # 将path注册到mako中
        output_encoding='utf-8', # 输出的格式
        input_encoding = 'utf-8', # 输入的格式
    )

    mako_template = lookup.get_template(template)  # 将template注册进mako中

    if not data:
        data = {}

    # 判断当前实例是否存在 存在将数据加入上下文的实例
    # 如果实例不存在(即上下文不存在) 我们就自己创建 并将数据加进去
    if context_instance:
        context_instance.update(data) # update(data) data不能为None 可以为一个字典
    else:
        context_instance = Context(data)

    result = {} # result是我们最终要传过去的数据

    # context_instance实例上下文是一个字典 
    for d in context_instance:
        result.update(d)
 
    result['request'] = request

    # csrf_token跨域请求的验证 使用mako模板后这个验证在前端就消失了
    # 我们需要在render里创建这个csrf_token关键词 很重要
    result['csrf_token'] = '<input type="hidden" name="csrfmiddlewaretoken" value="{0}" >'.format(request.META['CSRF_COOKIE'])
    
    return HttpResponse(mako_template.render(**result))
