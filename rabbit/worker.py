from pika import BlockingConnection, ConnectionParameters
import time

def work_queue():
    # http://www.rabbitmq.com/tutorials/tutorial-two-python.html
    connection = BlockingConnection(ConnectionParameters('localhost'))
    channel = connection.channel()
    queue_name = 'work_queue'
    
    # don't send tasks to this worker until it's ready, keep them in the queue for other workers
    # THIS IS IMPORTANT, otherwise adding more workers won't help anything cause 
    # all msgs will already have been sent to the currently 'busy' workers
    channel.basic_qos(prefetch_count=1) 
    
    # create the work queue and start consuming
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_consume(callback, queue=queue_name)
    print ' [*] Waiting for messages. To exit press CTRL+C'
    channel.start_consuming()
    
def fanout_exchange():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # connect to exchange and queue
    channel.exchange_declare(exchange='analytics', type='fanout')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    
    # bind to the queue and start consuming
    channel.queue_bind(exchange='analytics', queue=queue_name)
    channel.basic_consume(callback, queue=queue_name)
    print ' [*] Waiting for messages. To exit press CTRL+C'
    channel.start_consuming()
    
def direct_exchange():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # connect to exchange and queue
    channel.exchange_declare(exchange='direct_logs', type='direct')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    
    # create multiple bindings from the queue to the exchange 
    # not sure how this realy helps, if they're all going to the same queue...
    severities = ['critical', 'error', 'warning', 'info', 'debug']
    for severity in severities:
        channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)
        
    channel.basic_consume(callback, queue=queue_name)
    print ' [*] Waiting for messages. To exit press CTRL+C'
    channel.start_consuming()
    
def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    time.sleep( body.count('.') )
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print " [x] Done"
    
if __name__ == "__main__":
    work_queue()