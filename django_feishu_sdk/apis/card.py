#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""消息卡片相关

- 发送卡片消息，临时卡片消息，删除临时卡片消息
- flask和sanic的blueprint
"""
import logging
from typing import Union, Callable, Optional, Awaitable

from .base import BaseAPI, allow_async_call, decrypt_aes
from ..models import CardMessage, CardContent, SendMsgType

logger = logging.getLogger("feishu")


class CardAPI(BaseAPI):
    @allow_async_call
    def send_card(
            self,
            card: Union[dict, CardMessage],
            update_multi: bool = None,
            open_id: str = "",
            user_id: str = "",
            email: str = "",
            chat_id: str = "",
            root_id: str = "",
    ) -> Optional[str]:
        """发送卡片消息

        https://open.feishu.cn/document/ukTMukTMukTM/uYTNwUjL2UDM14iN1ATN

        Args:
            card: dict或CardMessage类型
            update_multi: 控制卡片是否是共享卡片, 默认位False
            open_id: 用户的飞信ID(自建应用)
            user_id: 用户的应用ID(三方应用)
            email: 用户的邮箱
            chat_id: 群ID, 以上4种ID必须提供一种, 优先级为chat_id>open_id>user_id>email
            root_id: 回复消息所对应的呃消息id, 可选
        Returns:
            message_id

        请求body示例
        {
           "chat_id": "oc_abcdefg1234567890",
           "msg_type": "interactive",
           "root_id":"om_4*********************ad8",
           "update_multi":false,
           "card": {
                // card content
            }
        }

        card参数示例
        {
            "config": {
                "wide_screen_mode": true
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "this is header"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "This is a very very very very very very very long text;"
                    }
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "Read"
                            },
                            "type": "default"
                        }
                    ]
                }
            ]
        }
        """
        api = "/message/v4/send/"

        msg = CardMessage(
            msg_type=SendMsgType.INTERACTIVE, card=card, update_multi=update_multi
        )
        if root_id:
            msg.root_id = root_id

        if chat_id:
            msg.chat_id = chat_id
        elif open_id:
            msg.open_id = open_id
        elif user_id:
            msg.user_id = user_id
        elif email:
            msg.email = email

        payload = msg.dict(exclude_none=True)
        result = self.client.request("POST", api=api, payload=payload)
        return result.get("data", {}).get("message_id")

    def send_ephemeral_card(self, card: Union[dict, CardMessage]) -> str:
        """发送临时卡片消息

        https://open.feishu.cn/document/ukTMukTMukTM/uETOyYjLxkjM24SM5IjN

        使用场景
            临时消息卡片多用于群聊中用户与机器人交互的中间态。
            例如在群聊中用户需要使用待办事项类bot创建一条提醒，
            bot 发送了可设置提醒日期和提醒内容的一张可交互的消息卡片，
            此卡片在没有设置为临时卡片的情况下为群内全员可见，既群内可看见该用户与 bot 交互的过程。
            而设置为临时卡片后，交互过程仅该用户可见，群内其他成员只会看到最终设置完成的提醒卡片。

        临时消息卡片可降低群消息的信噪比，并间接增加 bot 通知的用户触达。

        注意, card对象必须提供chat_id
        """
        api = "/ephemeral/v1/send"

        if isinstance(card, CardMessage):
            payload = card.dict(exclude_unset=True)
        else:
            payload = dict(card)

        result = self.client.request("POST", api=api, payload=payload)
        return result.get("data", {}).get("message_id")

    def delete_ephemeral_card(self, message_id: str):
        """删除临时卡片

        失败会raise FeishuError, (code和msg对应飞书平台的code/msg)
        """
        api = "/ephemeral/v1/delete"
        payload = {"message_id": message_id}
        self.client.request("POST", api=api, payload=payload)
