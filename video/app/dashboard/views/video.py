from django.views.generic import View
from django.shortcuts import redirect, reverse
from app.libs.base_render import render_to_response 
from app.utils.permission import dashboard_auth  # 登陆验证装饰器

from app.model.video import (
    VideoType, FromType, NationalityType, IdentityType, Video, VideoSub, VideoStar)
from app.utils.common import check_and_get_video_type


# 第三方外链
class ExternalVideo(View):
    TEMPLATE = 'dashboard/video/external_video.html'

    @dashboard_auth
    def get(self, request):

        error = request.GET.get('error', '')
        data = {'error': error}

        # 拿到video信息(排除是自制的)
        data['videos'] = Video.objects.exclude(from_to=FromType.custom.value)

        return render_to_response(request, self.TEMPLATE,data=data)
        
    def post(self,request):
        name = request.POST.get('name')
        image = request.POST.get('image')
        video_type = request.POST.get('video_type')
        from_to = request.POST.get('from_to')
        nationality = request.POST.get('nationality')
        info = request.POST.get('info')

        if not all([name, image, video_type, from_to, nationality,info]):
            return redirect('{}?error={}'.format(reverse('external_video'), '创建失败~缺少必要字段'))
            
        # result  =>  {'code': 0, 'msg': 'success', 'data': <VideoType.movie: 'movie'>}
        result = check_and_get_video_type(VideoType, video_type, '非法的视频类型')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result['msg']))

        result = check_and_get_video_type(FromType, from_to, '非法的视频来源')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result['msg']))

        result = check_and_get_video_type(NationalityType, nationality, '非法的国籍')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result['msg']))
        
        Video.objects.create(
            name=name,
            image=image,
            video_type=video_type,
            from_to=from_to,
            nationality=nationality,
            info=info,
        )
        return redirect(reverse('external_video'))


# video的附属信息(播放地址和集数附表)
class VideoSubView(View):
    TEMPLATE = 'dashboard/video/video_sub.html'

    @dashboard_auth
    def get(self, request, video_id):
        # 需要一个video_id指明附属信息来自哪里
        data = {}

        video = Video.objects.get(pk=video_id)
        error = request.GET.get('error', '')
        
        data['video'] = video
        data['error'] = error
    
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request, video_id):
        url = request.POST.get('url')
        # print(url,video_id) # https://www.baidu.com/  1
        video = Video.objects.get(pk=video_id)

        # video_sub = VideoSub.objects.filter(video=video)  # video_sub => <QuerySet []>
        # 可以直接拿 在外键的设置的时候 related_name='video_sub'
        number = video.video_sub.count() + 1 # 集数取决于它的长度 
        
        try:
            VideoSub.objects.create(video=video, url=url, number=number)
        except:
            return 
        
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))
        

class VideoStarView(View):

    def post(self, request):
        name = request.POST.get('name')
        identity = request.POST.get('identity')
        video_id = request.POST.get('video_id')
        print(name, identity, video_id)

        path_format = '{}'.format(reverse('video_sub', kwargs={'video_id': video_id}))
        if not all([name, identity, video_id]):
            return redirect('{}?error={}'.format(path_format,'缺少必要字段'))

        result = check_and_get_video_type(IdentityType, identity, '非法身份')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(path_format, result['msg']))      

        video = Video.objects.get(pk=video_id)

        try:
            VideoStar.objects.create(
                video=video,
                name=name,
                identity=identity
            )
        except:
            return redirect('{}?error={}'.format(path_format, '创建失败'))
            
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))        
                
class StarDelete(View):

    def get(self, request, star_id, video_id):
        
        VideoStar.objects.filter(id=star_id).delete()

        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))          
