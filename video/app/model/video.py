# coding:utf-8

from enum import Enum
from django.db import models


# 类型
class VideoType(Enum):
    movie = 'movie' # 电影
    cartoon = 'cartoon' # 动漫
    episode = 'episode'  # 剧集
    variety = 'variety'  # 综艺
    other = 'other'

VideoType.movie.label = '电影'
VideoType.cartoon.label = '动漫'
VideoType.episode.label = '剧集'
VideoType.variety.label = '综艺'
VideoType.other.label = '其它'


# 来源
class FromType(Enum):
    youku = 'youku'  # 优酷
    aiqiyi = 'aiqiyi' # 爱奇艺
    bili = 'bili' # b站
    custom = 'custom'  # 自定义

FromType.youku.label = '优酷'
FromType.aiqiyi.label = '爱奇艺'
FromType.bili.label = '哔哩哔哩'
FromType.custom.label = '自制'


# 国籍
class NationalityType(Enum):
    china = 'china'
    japan = 'japan'
    korea = 'korea'
    america = 'america'
    other = 'other'

NationalityType.china.label = '中国'
NationalityType.japan.label = '日本'
NationalityType.korea.label = '韩国'
NationalityType.america.label = '美国'
NationalityType.other.label = '未知'


# 演员身份
class IdentityType(Enum):
    to_str = 'to_str'
    supporting_rule = 'supporting_rule'
    director = 'director'

IdentityType.to_str.label = '主演'
IdentityType.supporting_rule.label = '配角'
IdentityType.director.label = '导演'


class Video(models.Model):
    name = models.CharField(max_length=100, null=False)
    image = models.CharField(max_length=500, default='')  # 海报
    video_type = models.CharField(max_length=50, default=VideoType.other.value)  # 类型
    from_to = models.CharField(max_length=20, null=False, default=FromType.custom.value)
    nationality = models.CharField(max_length=20, default=NationalityType.other.value)  # 国籍
    info = models.TextField()  # 视频描述
    status = models.BooleanField(default=True, db_index=True)  # 视频是否可用
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        # 联合索引
        unique_together = ('name', 'video_type', 'from_to', 'nationality')

    def __str__(self):
        return self.name


# 演员附表
class VideoStar(models.Model):
    video = models.ForeignKey(Video, related_name='video_star', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, null=False)  # 姓名
    identity = models.CharField(max_length=50, default='')  # 身份(主演/配角/导演...)
    
    class Meta:
        unique_together = ('video', 'name', 'identity')
        
    def __str__(self):
        return self.name


# 播放地址和集数附表
class VideoSub(models.Model):
    video = models.ForeignKey(Video, related_name='video_sub', on_delete=models.SET_NULL, blank=True, null=True)
    url = models.CharField(max_length=500, null=False)  # 播放地址
    number = models.IntegerField(default=1)  # 集数
    
    class Meta:
        unique_together = ('video', 'number')

        def __str__(self):
            return 'video:{},number:{}'.format(self.video.name, self.number)
