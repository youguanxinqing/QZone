PHOTOMJS_DIR = r"D:\phantomjs-2.1.1-windows\bin\chromedriver.exe"
QQUSER = "578******"
QQPASSWORD = "**********"

# 获取QQ空间说说接口
WORDS_API = "https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6"
# 我的QQ空间主页
MY_MAIN_URL = "https://user.qzone.qq.com/578******/infocenter"
# QQ空间登陆地址
LOGIN_URL = "https://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=https%3A//qzs.qq.com/qzone/v6/portal/proxy.html&daid=5&&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=22&target=self&s_url=https%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&pt_qr_app=手机QQ空间&pt_qr_link=https%3A//z.qzone.com/download.html&self_regurl=https%3A//qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=https%3A//z.qzone.com/download.html&pt_no_auth=0"


# 获取QQ空间说说的参数
WORDS_REQUESTS_PARAMS = {
        "uin": "159******509",
        "inCharset": "utf-8",
        "outCharset": "utf-8",
        "hostUin": "159******509",
        "notice": "0",
        "sort": "0",
        "pos": "",
        "num": "20",
        "cgi_host": "http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6",
        "code_version": "1",
        "format": "jsonp",
        "need_private_comment": "1",
        "g_tk": "",
        "qzonetoken": ""
}

# 申请头
HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "user.qzone.qq.com",
        #"If-Modified-Since": "Sun, 24 Jun 2018 01:07:59 GMT",
        "Referer": "https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
}

# 存储申请失败的参数
FAILURE = []
