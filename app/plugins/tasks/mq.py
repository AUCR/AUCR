# coding=utf-8
"""Default RabbitMQ function file."""
import pika
from flask import current_app


def index_mq_aucr_task(rabbit_mq_server, task_name, routing_key):
    """Create MQ aucr task."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_mq_server))
    channel = connection.channel()
    channel.basic_publish(exchange='',  routing_key=routing_key,  body=task_name)
    connection.close()


def get_mq_aucr_tasks(call_back, rabbit_mq_server, rabbit_mq_que):
    """Start MQ message consumer."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_mq_server))
    channel = connection.channel()
    channel.queue_declare(queue=rabbit_mq_que)
    channel.basic_consume(call_back, queue=rabbit_mq_que, no_ack=True)
    channel.start_consuming()
    connection.close()


def get_a_task_mq(tasks, call_back, rabbitmq_server):
    """Start MQ tasks consumer."""
    get_mq_aucr_tasks(call_back, rabbitmq_server, tasks)


def index_mq_aucr_report(task_name, rabbit_mq_dict):
    """Create MQ aucr report task."""
    rabbit_mq_server = rabbit_mq_dict
    index_mq_aucr_task(rabbit_mq_server, task_name, "logging")
