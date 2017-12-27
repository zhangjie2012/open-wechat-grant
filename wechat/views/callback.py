
import time
import requests
import json
import config

from xml.dom import minidom
from django.http import HttpResponse

from utils.logger import logger
from utils.crypto.WXBizMsgCrypt import WXBizMsgCrypt
from utils.global_store import global_store

from wechat.models import AuthWechat


def _get_cdata(dom, tag_name):
    """获取 xml CDATA值
    `![CDATA[xxxxxx]]`
    """
    content = dom.getElementsByTagName(tag_name)[0].firstChild.wholeText
    return content


def auth(request):
    """第三方平台授权事件接收URL
    1. 微信服务器会每10分钟定时推送 component_verify_ticket
    2. 收到 ticket 推送后需要对数据进行解密
    3. 必须返回 success 字符串
    """
    try:
        timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
        msg_sign = request.GET['msg_signature']
        crypt_xml = request.body.decode('utf-8')
    except (KeyError, ValueError, TypeError):
        logger.warning('无效的调用|%s', request.GET)
        return HttpResponse('error')  # anything, whatever

    decrypt = WXBizMsgCrypt(config.Token, config.EncodingAESKey, config.AppID)
    ret, decrypt_xml_bytes = decrypt.decrypt_msg(
        crypt_xml, msg_sign, timestamp, nonce)
    if ret != 0:
        logger.warning('解密失败|%s|%s', ret, crypt_xml)
        return HttpResponse('error')

    # 解密之后格式：
    # <xml>
    # <AppId> </AppId>
    # <CreateTime>1413192605 </CreateTime>
    # <InfoType> </InfoType>
    # <ComponentVerifyTicket> </ComponentVerifyTicket>
    # </xml>
    decrypt_xml = decrypt_xml_bytes.decode()
    logger.debug('收到微信授权回调|%s', decrypt_xml)

    dom = minidom.parseString(decrypt_xml)
    info_type = _get_cdata(dom, 'InfoType')
    if info_type == 'component_verify_ticket':
        component_verify_ticket = _get_cdata(dom, 'ComponentVerifyTicket')
        logger.info('更新component_verify_ticket|%s', component_verify_ticket)
        global_store.set_component_verify_ticket(component_verify_ticket)
    else:
        logger.debug('未处理的类型|%s', info_type)

    return HttpResponse('success')


def grant(request):
    """微信公众号授权回调
    """
    try:
        auth_code = request.GET['auth_code']
        ex = int(request.GET['expires_in'])
    except (KeyError, ValueError, TypeError):
        logger.warning('无效的调用|%s', request.GET)
        return HttpResponse('error')

    logger.info('公众号授权回调|%s|%f', auth_code, ex)

    component_access_token = global_store.get_component_access_token()
    if not component_access_token:
        logger.error('没有component_access_token')
        return HttpResponse('error')

    # 1. 通过 auth_code 获取公众号 `接口调用凭据`

    api = 'https://api.weixin.qq.com/cgi-bin/component/api_query_auth?' \
          'component_access_token={0}'.format(component_access_token)
    data = {
        'component_appid': config.AppID,
        'authorization_code': auth_code,
    }
    resp = requests.post(api, data=json.dumps(data), timeout=1)
    resp_data = json.loads(resp.text)

    auth_info = resp_data['authorization_info']
    auth_appid = auth_info['authorizer_appid']
    auth_access_token = auth_info['authorizer_access_token']
    auth_refresh_token = auth_info['authorizer_refresh_token']
    auth_ex = int(auth_info['expires_in'])

    logger.info('获得公众号调用接口凭据|%s', auth_appid)

    # 2. 获取授权方的帐号基本信息：
    # 头像、昵称、帐号类型、认证类型、微信号、原始ID和二维码图片URL

    api = 'https://api.weixin.qq.com/cgi-bin/component/api_get_authorizer_info?' \
          'component_access_token={0}'.format(component_access_token)
    data = {
        'component_appid': config.AppID,
        'authorizer_appid': auth_appid
    }
    resp = requests.post(api, data=json.dumps(data), timeout=1)
    resp_data = json.loads(resp.text)

    auth_info = resp_data['authorizer_info']
    nick_name = auth_info['nick_name']
    head_img = auth_info['head_img']
    service_type_info = int(auth_info['service_type_info']['id'])  # 2 表示服务号
    user_name = auth_info['user_name']
    principal_name = auth_info['principal_name']
    qrcode_url = auth_info['qrcode_url']

    logger.info('获得授权方账号信息|%s|%s', nick_name, principal_name)
    if service_type_info != 2:
        logger.error('接入的公众号不是服务号|%s|%s', nick_name, principal_name)
        return HttpResponse('授权失败：请确认您的微信公众号类型为服务号')

    # 3. 接入公众号到本服务器
    # 如果已经接入的公众号，则更新基本信息（为了解决授权码没有及时更新全部失效）

    # 提前 11 分钟过期
    expire_ts = int(time.time()) + auth_ex - 11 * 60
    auth_wechat, created = AuthWechat.objects.update_or_create(
        appid=auth_appid,
        defaults={
            'access_token': auth_access_token,
            'refresh_token': auth_refresh_token,
            'expire_ts': expire_ts,

            'nick_name': nick_name,
            'head_img': head_img,
            'user_name': user_name,
            'principal_name': principal_name,
            'qrcode_url': qrcode_url,
        }
    )
    if created:
        logger.info('授权接入微信公众号|%s|%s', nick_name, principal_name)
    else:
        logger.info('更新授权接入微信公众号|%s|%s', nick_name, principal_name)

    # 4. 接入成功之后，清空预授权码
    # 一个预授权码只能被一个微信公众号接入
    global_store.delete_pre_auth_code()

    return HttpResponse('恭喜您，授权成功')
