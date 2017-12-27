# Description: WXBizMsgCrypt 使用demo文件

from utilities.crypto.WXBizMsgCrypt import WXBizMsgCrypt
from xml.dom import minidom
if __name__ == "__main__":
    """ 
    1.第三方回复加密消息给公众平台；
    2.第三方收到公众平台发送的消息，验证消息的安全性，并对消息进行解密。
    """
    # encodingAESKey = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFG"
    # to_xml = """ <xml><ToUserName><![CDATA[oia2TjjewbmiOUlr6X-1crbLOvLw]]></ToUserName><FromUserName><![CDATA[gh_7f083739789a]]></FromUserName><CreateTime>1407743423</CreateTime><MsgType>  <![CDATA[video]]></MsgType><Video><MediaId><![CDATA[eYJ1MbwPRJtOvIEabaxHs7TX2D-HV71s79GUxqdUkjm6Gs2Ed1KF3ulAOA9H1xG0]]></MediaId><Title><![CDATA[testCallBackReplyVideo]]></Title><Descript  ion><![CDATA[testCallBackReplyVideo]]></Description></Video></xml>"""
    # token = "spamtest"
    # nonce = "1320562132"
    # appid = "wx2c2769f8efd9abc2"


    # # 测试加密接口
    # encryp_test = WXBizMsgCrypt(token, encodingAESKey, appid)
    # ret, encrypt_xml = encryp_test.encrypt_msg(to_xml, nonce)
    # print(ret, encrypt_xml)

    # 测试解密接口
    # timestamp = "1409735669"
    # msg_sign = "5d197aaffba7e9b25a30732f161a50dee96bd5fa"
    # from_xml = """<xml><ToUserName><![CDATA[gh_10f6c3c3ac5a]]></ToUserName><FromUserName><![CDATA[oyORnuP8q7ou2gfYjqLzSIWZf0rs]]></FromUserName><CreateTime>1409735668</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[abcdteT]]></Content><MsgId>6054768590064713728</MsgId><Encrypt><![CDATA[hyzAe4OzmOMbd6TvGdIOO6uBmdJoD0Fk53REIHvxYtJlE2B655HuD0m8KUePWB3+LrPXo87wzQ1QLvbeUgmBM4x6F8PGHQHFVAFmOD2LdJF9FrXpbUAh0B5GIItb52sn896wVsMSHGuPE328HnRGBcrS7C41IzDWyWNlZkyyXwon8T332jisa+h6tEDYsVticbSnyU8dKOIbgU6ux5VTjg3yt+WGzjlpKn6NPhRjpA912xMezR4kw6KWwMrCVKSVCZciVGCgavjIQ6X8tCOp3yZbGpy0VxpAe+77TszTfRd5RJSVO/HTnifJpXgCSUdUue1v6h0EIBYYI1BD1DlD+C0CR8e6OewpusjZ4uBl9FyJvnhvQl+q5rv1ixrcpCumEPo5MJSgM9ehVsNPfUM669WuMyVWQLCzpu9GhglF2PE=]]></Encrypt></xml>"""

    """wechat的信息"""
    appid = 'wxedfe0fd7629d9600'
    token = 'wechat_open'
    encodingAESKey = '86dnr62NFVYizgkWypLPY7m9g4mq3akxXDLMbSrw6bj'

    msg_sign = '637895a7100f656d45cecb1651913b795cc332c0'
    timestamp = '1503996469'
    nonce = '534906537'
    from_xml = """<xml>
    <AppId><![CDATA[wxedfe0fd7629d9600]]></AppId>
    <Encrypt><![CDATA[40SGEugL+8fwmHmP0ySsWDS30qHAnhcareT2nQVa/QXYOPK3GabbIFdbKmFiI5fX4Wu3vUht625UkDKClVJWlzw3YFfcbGsTKw3rKU3N6gujWDHemyAtKMGbcOrwEF3Cvirs6RpkXCZAlb851p9naAZpet1kcksgUcgvSau/6si+9H7aGhX52WUn3SGuCXwYlik0Mbux2xzk+UxiJS+RYErZvK8TVvibBzpsV1gv+/Ci3EejucYVVSjH+B+v4a2IHbaRoIFtX/oKlM5971/YvIC28RDhsW2MYjs0LaLM93eJ5puLUfJC7goC/UDHHmY+hifJmhqlYxndUUNLAMEZ1wKmxNcWofTMVyL0D/dCi5M1lY20tkUjsYh0JxDOgXW0NvSxR5Qcnk9ADRfiOD4IC3+3B9fvaisU/yPuZap3WW4nmooRSpYRwiQVWuuj2gSNtoD0bm/7ONCdAN+VCQTQFQ==]]></Encrypt>
</xml>"""
    decrypt_test = WXBizMsgCrypt(token, encodingAESKey, appid)
    ret, decryp_xml = decrypt_test.decrypt_msg(from_xml, msg_sign, timestamp, nonce)
    # print(ret, decryp_xml)

    decryp_xml = decryp_xml.decode()
    dom = minidom.parseString(decryp_xml)
    print(decryp_xml)
    cvt_node = dom.getElementsByTagName('ComponentVerifyTicket')[0].firstChild.wholeText

    print(cvt_node)
