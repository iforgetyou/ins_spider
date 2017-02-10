#!/usr/bin/python
# coding:utf-8
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import urllib2
import ssl
import re
import time
import json
import logging

from Models import InsImage

base_url = 'https://www.instagram.com'


class BS4Ins(object):
    # 关闭证书
    # ssl._create_default_https_context = ssl._create_unverified_context
    # To issue an HTTPS request, set the validate_certificate parameter to true when calling the urlfetch.fetch() method.

    def image_loader_filter(tag):
        return tag.name == 'img' and tag.has_attr('src') and tag.has_attr('id') and tag['id'].find(
            "pImageLoader_") != -1

    # 通过数据直接找资源
    def find_src_by_data(self, url):
        # 最后一次访问的id
        last_id = ''
        # 访问主页
        # response = urllib.request.urlopen('https://www.instagram.com/cherry_quahst/')
        # response = urllib2.request.urlopen(url) # 3.6
        response = urllib2.urlopen(url)  # 2.7
        logging.info(response.getcode())
        html_doc = response.read()

        # 构建soup
        soup = BeautifulSoup(html_doc, "lxml")

        # 打印全部
        # logging.debug(soup.prettify())
        logging.debug("---------------------------------------------------------------------------------")
        images = []
        # 直接通过data数据找url
        for tag in soup.find_all(text=re.compile('_sharedData')):
            # 找到json数据,替换掉多余数据
            json_data = tag.replace('window._sharedData = ', '').replace(';', '')
            logging.info(json_data)
            data = json.loads(json_data)
            # 主页处理
            if 'ProfilePage' in data['entry_data']:
                pages = data['entry_data']['ProfilePage']
                for page in pages:
                    nodes = page['user']['media']['nodes']
                    # 遍历节点
                    for node in nodes:
                        img = InsImage()
                        img.id = node['id']
                        img.image_url = node['display_src']
                        img.owner = node['owner']
                        # 判断图片或者视频
                        if node['is_video']:
                            # 视频
                            img.video_url = find_video_url('https://www.instagram.com/p/' + node['code'])
                        else:
                            # 图片
                            pass
                        # print(json.dumps(img, default=lambda o: o.__dict__, sort_keys=True))
                        images.append(img)
                        # 最后的id
                        last_id = node['id']
                        # print(last_id)
                        # 递归调用加载更多
                        # self.find_src_by_data("https://www.instagram.com/instagram/?max_id=" + last_id)
        # 返回找到的结果
        return images


def find_video_url(url):
    # response = urllib.request.urlopen(url)
    response = urllib2.urlopen(url)
    logging.info(response.getcode())
    html_doc = response.read()

    # 构建soup
    soup = BeautifulSoup(html_doc, "lxml")
    # 直接通过data数据找url
    for tag in soup.find_all(text=re.compile('_sharedData')):
        # 找到json数据,替换掉多余数据
        json_data = tag.replace('window._sharedData = ', '').replace(';', '')
        logging.info(json_data)
        data = json.loads(json_data)

    # 视频页面处理
    if 'PostPage' in data['entry_data']:
        pages = data['entry_data']['PostPage']
        for page in pages:
            return page['media']['video_url']

# BS4Ins().find_src_by_data('https://www.instagram.com/instagram/')
