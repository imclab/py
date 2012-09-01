from pika import BlockingConnection, ConnectionParameters, BasicProperties
import sys

def work_queue():
    message = ' '.join(sys.argv[1:]) or "Hello World!"
    
    connection = BlockingConnection(ConnectionParameters('localhost'))
    channel = connection.channel()
    queue_name = 'work_queue'
    
    # create a work queue and send a message directly to it, bypassing the exchange
    channel.queue_declare(queue='work_queue', durable=True)
    channel.basic_publish(exchange='', routing_key='work_queue', body=message,  properties=BasicProperties(delivery_mode=2))
    print " [x] Sent '%s'" % (message)
    connection.close()
    
def fanout_exchange():
    message = ' '.join(sys.argv[1:]) or "Hello World!"
    
    connection = BlockingConnection(ConnectionParameters('localhost'))
    channel = connection.channel()
    exchange_name = 'analytics'
    
    # create a fanout queue
    channel.exchange_declare(exchange=exchange_name, type='fanout')
    
    # send a task
    channel.basic_publish(exchange=exchange_name, routing_key='', body=message)
    print " [x] Sent '%s'" % (message)
    connection.close() 
    
def direct_exchange():
    severity = sys.argv[1]
    message = ' '.join(sys.argv[2:]) or "Hello World!"
    message = severity + ": " + message
    
    connection = BlockingConnection(ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # create a direct exchange
    channel.exchange_declare(exchange='direct_logs', type='direct')
    
    # send a task
    channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)
    print " [x] Sent '%s'" % (message)
    connection.close()
    
if __name__ == "__main__":
    direct_exchange()