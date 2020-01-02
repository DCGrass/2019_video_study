# coding:utf-8

# 验证视频等的类型
# eg: VideoType('movie') ==>  <VideoType.movie: 'movie'>
def check_and_get_video_type(type_obj, type_value, message):
    try:
        type_obj(type_value)
    except:
        return {'code': -1, 'msg': message}

    # return {'code': 0, 'msg': 'success', 'data': final_type_obj}
    return {'code': 0, 'msg': 'success'}

    