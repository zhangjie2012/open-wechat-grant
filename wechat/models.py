
from datetime import datetime
from django.db import models


class AuthWechat(models.Model):
    """认证微信信息"""

    # 接口调用凭据
    appid = models.CharField(max_length=32, unique=True)
    access_token = models.CharField(max_length=128)
    refresh_token = models.CharField(max_length=128)
    expire_ts = models.IntegerField('到期时间戳')

    # 账号主体信息
    nick_name = models.CharField('昵称', max_length=64)
    head_img = models.CharField('头像', max_length=256)
    user_name = models.CharField('原始ID', max_length=64)
    principal_name = models.CharField('主体名称', max_length=64)
    qrcode_url = models.CharField('二维码链接', max_length=256)

    grant_dt = models.DateTimeField('授权时间', default=datetime.now)

    class Meta:
        ordering = ('-id', )
