# /usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Tuple

from .base import BaseAPI, allow_async_call


class CloudAPI(BaseAPI):

    @allow_async_call
    def get_cloud_allfiles(self, folder_token):
        """获取文件夹下的清单

        https://open.feishu.cn/open-apis/drive/v1/files

        Returns:
            json
        """
        api = "/drive/v1/files"
        payload = dict(
            app_id=self.client.app_id,
            app_secret=self.client.app_secret,
        )
        params = dict(
            page_size=10,
            folder_token=folder_token,
        )
        result = self.client.request("GET", api=api, payload=payload, params=params)
        # 返回 Body ：
        # {
        #     "code":0,
        #     "msg":"ok",
        #     "tenant_access_token":"xxxxx",
        #     "expire":7200  // 过期时间，单位为秒（两小时失效）
        # }
        return result

    @allow_async_call
    def get_cloud_folderdata(self, folderToken: str):
        """获取文件夹元信息

        https://open.feishu.cn/open-apis/drive/explorer/v2/folder/:folderToken/meta

        Returns:
            json
        """
        api = "/drive/explorer/v2/folder/" + folderToken + "/meta"
        payload = dict(
            app_id=self.client.app_id,
            app_secret=self.client.app_secret,
        )
        params = dict(
        )
        result = self.client.request("GET", api=api, payload=payload, params=params)
        # 返回 Body ：
        # {
        #     "code":0,
        #     "msg":"ok",
        #     "tenant_access_token":"xxxxx",
        #     "expire":7200  // 过期时间，单位为秒（两小时失效）
        # }
        return result

    @allow_async_call
    def creat_cloud_folder(self, name, folder_token: str = ''):
        """在云文件夹下创建文件夹

        https://open.feishu.cn/open-apis/drive/v1/files/create_folder

        Returns:
            json
        """
        api = "/drive/v1/files/create_folder"
        payload = dict(
            app_id=self.client.app_id,
            app_secret=self.client.app_secret,
            name=name,
            folder_token=folder_token,
        )
        result = self.client.request("POST", api=api, payload=payload)
        # 返回 Body ：
        # {
        #     "code":0,
        #     "msg":"ok",
        #     "tenant_access_token":"xxxxx",
        #     "expire":7200  // 过期时间，单位为秒（两小时失效）
        # }
        return result

    @allow_async_call
    def creat_cloud_table(self, title, folder_token: str = ''):
        """在云文件夹下创建表格
        https://open.feishu.cn/open-apis/sheets/v3/spreadsheets

        Args:
            title: 表格名字
            folder_token: 表格所在文件
        Returns:
            json
        Raises:
            FeishuException
        """
        api = "/sheets/v3/spreadsheets"
        payload = dict(
            app_id=self.client.app_id,
            app_secret=self.client.app_secret,
            title=title,
            folder_token=folder_token,
        )
        result = self.client.request("POST", api=api, payload=payload)
        # 返回 Body ：
        # {
        #     "code":0,
        #     "msg":"ok",
        #     "tenant_access_token":"xxxxx",
        #     "expire":7200  // 过期时间，单位为秒（两小时失效）
        # }
        return result

    @allow_async_call
    def get_cloud_tabledata(self, spreadsheetToken: str):
        """获取表格元数据

        https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/:spreadsheetToken/metainfo

        Returns:
            json
        """
        api = "/sheets/v2/spreadsheets/" + spreadsheetToken + "/metainfo"
        payload = dict(
            app_id=self.client.app_id,
            app_secret=self.client.app_secret,
        )
        result = self.client.request("GET", api=api, payload=payload)
        # 返回 Body ：
        # {
        #     "code":0,
        #     "msg":"ok",
        #     "tenant_access_token":"xxxxx",
        #     "expire":7200  // 过期时间，单位为秒（两小时失效）
        # }
        return result
