# -*- coding: utf-8 -*-
# @Time    : 2020/12/21 14:35
# @Author  : Baron！
import json
import logging
import requests

log = logging.getLogger(name='4399-cdn')

default_push_url = 'https://fapi.gz4399.com/api/portal/v1/push'
default_preheat_url = 'https://fapi.gz4399.com/api/portal/v1/preheat'


def _domain_url(domain):
    domain = str(domain).lower()
    if not (domain.startswith('http://') or domain.startswith('https://')):
        domain = 'https://' + domain
    if domain.endswith('/'):
        domain = domain[:len(domain) - 1]
    return domain


def _refresh(domain, paths):
    data = {}
    urls = []
    dirs = []
    if isinstance(paths, str):
        paths = [paths]
    for i in paths:
        ri = i.rindex('/')
        name = i[ri + 1:]
        i = domain + i
        if not name:
            dirs.append(i)
        else:
            urls.append(i)
    if len(urls) != 0:
        data["urls"] = urls
        data["urlAction"] = "expire"
    if len(dirs) != 0:
        data["dirs"] = dirs
        data["dirAction"] = "expire"
    refresh_data = json.dumps(data)
    return refresh_data


def _preheat(domain, paths):
    data = {}
    urls = []
    if isinstance(paths, str):
        paths = [paths]
    for i in paths:
        ri = i.rindex('/')
        name = i[ri + 1:]
        i = domain + i
        if not name:
            return False
        urls.append(i)
    if len(urls) != 0:
        data["urls"] = urls
        data["urlAction"] = "preheat_urlcomm"
    preheat_data = json.dumps(data)
    return preheat_data


def cdn_refresh(cfg, domain, paths):
    try:
        headers = {
            "X-Auth-User": cfg.get('user'),
            "X-Auth-Password": cfg.get('password')
        }
        data = _refresh(_domain_url(domain), paths)
        post_url = cfg.get('push_url', default_push_url)
        print("4399 cdn push", post_url, data)
        res = requests.post(url=post_url, data=data, headers=headers)
        callback = json.loads(res.content)
        code = callback['code']
        msg = callback['message']
        if code == 0:
            return True
        return {"异常": str(code) + ' - ' + msg}
    except Exception as e:
        log.exception(e)
        return repr(e)


def cdn_preheat(cfg, domain, paths):
    try:
        headers = {
            "X-Auth-User": cfg.get('user'),
            "X-Auth-Password": cfg.get('password')
        }
        data = _preheat(_domain_url(domain), paths)
        post_url = cfg.get('preheat_url', default_preheat_url)
        print("4399 cdn preheat", post_url, data)
        res = requests.post(url=post_url, data=data, headers=headers)
        callback = json.loads(res.content)
        code = callback['code']
        msg = callback['message']
        if code == 0:
            return True
        return {"异常": str(code) + ' - ' + msg}
    except Exception as e:
        log.exception(e)
        return repr(e)


if __name__ == '__main__':
    cfg = {
        "user": "***",
        "password": "***",
        "domain": "csjs-cdnres.netfungame.com"
    }
    domain = "http://csjs-cdnres.netfungame.com"
    paths = "/game/ios4399-cod/"

    result = cdn_refresh(cfg, domain, paths)
    print("refresh result:", result)

    paths = "/game/ios4399-cod/index.html"
    result = cdn_preheat(cfg, domain, paths)
    print("preheat result:", result)
