#!/usr/bin/env python
# encoding: utf-8
import re
import math
import logging
import aiohttp
from chaos.settings import PICTURE_ENGINE


class PictureCtrl:
    """
    图片相关
    """

    async def handler(self, request):
        """
        """
        images = []
        if request.get("engine", "") == "baidu":
            logging.getLogger().info("engine: baidu")
            images = await self.baidu_handler(request)
        return images

    async def baidu_handler(self, request):
        """获取百度图片
        """
        baidu_url = PICTURE_ENGINE["baidu"]["url"]
        pn = PICTURE_ENGINE["baidu"]["pn"]
        images = []
        baidu_params = {
            "word": request.get("word", ""),
            "width": request.get("size", {}).get("width", ""),
            "height": request.get("size", {}).get("height", ""),
            "tn": "baiduimage",
            "gsm": "3c",
            "pn": "0",
            "ct": "",
            "lm": "-1",
            "ic": "0",
            "ie": "utf-8",
        }
        limit = request.get("limit", 0)
        # 翻页次数
        page_count = int(math.ceil(limit / (pn * 1.0)))
        async with aiohttp.ClientSession() as session:
            for i in range(page_count):
                if len(images) >= limit:
                    break
                baidu_params["pn"] = pn * i
                logging.getLogger().info("[BAIDU] request params: %s" % baidu_params)
                async with session.get(baidu_url, params=baidu_params) as resp:
                    resp_str = await resp.text()
                    # print(resp_str)
                    urls = self.regex_imageurl_baidu(resp_str)
                    images += urls
        images = images[:limit]
        logging.getLogger("[BAIDU] images count: %s" % len(images))
        return images

    def regex_imageurl_baidu(self, text):
        """正则方法找到百度图片URL
        """
        urls = set()
        pattern = re.compile(r'"thumbURL":"http.*?"')
        result = pattern.findall(text)
        if result:
            for line in result:
                item = line.strip().split('thumbURL":')
                if len(item) != 2:
                    continue
                _, url = item
                url = url.strip().strip('"')
                urls.add(url)
        return urls
