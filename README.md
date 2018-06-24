# QZone
爬取心仪女生的QQ空间说说。自动登陆QQ获取cookies.

##目标
爬去男/女神QQ空间里的说说。但我女神的说说是没办法爬了，所以这里找个平时话比较多的朋友来替代吧。

##工具
selenium，mongodb，chromedriver.exe

##思路
1. 利用selenium操纵谷歌浏览器自动化登陆QQ空间获取cookies值
2. 利用requests库向QQ说说的API接口请求数据![Alt text](./1529841274357.png)![Alt text](./1529841343301.png)

##注意事项
1. 注意QQ空间的登陆地址不是第一图，仔细分析，发现登陆界面是用的iframe框架，这是前端的一个知识。可以这样认为，这是在一个页面上镶嵌了另一个页面的数据
![Alt text](./1529838251071.png)
![Alt text](./1529838458518.png)
![Alt text](./1529838518707.png)

2. 打开chrome开发者工具，注意数据来源，而不是直接对页面解析
![Alt text](./1529838848885.png)
![Alt text](./1529838901578.png)
![Alt text](./1529839033699.png)

3. 最后数据存入MongoDB，以字典类型直接插入，与mysql相比，MongoDB直接爽快![Alt text](./1529839251350.png)

4. 查看网页源码，可以直接找到qzonetoken值![Alt text](./1529839411539.png)

5. g_tk需要一定的计算，这里我是通过强大网友帮的忙，实现算法![Alt text](./1529839554066.png)
```python
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
```

6. msglist中content字段一定存在，而pic(图片)，video(视频)不一定存在，所以需要做一些判断来处理一下处理
```
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
```

##最后
![Alt text](./1529840895269.png)

结果是比较满意的，然而稍微有点问题的是，QQ空间显示的是711条说说，但爬下来只有678，我对照过开头以及结尾数十条说说，都能对得上，估计是中间哪里出错了，抓取率只达到了95.5%。还有需要改进的地方。
