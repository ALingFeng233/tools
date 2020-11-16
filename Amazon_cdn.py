# -*- coding: utf-8 -*-
import time
import boto3
import logging

log = logging.getLogger(name='aws-cdn')
cfg = {
    'aws_access_key_id': '****',
    'aws_secret_access_key': '****',
    'region_name': '****',
    'DistributionId': '****'
}


def cdn_refresh(cfg, domain, paths):
    if isinstance(paths, str):
        paths = [paths]
    DistributionId = cfg.pop('DistributionId')
    print(DistributionId)
    print(type(DistributionId))
    now = time.time()
    client = boto3.client('cloudfront', aws_access_key_id=cfg['aws_access_key_id'],
                          aws_secret_access_key=cfg['aws_secret_access_key'], region_name=cfg['region_name'])
    par = {
        "DistributionId": DistributionId,
        "InvalidationBatch": {
            "Paths": {
                "Quantity": len(paths),
                "Items": [paths[i] for i in range(len(paths))]
            },
            'CallerReference': str(int(now * 1000))
        }
    }
    try:
        response = client.create_invalidation(**par)
        print(repr(response))
        if response['ResponseMetadata']['HTTPStatusCode'] == '201':
            return True
        return response
    except Exception as e:
        log.exception(e)
        return False

if __name__ == '__main__':
    cfg = {
        'aws_access_key_id': '****',
        'aws_secret_access_key': '****',
        'region_name': '****',
        'DistributionId': '****'
    }
    domain = '****'
    paths = ['****']
    cdn_refresh(cfg, domain, paths)