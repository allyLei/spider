#!/usr/bin/env pyt# hon
# encoding: utf-8
import logging
from sanic import response
from chaos.controllers.picture import PictureCtrl


async def crawl_picture(request):
    """获取图片
    """
    resp_data = {
        "engine": None,
        "word": [],
        "limit": 0,
        "images": []
    }
    # 参数解析
    req_data = request.args
    params, flag = format_request_data(req_data)
    logging.getLogger().info("check request: %s, format request: %s" % (flag, params))
    if flag:
        images = await PictureCtrl().handler(params)
        resp_data["engine"] = params["engine"]
        resp_data["word"] = params["word"].split("+")
        resp_data["limit"] = params["limit"]
        resp_data["images"] = images
    logging.getLogger().info("response data: %s, %s, %s, %s" %
                             (resp_data["engine"], resp_data["word"], resp_data["limit"], len(resp_data["images"])))
    return response.json(resp_data)


def format_request_data(req_data):
    """格式化请求参数
    """
    flag = False
    params = None
    engine = req_data.get("engine", None)
    if engine:
        word = req_data.get("word", None)
        limit = req_data.get("limit", 0)
        size = req_data.get("size", None)
        width = 0
        height = 0
        sizetype = req_data.get("sizetype", "eq" if size else None)
        if (not size) and sizetype:
            flag = False
        else:
            flag = True
        if size:
            item = size.strip().split(",")
            if len(item) == 2:
                width = item[0]
                height = item[1]
        params = {
            "engine": engine,
            "word": "+".join(word.split(" ")) if word else "",
            "limit": int(limit),
            "size": {"width": width, "height": height},
            "sizetype": sizetype
        }
    return params, flag
