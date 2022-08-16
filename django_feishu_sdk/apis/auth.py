# /usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Tuple, Dict

from .base import BaseAPI, allow_async_call


class AuthAPI(BaseAPI):

    @allow_async_call
    def get_tenant_access_token(self) -> Tuple[str, int]:
        """获取自建应用的token

        https://open.feishu.cn/document/ukTMukTMukTM/uIjNz4iM2MjLyYzM

        Returns:
            Tuple[token, expire]
        """
        api = "/auth/v3/tenant_access_token/internal/"
        payload = dict(
            app_id=self.client.app_id,
            app_secret=self.client.app_secret,
        )
        result = self.client.request("POST", api=api, payload=payload, auth=False)
        return result["tenant_access_token"], result["expire"]

    def resend_app_ticket(self):
        """重新推送app_ticket

        https://open.feishu.cn/document/ukTMukTMukTM/uQjNz4CN2MjL0YzM
        """
        NotImplementedError

    @allow_async_call
    def get_user_info(self, user_id: str,
                      user_id_type: str = 'open_id',
                      department_id_type: str = 'open_department_id') -> Dict:
        """获取单个用户信息（user_id_type和department_id_type设置默认值）

        https://open.feishu.cn/open-apis/contact/v3/users/:user_id

        Returns:
            Dict
        """
        api = "/contact/v3/users/" + user_id
        payload = dict(
            app_id=self.client.app_id,
            app_secret=self.client.app_secret,
        )
        params = dict(
            user_id_type=user_id_type,
            department_id_type=department_id_type,
        )
        result = self.client.request("GET", api=api, payload=payload, params=params)
        return result

    @allow_async_call
    def get_user_by_department(self, department_id: str, user_id_type: str = 'open_id',
                               department_id_type: str = 'open_department_id'):
        """获取部门直属用户列表

        https://open.feishu.cn/open-apis/contact/v3/users/find_by_department

        Returns:
            json
        """
        api = "/contact/v3/users/find_by_department"
        payload = dict(
            app_id=self.client.app_id,
            app_secret=self.client.app_secret,
        )
        params = dict(
            user_id_type=user_id_type,
            department_id_type=department_id_type,
            department_id=department_id,
        )
        result = self.client.request("GET", api=api, payload=payload, params=params)
        return result

    @allow_async_call
    def get_department_by_id(self, department_id: str, user_id_type: str = 'open_id',
                             department_id_type: str = 'open_department_id'):
        """获取单个部门信息

        https://open.feishu.cn/open-apis/contact/v3/departments/:department_id

        Returns:
            json
        """
        api = "/contact/v3/departments/" + department_id
        payload = dict(
            app_id=self.client.app_id,
            app_secret=self.client.app_secret,
        )
        params = dict(
            user_id_type=user_id_type,
            department_id_type=department_id_type,
        )
        result = self.client.request("GET", api=api, payload=payload, params=params)
        return result
