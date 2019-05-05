# 与rabbitmq通讯相关的参数设置
USERNAME = "jnc"  # 用户名
PASSWORD = "juneng"  # 密码
HOST = '14.23.57.52'  # ip
PORT = 5672  # 端口
EXCHANGE = 'sem.server.exchange'  # 交换机名称
EXCHANGE_TYPE = 'topic'  # 交换机方式
# QUEUE_NAME_GET = "dgjykj_data"  # 获取数据的队列
# ROUTING_KEY_GET = "dgjykj_data"  # 获取数据的routingkey
QUEUE_NAME_GET = "lisitao"  # 获取数据的队列
ROUTING_KEY_GET = "lisitao"  # 获取数据的routingkey
QUEUE_NAME_RESPONSE = "lisitao_test_send_queue"  # 回送回应的队列
ROUTING_KEY_RESPONSE = "lisitao_test_send_queue"    # 回送回应的routingkey
QUEUE_NAME_CONTROL = "return_message"   # 上送下发指令以及下发状态的队列
ROUTING_KEY_CONTROL = "return_message"  # 上送下发指令以及下发状态的routingkey
QUEUE_NAME_ALARM = "lisitao_test_alarm_queue"   # 上送警报指令的队列
ROUTING_KEY_ALARM = "lisitao_test_alarm_queue"  # 上送警报指令的routingkey123


class Config(object):
    @staticmethod
    def init_app(app):
        pass


class GetConfig(Config):
    HOST = "192.168.1.239"
    PORT = 6379
    PASS = None


class SetConfig(Config):
    HOST = "192.168.1.224"
    PORT = 6379
    PASS = None
    # HOST = "192.168.1.239"
    # PORT = 6379
    # PASS = None


class BaseClass(object):
    def __init__(self, config):
        self.config = config


