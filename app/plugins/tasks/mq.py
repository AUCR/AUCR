# coding=utf-8
"""Default RabbitMQ function file."""
import pika
import glob
from yaml_info.yamlinfo import YamlInfo


def index_mq_aucr_task(rabbit_mq_server, task_name, routing_key):
    """Create MQ aucr task."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_mq_server))
    channel = connection.channel()
    channel.basic_publish(exchange='',  routing_key=routing_key,  body=task_name)
    connection.close()


def get_mq_aucr_tasks(call_back, rabbit_mq_server, rabbit_mq_que, rabbitmq_username, rabbitmq_password):
    """Start MQ message consumer."""
    credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(credentials=credentials, host=rabbit_mq_server))
    channel = connection.channel()
    channel.queue_declare(queue=rabbit_mq_que)
    channel.basic_consume(call_back, queue=rabbit_mq_que, no_ack=True)
    channel.start_consuming()
    connection.close()


def get_a_task_mq(tasks, call_back, rabbitmq_server, rabbitmq_username, rabbitmq_password):
    """Start MQ tasks consumer."""
    get_mq_aucr_tasks(call_back, rabbitmq_server, tasks, rabbitmq_username, rabbitmq_password)


def index_mq_aucr_report(task_name, rabbit_mq_dict, task_mq):
    """Create MQ aucr report task."""
    rabbit_mq_server = rabbit_mq_dict
    index_mq_aucr_task(rabbit_mq_server, str(task_name), task_mq)


def get_mq_yaml_configs():
    """MQ aucr yaml config file from each plugin."""
    mq_yaml_dict_config = {}
    tasks_mq_list = []
    reports_mq_list = []
    analysis_mq_list = []
    for filename in glob.iglob('app/plugins/**/mqtasks.yml', recursive=True):
        mq_tasks = YamlInfo(filename, "none", "none")
        run = mq_tasks.get()
        if "tasks" in run:
            tasks_mq_list.append(run["tasks"])
        if "reports" in run:
            reports_mq_list.append(run["reports"])
        if "analysis" in run:
            analysis_mq_list.append(run["analysis"])
    mq_yaml_dict_config["tasks"] = tasks_mq_list
    mq_yaml_dict_config["reports"] = reports_mq_list
    mq_yaml_dict_config["analysis"] = analysis_mq_list
    return mq_yaml_dict_config
