# 网站 哔哩哔哩
# 功能 爬取b站视频的弹幕并保存
# 功能 弹幕生成词云
# 哔哩哔哩弹幕所在xml文件 https://comment.bilibili.com/192966399.xml
# 哔哩哔哩弹幕所在xml文件 https://api.bilibili.com/x/v1/dm/list.so?oid=192966399
# 测试视频的地址 https://www.bilibili.com/video/BV1tC4y1H7yz?spm_id_from=333.851.b_696e7465726e6174696f6e616c486561646572.37
# 测试视频 192966399


# 请求xml，返回弹幕信息
def sendRequest():
    # 发起请求
    resp = requests.get(url=url, headers=headers, proxies=proxies)
    # 转码
    resp.encoding = "utf-8"
    # 打印状态码
    print("code-",resp.status_code)
    # print(resp.text)
    # 使用BS处理解析数据源
    soup = BeautifulSoup(resp.text, "xml")
    # print(soup)
    # 获取d标签的所有内容

    p_list= soup.find_all(name="d")
    # 输出字幕的个数
    print("len-",len(p_list))
    # 将弹幕输入列表comment_list中
    for p in p_list:
        # 去空白字符
        text = p.text.strip()
        # 列表末尾插入
        comment_list.append(text)
        # 打印
        # print(text)
    # 保存
    save(comment_list)
    # 返回列表
    return comment_list


def save(comment_list):
    # 打开文件
    file = open("哔哩哔哩弹幕-" + oid + ".txt", "w", encoding="utf-8")
    # 循环写入
    for list in comment_list:
        file.write(list)
        file.write("\n")

    file.flush()
    file.close()



def generateWordCloud(comment_list):
    allComment = "" # 拼接所有的弹幕
    for comment in comment_list:
        allComment+=comment

    # 分词处理
    cut = jieba.cut(allComment)

    # 统计词汇总量
    c_dict = Counter(cut)
    # print(c_dict)

    # 把字典转换成二维列表
    word_list = [[key,value] for key,value in c_dict.items()]
    # print(word_list)

    # 绘制词云
    wordCloud = (
        WordCloud()
            .add(series_name="哔哩哔哩", data_pair=word_list, word_size_range=[20, 100])
            .set_global_opts(
            title_opts=options.TitleOpts(
                title="哔哩哔哩弹幕词云",
                title_textstyle_opts=options.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=options.TooltipOpts(is_show=True),
        )

    )
    # 生成词云
    wordCloud.render("哔哩哔哩弹幕词云-"+oid+".html")




# 入口
if __name__ == '__main__':
    # 导入框架
    import re #正则表达式
    import requests # 模拟游览器发起地址栏请求，可以获取服务器响应结果
    from bs4 import BeautifulSoup # 快速解析html，xml等数据的，可以帮你提前几个小时或者几天的额外时间完成任务
    import jieba  # 分词统计框架
    from pyecharts.charts import WordCloud  # 词云
    from pyecharts import options
    from collections import Counter  # 统计的内置函数

    # 定制头部
    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}

    #  用户代理
    proxies = {
        "http://":"148.70.158.7:8080",
        "https://": "148.70.158.7:8080"
    }

    # 测试视频的地址 https://www.bilibili.com/video/BV1tC4y1H7yz?spm_id_from=333.851.b_696e7465726e6174696f6e616c486561646572.37
    # https://www.bilibili.com/video/BV1tM4y1b7No/?spm_id_from=333.1007.tianma.1-3-3.click&vd_source=2a9ba257609d6a92dabb3b80a998e8ad
    # 弹幕接口url带有oid参数，需要先获取oid，在网页源代码中搜索oid的值发现cid就是oid，可以通过正则来提取cid
    # 获取视频的地址
    print("请输入视频的地址：")
    url =input()
    html_text = requests.get(url=url, headers=headers, proxies=proxies).text
    # print(html_text)


    #新版哔哩哔哩页面数据变化，老版正则匹配不到cid字段----20230506
    try:
        oid = re.search('cid=(\d+)&aid=\d+', html_text).group(1)
    except:
        oid = re.search('cid":(\d{9,11}),', html_text).group(1)

    # 得到视频的oid
    print("视频的oid：" + oid)

    # 哔哩哔哩弹幕所在xml文件 https://comment.bilibili.com/oid.xml
    # 哔哩哔哩弹幕所在xml文件 https://api.bilibili.com/x/v1/dm/list.so?oid=oid
    # 测试视频oid  192966399    1119379139
    url = "https://comment.bilibili.com/" + oid + ".xml"
    # 存放弹幕的序列
    comment_list = []

    generateWordCloud(sendRequest())