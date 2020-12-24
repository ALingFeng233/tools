#!/usr/bin/env python
# coding=utf-8
import json
import logging
from typing import Union

import os
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

log = logging.getLogger(name='cdn')


class Client(AcsClient):
    def __init__(self, ak, secret, region_id='cn-shenzhen'):
        super().__init__(
            ak=ak,
            secret=secret,
            region_id=region_id,
            auto_retry=True,
            max_retry_time=5,
            user_agent='GameWinnerInc',
        )

    def do_action_json(self, req: CommonRequest) -> Union[None, dict]:
        resp = self.do_action_with_exception(req)
        if isinstance(resp, bytes):
            resp = json.loads(resp.decode('utf-8'))
        return resp


class Request(CommonRequest):
    domain = ''
    version = ''

    def __init__(self, action_name=None, uri_pattern=None, product=None, location_endpoint_type='openAPI'):
        if self.domain:
            __class__.domain = self.domain
            __class__.version = self.version
        CommonRequest.__init__(self, domain=self.domain, version=self.version, action_name=action_name,
                               uri_pattern=uri_pattern, product=product,
                               location_endpoint_type=location_endpoint_type)
        self.set_method('POST')

    @staticmethod
    def request(cls, client: Client, action_name, params: dict = None):
        __class__.domain = cls.domain
        __class__.version = cls.version
        req = __class__(action_name=action_name)
        if params:
            for k, v in params.items():
                if v is not None:
                    req.add_query_param(k, v)
        return client.do_action_json(req)


class PushObjectCacheRequest(Request):
    domain = 'cdn.aliyuncs.com'
    version = '2018-05-10'

    @staticmethod
    def run_preheat(client: Client, params: dict):
        """
        运行预热
        :param client: API客户端实例
        :param params: 参数
        :return:
        """
        c = __class__
        return c.request(c, client, 'PushObjectCache', params)


class RefreshObjectCacheRequest(Request):
    domain = 'cdn.aliyuncs.com'
    version = '2018-05-10'

    @staticmethod
    def run_refresh(client: Client, params: dict):
        """
        运行刷新
        :param client: API客户端实例
        :param params: 参数
        :return:
        """
        c = __class__
        return c.request(c, client, 'RefreshObjectCaches', params)


def cdn_preheat(cfg, domain, paths):
    if isinstance(paths, str):
        paths = [paths]
    if len(paths) > 2000:
        log.error('预热文件数量超出限制')
        return False
    path_list = [paths[i:i + 100] for i in range(0, len(paths), 100)]
    client = Client(cfg['cdn_accessKeyId'], cfg['cdn_accessSecret'], cfg['cdn_region_id'])
    try:
        for one in path_list:
            rel_path = []
            for item in one:
                item = 'https://' + os.path.join(domain, item.lstrip('/')).replace('\\', '/')
                rel_path.append(item)
            path_str = "\n".join(rel_path)
            # 国内domestic 海外overseas
            response = PushObjectCacheRequest().run_preheat(client=client,
                                                            params={'Area': 'domestic', 'ObjectPath': path_str})
            if "PushTaskId" not in response:
                return False
        return True
    except Exception as e:
        log.exception(e)
        return False


def cdn_refresh(cfg, domain, paths):
    if isinstance(paths, str):
        paths = [paths]
    urls = []
    _type = 'File'
    for item in paths:
        if item.endswith('/'):
            _type = 'Directory'
        item = 'https://' + os.path.join(domain, item.lstrip('/')).replace('\\', '/')
        urls.append(item)
    urls_str = "\n".join(urls)
    client = Client(cfg['cdn_accessKeyId'], cfg['cdn_accessSecret'], cfg['cdn_region_id'])
    # 国内domestic 海外overseas
    try:
        response = RefreshObjectCacheRequest().run_refresh(client=client,
                                                           params={'ObjectPath': urls_str, 'ObjectType': _type})
        if 'RefreshTaskId' in response:
            return True
        return str(response)
    except Exception as e:
        log.exception(e)
        return False
