# coding

import hashlib

from django.db import models


# 密码加密
def hash_password(password):
    if isinstance(password, str):
        password = password.encode('utf-8')  # 加密需要比特类型
    
    return hashlib.md5(password).hexdigest().upper()

# 客户端用户
class ClientUser(models.Model):
    username = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    avatar = models.CharField(max_length=500, default='') # 头像
    gender = models.CharField(max_length=10, default='') # 性别
    birthday = models.DateTimeField(null=True, blank=True, default=None)
    status = models.BooleanField(default=True, db_index=True)  # 用户是否可用
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'username:{}'.format(self.username)

    # 创建
    @classmethod
    def add(cls, username, password, avatar='', gender='', birthday=None):
        return cls.object.create(
            username=username,
            password=hash_password(password),
            avatar=avatar,
            gender=gender,
            birthday=birthday,
            status=True,
        )

    # 获取
    def get_user(cls, username, password):
        try:
            user = cls.object.get(
                username=username,
                password=hash_password(password)
            )
            return user
        except:
            return None

    # 更改密码
    def update_password(self, old_password, new_password):
        hash_old_password = hash_password(old_password)

        if hash_old_password != self.password:
            return False
        
        hash_new_password = hash_password(new_password)
        self.password = hash_new_password
        self.save()

        return True

    # 更改当前用户状态
    def update_status(self):
        self.status = not self.status
        self.save()

        return True

    




    
