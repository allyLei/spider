#!/usr/bin/env python
# encoding: utf-8
import os
import logging.config
import time
import yaml

path = lambda root, *a: os.path.join(root, *a)
# some basic path settings
SETTING_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SETTING_DIR)
BASE_DIR = os.path.dirname(PROJECT_ROOT)
STATIC_PATH = path(PROJECT_ROOT, 'static')
TEMPLATE_PATH = path(PROJECT_ROOT, "templates")
LOG_DIR = "/data/log/chaos"

# 部分文件路径
SETTING_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SETTING_DIR)

# Development type setting


class DeploymentType:
    PRODUCTION = "PRODUCTION"
    STAGING = "STAGING"
    TEST = "TEST"
    DEV = "DEV"


if 'DEPLOYMENT_TYPE' in os.environ:
    DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
else:
    DEPLOYMENT = DeploymentType.DEV

# settings for tornado Web class `Application` init
app_conf = {
    # "debug": DEPLOYMENT != DeploymentType.PRODUCTION,
    "debug": False,
    "static_path": STATIC_PATH,
    "template_path": TEMPLATE_PATH,
    "cookie_secret": "!!CHANGEME!!",
    "xsrf_cookies": False
}
# 并发处理新闻的数量
CONCURRENT = 20


# set logging time
logging.Formatter.converter = time.gmtime


# ##########################
# use yaml custom tag
# ##########################
def __pathjoin(loader, node):
    seq = loader.construct_sequence(node)
    return path(*seq)


yaml.add_constructor('!pathjoin', __pathjoin)


# ##########################
# load logging config from yaml file
# ##########################
try:
    f = open(path(SETTING_DIR, 'logging.yml'))
    logging_conf = yaml.load(f)
    prod = logging_conf.pop('product', {})
    _ = logging_conf.pop('log_dir')
    if app_conf['debug']:
        final_conf = logging_conf
    else:
        logging_conf.update(prod)
        final_conf = logging_conf
    logging.config.dictConfig(final_conf)
finally:
    f.close()
# disable boto3 logging
logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('nose').setLevel(logging.WARNING)
logging.getLogger('engineio').setLevel(logging.WARNING)
logging.getLogger('aioredis').setLevel(logging.INFO)
logging.getLogger('aiokafka').setLevel(logging.INFO)

# ##########################
# load storage config
# ##########################
try:
    f = open(path(SETTING_DIR, 'storage.yml'))
    STORAGE = yaml.safe_load(f)[DEPLOYMENT]
except Exception as e:
    STORAGE = {}
finally:
    f.close()

# ##########################
# load weixin config
# ##########################
try:
    f = open(path(SETTING_DIR, 'picture.yml'))
    PICTURE = yaml.safe_load(f)
except Exception as e:
    PICTURE = {}
finally:
    f.close()


if __name__ == '__main__':
    print(STORAGE)
