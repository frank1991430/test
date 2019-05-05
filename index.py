import logging
import numpy as np
import json
from process import get_data_from_redis, dealing_data, analysis, send_data_to_redis


def handler(event, context):
    # print(np.__version__)
    temp = []
    # original_data = get_data_and_response()
    # ==================================================================
    # needs to be replaced
    with open('original_data.json', 'rb') as f:
        original_data = f.read().decode()
    original_data = json.dumps(original_data)
    original_data = json.loads(original_data)
    if original_data.startswith(u'\ufeff'):
        original_data = original_data.encode('utf8')[3:].decode('utf8')
    # ==================================================================
    original_data = json.loads(original_data)
    # print(len(original_data))
    original_data = get_data_from_redis(original_data)
    project_data_dict = dealing_data(original_data)
    suggestion_return = json.dumps(analysis(project_data_dict), ensure_ascii=False)
    send_data_to_redis(suggestion_return)
    return 'success'

