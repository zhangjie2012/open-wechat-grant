
import time
import json
import config

import requests

from django.http import HttpResponse

from utils.logger import logger
from utils.global_store import global_store

from wechat.models import AuthWechat


def update_component_token(request):
    """定时更新 component_access_token
    2小时有效期
    定时间隔：10分钟，触发更新
    """
    api = 'https://api.weixin.qq.com/cgi-bin/component/api_component_token'

    ttl = global_store.ttl_component_access_token()
    if ttl > 11 * 60:
        # 无需更新：11 而不是 10 是为了有一次失败容错
        logger.debug('无需更新 component_token|%d', ttl)
        return HttpResponse('无需更新 component_token')

    ticket = global_store.get_component_verify_ticket()
    if not ticket:
        logger.warning('component_verify_ticket不存在')
        return HttpResponse('component_verify_ticket不存在')

    data = {
        'component_appid': config.AppID,
        'component_appsecret': config.AppSecret,
        'component_verify_ticket': ticket
    }
    resp = requests.post(api, data=json.dumps(data), timeout=2)
    resp_data = json.loads(resp.text)

    token = resp_data['component_access_token']
    ex = int(resp_data['expires_in'])
    global_store.set_component_access_token(token, ex)

    logger.info('更新component_access_token|%s|%d', token, ex)

    return HttpResponse('success')


def update_auth_access_token(request):
    """定时更新微信公众号令牌
    2小时有效期
    定时间隔：10分钟，触发更新
    """
    timestamp = int(time.time())
    component_access_token = global_store.get_component_access_token()
    if not component_access_token:
        logger.error('component_access_token不存在')
        return HttpResponse('component_access_token不存在')

    api = 'https://api.weixin.qq.com/cgi-bin/component/api_authorizer_token?' \
          'component_access_token={0}'.format(component_access_token)

    auth_wechat_qs = AuthWechat.objects.filter(expire_ts__lte=timestamp)
    for auth_wechat in auth_wechat_qs:
        try:
            data = {
                'component_appid': config.AppID,
                'authorizer_appid': auth_wechat.appid,
                'authorizer_refresh_token': auth_wechat.refresh_token,
            }
            resp = requests.post(api, data=json.dumps(data), timeout=2)
            resp_data = json.loads(resp.text)

            access_token = resp_data['authorizer_access_token']
            refresh_token = resp_data['authorizer_refresh_token']
            ex = int(resp_data['expires_in'])
            expire_ts = timestamp + ex - 11 * 60

            auth_wechat.access_token = access_token
            auth_wechat.refresh_token = refresh_token
            auth_wechat.expire_ts = expire_ts
            auth_wechat.save()

            logger.info('更新公众号令牌成功|%s', auth_wechat.principal_name)
        except Exception as e:  # 一次请求失败不能影响其它更新
            logger.warning('更新公众号令牌失败|%s|%s', auth_wechat.principal_name, e)

    logger.debug('更新微信公众号令牌|%d', auth_wechat_qs.count())

    return HttpResponse('success')
