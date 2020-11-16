# -*- coding: utf-8 -*-
# @Time    : 2020/10/20 18:37
# @Author  : Baron！
# @FileName: checkout.py
# @Software: PyCharm

# -*- coding: utf-8 -*-
import os

import oss2

def CalculateFolderLength(bucket, folder):
    length = 0
    for obj in oss2.ObjectIterator(bucket, prefix=folder):
        length += obj.size
    return length

# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
auth = oss2.Auth('****', '****')
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, 'https://oss-cn-shenzhen.aliyuncs.com', 'csjs-static')

# for obj in oss2.ObjectIterator(bucket, delimiter='/'):
#     if obj.is_prefix():  # 文件夹
#         length = CalculateFolderLength(bucket, obj.key)
#         print('directory: ' + obj.key + '  length:' + str(length / 1024) + "KB.")
#     else: # 文件
#         print('file:' + obj.key + '  length:' + str(obj.size / 1024) + "KB.")
#
# # 设置Delimiter参数为正斜线（/）。
# for obj in oss2.ObjectIterator(bucket, delimiter = '/'):
# 	# 通过is_prefix方法判断obj是否为文件夹。
#     if obj.is_prefix():  # 文件夹
#         print('directory: ' + obj.key)
#     else:                # 文件
#         print('file: ' + obj.key)

# 列举存储空间下所有文件。
sum = 0
local_dir = 'C:\\Users\Baron\Desktop\oss_download\\'
for obj in oss2.ObjectIterator(bucket, prefix="****"):
    if (obj.size / 1024) >= 100:
        print(obj.key)
        filepath = local_dir + obj.key
        filedir = os.path.dirname(filepath)
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        print('目录创建成功:' + filedir)
        bucket.get_object_to_file(obj.key, filepath)
        sum = sum + 1
print(sum)