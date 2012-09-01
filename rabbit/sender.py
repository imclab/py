from pika import BlockingConnection, ConnectionParameters, BasicProperties
import sys

def work_queue():
    message = ' '.join(sys.argv[1:]) or "Hello World!"
    
    connection = BlockingConnection(ConnectionParameters('localhost'))
    channel = connection.channel()
    queue_name = 'work_queue'
    
    # create a work queue and send a message directly to it, bypassing the exchange
    channel.queue_declare(queue='work_queue', durable=True)
    channel.basic_publish(exchange='', routing_key='work_queue', body=message,  properties=BasicProperties(delivery_mode = 2))
    print " [x] Sent '%s'" % (message)
    connection.close()
    
def fanout_exchange():
    message = ' '.join(sys.argv[1:]) or "Hello World!"
    
    connection = BlockingConnection(ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # create a fanout queue
    channel.exchange_declare(exchange='analytics', type='fanout')
    
    # send a task
    channel.basic_publish(exchange='analytics', routing_key='', body=message)
    print " [x] Sent '%s'" % (message)
    connection.close() 
    
def direct_exchange():
    message = ' '.join(sys.argv[1:]) or "Hello World!"
    
    connection = BlockingConnection(ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # create a fanout queue
    channel.exchange_declare(exchange='direct_logs', type='direct')
    
    # send a task of a random severity level
    from random import choice
    severities = ['critical', 'error', 'warning', 'info', 'debug']
    severity = choice(severities)
    message = severity + ": " + message
    channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)
    print " [x] Sent '%s'" % (message)
    connection.close()
    
if __name__ == "__main__":
    work_queue()