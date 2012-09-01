from pika import BlockingConnection, ConnectionParameters
import time

def work_queue():
    # http://www.rabbitmq.com/tutorials/tutorial-two-python.html
    connection = BlockingConnection(ConnectionParameters('localhost'))
    channel = connection.channel()
    queue_name = 'work_queue'
    
    # don't send tasks to this worker until it's ready, keep them in the queue for other workers
    # THIS IS IMPORTANT, otherwise adding more workers won't help anything cause 
    # all msgs will already have been sent to the currently 'busy' worker(s)
    channel.basic_qos(prefetch_count=1) 
    
    # create the work queue and start consuming
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_consume(callback, queue=queue_name)
    print ' [*] Waiting for messages. To exit press CTRL+C'
    channel.start_consuming()
    
def fanout_exchange():
    connection = BlockingConnection(ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # connect to exchange and queue
    channel.exchange_declare(exchange='analytics', type='fanout')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    exchange_name = 'analytics'
    
    # bind to the queue and start consuming
    channel.queue_bind(exchange=exchange_name, queue=queue_name)
    channel.basic_consume(callback, queue=queue_name)
    print ' [*] Waiting for messages. To exit press CTRL+C'
    channel.start_consuming()
    
def direct_exchange():
    connection = BlockingConnection(ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # connect to exchange and queue
    channel.exchange_declare(exchange='direct_logs', type='direct')
    
    # create multiple queues to handle each type of severity
    severities = ['critical', 'error', 'warning', 'info', 'debug']
    for severity in severities:
        channel.queue_declare(queue=severity)
        channel.queue_bind(exchange='direct_logs', queue=severity, routing_key=severity)
    
    # pick a random severity level queue to attach this worker to
    from random import choice
    severities = ['critical', 'error', 'warning', 'info', 'debug']
    severity = choice(severities)
    severity = "info"
    
    # don't send tasks to this worker until it's ready, keep them in the queue for other workers
    # THIS IS IMPORTANT, otherwise adding more workers won't help anything cause 
    # all msgs will already have been sent to the currently 'busy' worker(s)
    channel.basic_qos(prefetch_count=1) 
    
    channel.basic_consume(callback, queue=severity)
    print ' [*] Waiting for messages in %s queue. To exit press CTRL+C' % (severity)
    channel.start_consuming()
    
def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    time.sleep( body.count('.') )
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print " [x] Done"
    
if __name__ == "__main__":
    direct_exchange()