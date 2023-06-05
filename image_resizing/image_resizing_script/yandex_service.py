# -*- coding: utf-8 -*-

import boto3
from botocore.config import Config


def get_yandex_service(s3_cred_filename) -> boto3.session.Session.client:
    yandex_session = boto3.session.Session()

    yandex_config = Config(
        region_name='ru-central1',
    )

    s3_credentials = dict()
    with open(s3_cred_filename, 'r') as f:
        for s in f:
            s = s.strip().split(' ')
            s3_credentials[s[0]] = s[1]

    return yandex_session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=s3_credentials['aws_access_key_id'],
        aws_secret_access_key=s3_credentials['aws_secret_access_key'],
        config=yandex_config
    )
