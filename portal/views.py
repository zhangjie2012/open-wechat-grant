
import config
import requests
import json

from urllib.parse import urljoin

from django.shortcuts import render
from django.shortcuts import reverse

from utils.global_store import global_store
from utils.logger import logger

from wechat.models import AuthWechat


def get_pre_auth_code():
    """获取预授权码"""
    token = global_store.get_component_access_token()
    if not token:
        logger.warning('令牌不存在')
        return None

    code = global_store.get_pre_auth_code()
    if not code:
        api = 'https://api.weixin.qq.com/cgi-bin/component/api_create_preauthcode?' \
              'component_access_token={0}'.format(token)
        data = {'component_appid': config.AppID}
        resp = requests.post(api, data=json.dumps(data), timeout=1)
        resp_data = json.loads(resp.text)

        code = resp_data['pre_auth_code']
        ex = int(resp_data['expires_in'])
        global_store.set_pre_auth_code(code, ex)

        logger.info('更新pre_auth_code|%s|%d', code, ex)

    return code


def auth(request):
    """微信公众号管理员认证"""

    pre_auth_code = get_pre_auth_code()
    if pre_auth_code:
        redirect_uri = urljoin('http://'+config.DOMAIN_NAME, reverse('wechat:grant'))
        auth_url = 'https://mp.weixin.qq.com/cgi-bin/componentloginpage?' \
                   'component_appid={0}&' \
                   'pre_auth_code={1}&' \
                   'redirect_uri={2}&' \
                   'auth_type={3}'.format(
                       config.AppID,
                       pre_auth_code,
                       redirect_uri,
                       1  # auth_type = 1 仅允许公众号
                   )
    else:  # 测试环境才可能出现为空的情况
        auth_url = ''

    auth_wechat_qs = AuthWechat.objects.all()

    return render(request, 'portal/auth.html', {
        'auth_url': auth_url,
        'auth_wechat_qs': auth_wechat_qs
    })
