#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""飞书通讯录事件

https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/department/field-overview
"""
from .base import EventContent


class UserCreatedEvent(EventContent):
    """
    事件类型：员工入职
    飞书文档地址：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/user/events/created
    """

    @staticmethod
    def event_type():
        return "contact.user.created_v3"


class UserUpdatedEvent(EventContent):
    """
    事件类型：员工信息被修改
    飞书文档地址：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/user/events/updated
    """

    @staticmethod
    def event_type():
        return "contact.user.updated_v3"


class UserDeletedEvent(EventContent):
    """
    事件类型：员工离职
    飞书文档地址：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/user/events/deleted
    """

    @staticmethod
    def event_type():
        return "contact.user.deleted_v3"


class DepartmentCreatedEvent(EventContent):
    """
    事件类型：部门被创建
    飞书文档地址：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/department/events/created
    """

    @staticmethod
    def event_type():
        return "contact.department.created_v3"


class DepartmentUpdatedEvent(EventContent):
    """
    事件类型：员工信息被修改
    飞书文档地址：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/department/events/updated
    """

    @staticmethod
    def event_type():
        return "contact.department.updated_v3"


class DepartmentDeletedEvent(EventContent):
    """
    事件类型：部门信息被修改
    飞书文档地址：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/department/events/deleted
    """

    @staticmethod
    def event_type():
        return "contact.department.deleted_v3"
