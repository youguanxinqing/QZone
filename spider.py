import re
import time
import json
import requests
import pymongo
from CONFIG import *
from QQLogin import login


# 连接数据库，选择数据库，选择集合
client = pymongo.MongoClient("localhost", 27017)
db = client.qqzone
yaner = db.yaner


def get_gtk(cookie):
    """
    获取QQ空间GTK算法
    :param cookie:
    :return:
    """
    hashes = 5381
    for letter in cookie['p_skey']:
        hashes += (hashes << 5) + ord(letter)
    return hashes & 0x7fffffff

def get_qzonetoken(url, cookies):
    """
    获取QQ空间qzonetoken值
    :param url:
    :param cookies:
    :return:
    """
    try:
        response = requests.get(url=url, headers=HEADERS, cookies=cookies)
        response.encoding = "utf-8"
        response.raise_for_status()
    except requests.HTTPError:
        return None

    # 利用正则提取qzonetoken值
    qzonetoken = re.search(\
        r'window\.g_qzonetoken = \(function\(\)\{ try\{return \"(\w+)\";\}', \
        response.text).group(1)

    return qzonetoken

def get_words(url, params, cookies, tries=3):
    """
    获取女神说说
    :param url:
    :param params:
    :param cookies:
    :param tries:
    :return:
    """
    try:
        response = requests.get(url=url, headers=HEADERS, params=params, cookies=cookies)
        response.raise_for_status()
        response.encoding = "utf-8"
    except requests.HTTPError:
        # 如果请求失败三次，加入FAILURE列表中
        if tries<1:
            get_words(url, params, cookies, tries-1)
        else:
            FAILURE.append(params["pos"])
            return None

    # 成功则返回数据
    return response.text

def parse_data(data):
    """
    提取数据
    :param data:
    :return:
    """
    # 取出JSON格式的字符串
    content = re.search(r"_Callback\((.+)\)", data).group(1)
    # print(content)
    # 转换成字典，并定义一个字典用来存放数据
    data = json.loads(content)
    dic = {}
    # 如果msglist存在，值不为“null”，那么提取数据
    if "msglist" in data.keys() and data["msglist"]!="null":
        for item in data["msglist"]:
            pics = []
            videos = []

            # 如果说说为空，用内“null”填充，否之则取出
            if not item["content"]:
                dic["content"] = "null"
            else:
                dic["content"] = item["content"]

            # 用时间戳设置_id字段
            dic["_id"] = item["created_time"]
            # 将时间戳转换“某年-某月-某日 时：分：秒”格式
            dic["time"] = time.strftime("%Y-%m-%d %H:%M:%S", \
                            time.localtime(int(item["created_time"])))

            # 如果照片存在，如果视频存在，取出，否则用“null”填充
            if "pic" in item.keys():
                for picture in item["pic"]:
                    pics.append(picture["url3"])
                dic["picture"] = pics
            else:
                dic["picture"] = "null"

            if "video" in item.keys():
                for video in item["video"]:
                    videos.append(video["url3"])
                dic["video"] = videos
            else:
                dic["video"] = "null"

            yield dic

    # 这个else主要针对msglist="null"的情况，如果连续三次出现
    # 这种情况，说明女生的说说都爬完了
    else:
        return None


def save_mongodb(item):
    """
    写入mongodb，并且打印成功提示
    :param item:
    :return:
    """
    yaner.insert(item)
    print("插入成功",item)


def main():

    cookies = login(LOGIN_URL)
    if not cookies:
        print("获取cookies值失败")
        return

    gtk = get_gtk(cookies)
    qzonetoken = get_qzonetoken(MY_MAIN_URL, cookies)
    if not gtk or not qzonetoken:
        print("获取gtk或这qzonetoken失败")
        return

    # WORDS_REQUESTS_PARAMS["uin"]
    # WORDS_REQUESTS_PARAMS["hostUin"]
    # 如果需要爬去自家女神的说说，需要用QQ账号，填充上面的值
    WORDS_REQUESTS_PARAMS["g_tk"] = gtk
    WORDS_REQUESTS_PARAMS["qzonetoken"] = qzonetoken

    count = 0
    # 每次请求20条数据，pos每次增加20
    for pos in range(0, 100000, 20):
        time.sleep(3)
        # 实现翻页功能
        WORDS_REQUESTS_PARAMS["pos"] = pos
        wordsData = get_words(WORDS_API, WORDS_REQUESTS_PARAMS, cookies)
        if not wordsData:
            print("获取女神说说失败")
            return
        try:
            for item in parse_data(wordsData):
                save_mongodb(item)
            count = 0
        except TypeError:
            count += 1
            # 如果连续三次没有拿到数据，说明已经爬完
            if count >3:
                break
            else:
                continue

    # 断开MongoDB的连接，并且打印请求失败的连接
    client.close()
    print(FAILURE)
    print("结束")


if __name__ == "__main__":
    main()