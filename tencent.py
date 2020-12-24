import json
import logging

import os
from tencentcloud.cdn.v20180606 import cdn_client, models
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

log = logging.getLogger(__name__)


def cdn_refresh(cfg, domain, paths):
    try:
        if isinstance(paths, str):
            paths = [paths]
        rel_path = []
        for item in paths:
            item = 'https://' + os.path.join(domain, item.lstrip('/')).replace('\\', '/')
            rel_path.append(item)
        cred = credential.Credential(cfg['cdn_accessKeyId'], cfg['cdn_accessSecret'])
        http_profile = HttpProfile()
        http_profile.endpoint = "cdn.tencentcloudapi.com"

        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile
        client = cdn_client.CdnClient(cred, cfg['cdn_region_id'], client_profile)

        req = models.PurgeUrlsCacheRequest()

        params = {
            "Urls": rel_path
        }
        req.from_json_string(json.dumps(params))

        resp = client.PurgeUrlsCache(req)
        if hasattr(resp,'TaskId'):
            return True
        return resp.to_json_string()

    except TencentCloudSDKException as err:
        log.exception(err)
        return False


def cdn_preheat(cfg, domain, paths):
    try:
        if isinstance(paths, str):
            paths = [paths]
        rel_path = []
        for item in paths:
            item = 'https://' + os.path.join(domain, item.lstrip('/')).replace('\\', '/')
            rel_path.append(item)
        cred = credential.Credential(cfg['cdn_accessKeyId'], cfg['cdn_accessSecret'])
        httpProfile = HttpProfile()
        httpProfile.endpoint = "cdn.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = cdn_client.CdnClient(cred, cfg['cdn_region_id'], clientProfile)

        req = models.PushUrlsCacheRequest()
        params = {
            "Urls": rel_path
        }
        req.from_json_string(json.dumps(params))

        resp = client.PushUrlsCache(req)
        if hasattr(resp,'TaskId'):
            return True
        return resp.to_json_string()

    except TencentCloudSDKException as err:
        log.exception(err)
        return False
