from CommunicationConfig import *
from queue import Queue
from threading import Thread
import redis
import datetime
import json
import numpy as np
import pandas as pd
from utils import tree, dicts
from judge_strategy import *


class TaskThread(Thread):
    def __init__(self, thread_id, task_queue, R):
        super().__init__()
        self.thread_id = thread_id
        self.task_queue = task_queue  # 任务队列
        self.R = R  # redis实例

    def run(self):
        super().run()
        global original_data
        # global exitFlag
        while True:
            if exitFlag:
                break

            try:
                task = self.task_queue.get(block=False)
                for i in task["body"]:
                    meterid = i['meterId']
                    i["data"] = self.R.get_data("emHumiDataTimeKey:{}:*".format(meterid))
                self.task_queue.task_done()
            except Exception as e:
                pass


class RedisConnection(BaseClass):
    def __init__(self, config):
        """
        初始化参数:
        密码，ip，端口
        """
        super(RedisConnection, self).__init__(config)
        self.host = self.config.HOST
        self.port = self.config.PORT
        self.password = self.config.PASS
        self.time_now = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        # self.time_now = "2019-04-26"

    def connect(self):
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, password=None, decode_responses=True)
        self.connection = redis.Redis(connection_pool=self.pool)

    def get_data(self, key):
        data = []
        self.keys = self.connection.keys(key)
        for i in self.keys:
            data += json.loads(json.loads(json.dumps(self.connection.get(i))))
        return json.dumps(data)

    def set_value(self, key, value):
        self.connection.set(key, value)


def get_data_from_redis(original_data):
    """
    从redis取出数据
    :param original_data:
    :return: original_data
    """
    R = RedisConnection(GetConfig)
    R.connect()
    # t = time.time()
    original_data_number = len(original_data)
    original_data_queue = Queue(len(original_data))
    global exitFlag
    exitFlag = False
    for i in original_data:
        original_data_queue.put(i)
    for i in range(original_data_number):
        my_thread = TaskThread(i, original_data_queue, R)
        my_thread.start()
    original_data_queue.join()
    exitFlag = True
    # print(time.time() - t)
    return original_data


def dealing_data(original_data):
    project_name_list = []
    project_data_dict = {}

    for i in original_data:
        project_name_list.append(i['projectName'])
    project_name_set = set(project_name_list)
    for project_name in project_name_set:
        for data in original_data:
            if data["projectName"] == project_name:
                project_data_dict[project_name] = {"datetime": data["dateTime"], "entityId": data["entityId"], "data": data["body"]}
    for project_name in project_data_dict.keys():
        for point in project_data_dict[project_name]["data"]:
            df = pd.read_json(point['data']).sort_values(by='datetime')
            df.reset_index(inplace=True)
            del df["index"]
            df.dropna(axis=0, inplace=True)
            point["tp_average_7"] = np.average(df.tp.values) - (point["tpEnd"] + point["tpStart"]) # 七天平均温差
            tp_average_1 = df[df["datetime"] > str(datetime.datetime.now() - datetime.timedelta(hours=72))]
            tp_average_2 = df[df["datetime"] > str(datetime.datetime.now() - datetime.timedelta(hours=96))]
            tp_average_2 = tp_average_2[tp_average_2["datetime"] <= str(datetime.datetime.now() - datetime.timedelta(hours=72))]
            point["tp_average_1"] = np.average(tp_average_1.tp.values) - (point["tpEnd"] + point["tpStart"])  # 前一天平均温度
            point["tp_average_2"] = np.average(tp_average_2.tp.values) - (point["tpEnd"] + point["tpStart"])  # 前两天平均温度
            del point["data"]
    return project_data_dict


def analysis(project_data_dict):
    suggestion_return = []
    for project_name in project_data_dict.keys():
        payload = {"entityId": project_data_dict[project_name]["entityId"], "projectName": project_name,
                   "dateTime": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}
        df = pd.read_json(json.dumps(project_data_dict[project_name]["data"]))
        df.set_index('locIds', inplace=True)
        df["tp_average_np"] = df.apply(lambda x: np.array([x.tp_average_7, x.tp_average_1, x.tp_average_2]), axis=1)
        print(df)
        suggestion_list = []
        room_tree = tree()  # 创建树结构
        for i in list(df.index):
            room_tree[json.loads(i)[0]][json.loads(i)[1]][json.loads(i)[2]]
        room_tree = dicts(room_tree)  # 树结构转换为普通字典结构
        for i in list(df.index):  # 树结构下每个value变成({locId:}, [平均值])的形式，room
            room_tree[json.loads(i)[0]][json.loads(i)[1]][json.loads(i)[2]] = df.tp_average_np[i]
            suggestion_list.append({json.loads(i)[2]: judge_room(df.tp_average_np[i][1])})  # 根据前一天的平均温度判断房间是否存在问题
        sum_building = 0
        num = 0
        for k, i in zip(room_tree.keys(), room_tree.values()):  # building
            for j in i.keys():  # floor
                sum_building += np.sum(list(i[j].values()), axis=0)
                num += len(list(i[j].values()))
                i[j] = (i[j], np.average(list(i[j].values()), axis=0))
                suggestion_list.append({j: judge_floor(i[j][1][1], list(i.keys()))})
            room_tree[k] = (room_tree[k], sum_building/num)
            suggestion_list.append({k: judge_building(room_tree[k][1][1], list(room_tree.keys()))})
        payload["suggestion"] = suggestion_list
        suggestion_return.append(payload)
    return suggestion_return


def send_data_to_redis(suggestion_return):
    R = RedisConnection(SetConfig)
    R.connect()
    R.set_value("suggestionForSem", suggestion_return)
    R.set_value("suggestionForSem:"+str(datetime.datetime.now().strftime("%Y-%m-%d")), suggestion_return)
