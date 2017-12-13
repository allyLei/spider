# coding:utf-8

import copy
import json
import requests

SPLASH_SCRIPT = """
function main(splash)
    splash.private_mode_enabled = false
    if (splash.args.user_agent) then
        splash:set_user_agent(splash.args.user_agent)
    end
    if (splash.args.cookies) then
        splash:init_cookies(splash.args.cookies)
    end
    splash:go{url=splash.args.url, headers=splash.args.headers}
    splash:wait(1.5)


    if (splash.args.scroll_distance) then
        local scroll_to = splash:jsfunc("window.scrollTo")
        for i=1,splash.args.scroll_distance,1000 do
            scroll_to(0, i)
            splash:wait(1)
        end
    end
    local entries = splash:history()
    local last_entry=entries[#entries]
    if (last_entry==nil) then
        last_entry={response={headers=nil}}
    end

    splash:set_viewport_full()
    splash:wait(1)
    return {
        splash:html()
    }

end
"""

SPLASH_RENDER_SERVICE_ADDR = "http://internal-news-splash-intra-475729699.us-west-2.elb.amazonaws.com:5000"
ENDPOINT = SPLASH_RENDER_SERVICE_ADDR + "/execute"


def wrap_request_with_splash(req):
    param = {}
    param["url"] = str(req.url)
    if req.proxy:
        param["proxy"] = req.proxy
        # Splash request should not use proxy
        req.proxy = None
    if req.headers:
        param["headers"] = req.headers
    if req.user_agent:
        param["user_agent"] = req.user_agent
    if req.cookies:
        # Splash要求Cookie必须具有正确的domain和path, 否则不会发送
        # 这里根据请求url伪造domain和path, 现在方法比较暴力，以后可以改进
        cookies_for_spalsh = []
        for cookie in req.cookies:
            cookies_for_spalsh.append(
                {
                    "name": cookie,
                    "value": req.cookies[cookie],
                    "domain": "." + req.url.host,
                    "path": "/",
                    # "expires": cookie.expires,
                    # "httpOnly": False,
                    # "secure": False
                }
            )
        param["cookies"] = cookies_for_spalsh
    scroll_distance = req.user_data.get("ajax_scroll_distance", 0)
    if scroll_distance != 0:
        param["scroll_distance"] = scroll_distance
    else:
        param["scroll_distance"] = 6000
    param["lua_source"] = SPLASH_SCRIPT
    param["timeout"] = 120
    new_req = copy.deepcopy(req)
    new_req.url = ENDPOINT
    new_req.method = "post"
    if new_req.headers is None:
        new_req.headers = {}
    new_req.headers["content-type"] = "application/json"
    new_req.data = json.dumps(param)
    new_req.user_data["origin_req_before_splash"] = req
    return new_req


def init_params(url):
    params = {}
    params["url"] = url
    params["timeout"] = 120
    params["scroll_distance"] = 20000
    params["lua_source"] = SPLASH_SCRIPT

    return params


headers = {
    'cookie': 'cna=MnXqEfN/s2cCAXMi7r+pPqX6; _uab_collina=151134558568331197373288; cq=ccp%3D0; hng=CN%7Czh-CN%7CCNY%7C156; uc1=cookie14=UoTdevlByfneTA%3D%3D&lng=zh_CN&cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&existShop=false&cookie21=VFC%2FuZ9ainBZ&tag=8&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&pas=0; uc3=sg2=WqGsNtAZDlmE41qwTbTDVhagobqS2O0YkPI00MptRCw%3D&nk2=GgIGRzXDR00%2B&id2=UU6lSYjMEVGL5A%3D%3D&vt3=F8dBzLQCI5cZJiwm23U%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D; tracknick=yibwu7788; _l_g_=Ug%3D%3D; ck1=; unb=2644345992; lgc=yibwu7788; cookie1=BxIYgyhjMtUs%2F2upTsLmLKtbKtBYdcQZsuZzhmCrqcI%3D; login=true; cookie17=UU6lSYjMEVGL5A%3D%3D; cookie2=14f710047a2b10f84e0fb0781a0690e6; _nk_=yibwu7788; t=b3c52c50e34daaa4293b4d88e274898e; uss=AVUlRczPQdLs3IxtgN%2Fx%2FQxhFJn2W%2BkRJFWaod33cBlFeTDJHlU3D58qNSs%3D; skt=ae8552e91e5e0174; _tb_token_=580863700e1be; _umdata=BA335E4DD2FD504F7CF98A3A6B07C53AEEF78D72373F7D4B29C65DB1EEB9B67DB73482E66D71A119CD43AD3E795C914CDD3399B5304D84F918F595EA9D1A9542; pnm_cku822=; isg=Anx8i8IEChi0nj261NCR8joeTRwkSenXE7NWMlb9g2dyIRyrfoXwL_KTd3-i',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'cache-control': 'max-age=0',
    'authority': 'moussy.tmall.com',
    'referer': 'https://moussy.tmall.com/search.htm?spm=a1z10.3-b-s.w4011-16812940133.405.5b19e4433bKCwc&search=y&pageNo=2&tsearch=y',
}


def request_spiash_server(url):
    params = init_params(url)
    r = requests.get(ENDPOINT, params, headers=headers)
    if r.status_code == 200:
        print(r.text)
    else:
        print(r.status_code)