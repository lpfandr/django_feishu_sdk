#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from enum import Enum
from django.conf import settings

logger = logging.getLogger("feishu")

# 环境变量名
DEFAULTS = {
    'FEISHU_TOKEN_EXPIRE_TIME': 7200,  # token时效, https://open.feishu.cn/document/ukTMukTMukTM/uIjNz4iM2MjLyYzM
    'FEISHU_TOKEN_UPDATE_TIME': 600,  # token提前更新的时间
    'FEISHU_BATCH_SEND_SIZE': 200,  # 批量发送消息列表的大小限制
    'FEISHU_APP_ID': None,
    'FEISHU_APP_SECRET': None,
    'FEISHU_VERIFY_TOKEN': None,
    'FEISHU_ENCRYPT_KEY': None
}


class APISettings:
    def __init__(self, defaults=None):
        self.defaults = defaults or DEFAULTS
        self.user_settings = getattr(settings, 'FEISHU_V2_SDK_CONFIGS', None)  # CKEditor 5 configuration in settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]
        # Cache the result
        setattr(self, attr, val)
        return val


api_settings = APISettings(DEFAULTS)


# try:
#     if settings.FEISHU_APP_ID:
#         FEISHU_APP_ID = settings.FEISHU_APP_ID
#     if settings.FEISHU_APP_SECRET:
#         FEISHU_APP_SECRET = settings.FEISHU_APP_SECRET
#     if settings.FEISHU_ENCRYPT_KEY:
#         FEISHU_ENCRYPT_KEY = settings.FEISHU_ENCRYPT_KEY
#     if settings.FEISHU_VERIFY_TOKEN:
#         FEISHU_VERIFY_TOKEN = settings.FEISHU_VERIFY_TOKEN
#     if settings.FEISHU_TOKEN_EXPIRE_TIME:
#         FEISHU_TOKEN_EXPIRE_TIME = settings.FEISHU_TOKEN_EXPIRE_TIME
#     if settings.FEISHU_TOKEN_UPDATE_TIME:
#         FEISHU_TOKEN_UPDATE_TIME = settings.FEISHU_TOKEN_UPDATE_TIME
#     if settings.FEISHU_BATCH_SEND_SIZE:
#         FEISHU_BATCH_SEND_SIZE = settings.FEISHU_BATCH_SEND_SIZE
# except Exception as e:
#     logger.debug(f"导入飞书应用和事件的配置出现报错(%s)，请查看settings配置" % e)


class AppType(str, Enum):
    TENANT = "tenant"  # 企业自建应用
    USER = "user"  # 第三方应用
