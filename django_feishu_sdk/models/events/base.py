#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""飞书事件类型声明

参考订阅事件文档 https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM
"""
from enum import Enum
from typing import Union
import hashlib
import abc
from pydantic import BaseModel

from ...utils import InvalidEventException, Dict2Obj


class EventType(str, Enum):
    APP_OPEN = "app_open"
    APP_STATUS_CHANGE = "app_status_change"
    ORDER_PAID = "order_paid"
    APP_TICKET = "app_ticket"
    APP_UNINSTALLED = "app_uninstalled"

    USER_ADD = "user_add"
    DEPT_ADD = "dept_add"
    USER_STATUS_CHANGE = "user_status_change"
    CONTACT_SCOPE_CHANGE = "contact_scope_change"

    ADD_BOT = "add_bot"
    REMOVE_BOT = "remove_bot"
    P2P_CHAT_CREATE = "p2p_chat_create"
    MESSAGE = "message"
    MESSAGE_READ = "message_read"

    CHAT_DISBAND = "chat_disband"
    GROUP_SETTING_UPDATE = "group_setting_update"

    LEAVE_APPROVAL = "leave_approval"
    LEAVE_APPROVAL_V2 = "leave_approvalV2"
    WORK_APPROVAL = "work_approval"
    SHIFT_APPROVAL = "shift_approval"
    REMEDY_APPROVAL = "remedy_approval"
    TRIP_APPROVAL = "trip_approval"
    OUT_APPROVAL = "out_approval"

    EVENT_REPLY = "event_reply"

    ADD_USER_TO_CHAT = "add_user_to_chat"
    REMOVE_USER_FROM_CHAT = "remove_user_from_chat"
    REVOKE_ADD_USER_FROM_CHAT = "revoke_add_user_from_chat"


class AppStatus(str, Enum):
    START_BY_TENANT = "start_by_tenant"
    STOP_BY_TENANT = "stop_by_tenant"
    STOP_BY_PLATFORM = "stop_by_platform"


class BuyType(str, Enum):
    BUY = "buy"
    UPGRADE = "upgrade"
    RENEW = "renew"


class PricePlanType(str, Enum):
    PER_SEAT_PER_MONTH = "per_seat_per_month"


class UserChatEventType(str, Enum):
    ADD_USER_TO_CHAT = "add_user_to_chat"
    REMOVE_USER_FROM_CHAT = "remove_user_from_chat"
    REVOKE_ADD_USER_FROM_CHAT = "revoke_add_user_from_chat"


class EventHeaderContent(BaseModel):
    event_id: str
    event_type: str
    create_time: str
    token: str
    app_id: str
    tenant_key: str


class EventContent(object):
    """事件回调内容 v2.0
    参考：
    https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/events/receive
    Args:
        schema 2.0 事件模式(版本)
        header 事件头
        event 事件
    """

    schema: str = ''
    header: Union[dict, EventHeaderContent]
    event: Union[dict]

    def __init__(self, request, dict_data, token, encrypt_key):
        header = dict_data.get("header")
        event = dict_data.get("event")
        if header is None or event is None:
            raise InvalidEventException("request is not callback event(v2)")
        self.__request = request
        self.schema = dict_data.get("schema")
        self.header = Dict2Obj(header)
        self.event = Dict2Obj(event)
        self._validate(token, encrypt_key)

    def _validate(self, token, encrypt_key):
        if self.header.token != token:
            raise InvalidEventException("invalid token")
        timestamp = self.__request.headers.get("X-Lark-Request-Timestamp")
        nonce = self.__request.headers.get("X-Lark-Request-Nonce")
        signature = self.__request.headers.get("X-Lark-Signature")
        body = self.__request.body
        bytes_b1 = (timestamp + nonce + encrypt_key).encode("utf-8")
        bytes_b = bytes_b1 + body
        h = hashlib.sha256(bytes_b)
        if signature != h.hexdigest():
            raise InvalidEventException("invalid signature in event")

    @abc.abstractmethod
    def event_type(self):
        return self.header.event_type
