#!/usr/bin/env python
# encoding: utf-8

# flake8: ignore=E402

import os
import sys
import asyncio
import logging
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sanic import Sanic, response
from chaos.api import crawl_picture

logger = logging.getLogger('chaos.main')

app = Sanic('chaos')


def test(request):
    print(request.args)
    print(type(request.args))
    print(request.args.get("s"))
    return response.text("Helloworld")


# Sanic HTTP 接口路由配置
# app.add_route(login, '/login', methods=['POST'])
app.add_route(test, '/', methods=['GET'])
app.add_route(crawl_picture, '/images', methods=['GET'])


if __name__ == "__main__":
    server = app.create_server(host="0.0.0.0", port=8888)
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(server)
    logger.info("Server Started.")
    loop.run_forever()
    # app.run(host="0.0.0.0", port=8000)
