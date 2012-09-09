import logging
logger = logging.getLogger(__name__)

from BeautifulSoup import BeautifulSoup
from pika import BlockingConnection, ConnectionParameters, BasicProperties

import requests
import json as json
import time
import sys

EXCHANGE_NAME = 'process500'

def main(demo=True):
    """ bootstraps the processing by getting the list of 5000 companies and queuing them to be processed """

    if demo == True:
        companies = get_company_name_and_rank(limit=5, pages=1)
    else:
        companies = get_company_name_and_rank()
    
    connection = BlockingConnection(ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, type='direct')
    
    for company in companies: # send company names and ranks to be worked on asychronously
        to_send = json.dumps(company)
        channel.basic_publish(exchange=EXCHANGE_NAME, routing_key="url", body=to_send)
        print " [x] Sent '%s'" % (company)

def worker(worker_type):
    """ a worker that pulls messages from the Rabbit MQ """
    connection = BlockingConnection(ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, type='direct')
    
    channel.queue_declare(queue=worker_type)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=worker_type, routing_key=worker_type)
    
    channel.basic_qos(prefetch_count=1) 
    
    if worker_type == "url":
        callback = get_url_for_company_name
    elif worker_type == "mg":
        callback = get_mg_score_for_url
    elif worker_type == "write":
        callback = write_data
    
    channel.basic_consume(callback, queue=worker_type)
    print ' [*] Waiting for messages in %s queue. To exit press CTRL+C' % (worker_type)
    channel.start_consuming()
    
def get_company_name_and_rank(limit=100, pages=51):
    """ return a list of all the fortune 5000 fastest growing comapnies """ 
    companies = []

    years = ["x"]
    for number in range(1, 51):
        years.append(str(number) + "00")
        
    for year in years[:pages]:
        
        r = requests.get("http://www.inc.com/inc5000/list/2012/%s/" % (year))
        soup = BeautifulSoup(r.text)
        table = soup.find(id="fulltable")
        rows = soup.findAll("tr")[2:] # skip the first 2 rows, which are headers

        for row in rows[:limit]:
            name_cell = row.findAll("td")[1] # company names are in the second col
            rank_cell = row.findAll("td")[0] # company ranks are in the first col
            name_str  = name_cell.a.string
            rank_str  = rank_cell.string
            print "adding %s" % name_str
            company_data = dict(rank=rank_str, name=name_str)
            companies.append(company_data)

    return companies

def get_url_for_company_name(ch, method, properties, body):
    """ lookup URL for a company using fortune's profile on the company """
    
    company_data = json.loads(body)
    company_name = company_data["name"]
    print " [x] Received %r" % (company_name)

    # hacks for slugfiying
    company_name_slug = company_name.lower().replace("& ", "").replace(".", "").replace(",", "").replace(" ", "-") 
    company_profile_url = "http://www.inc.com/inc5000/profile/%s" % company_name_slug

    r = requests.get(company_profile_url)
    soup = BeautifulSoup(r.text)

    detail_section = soup.find("div", "companydetail")
    try:
        company_url = detail_section.find("a")["href"]
    except:
        company_url = None
        
    company_data["url"] = company_url
    to_send = json.dumps(company_data)
    ch.basic_ack(delivery_tag = method.delivery_tag)
    
    # now that we've gotten the company's URL, send the data to another worker to get the MG score
    connection = BlockingConnection(ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, type='direct')
    channel.basic_publish(exchange=EXCHANGE_NAME, routing_key='mg', body=to_send)

def get_mg_score_for_url(ch, method, properties, body):
    """ take a URL and return the overall marketing grader score """
    
    company_data = json.loads(body)
    company_url = company_data["url"]
    print " [x] Received %r" % (company_url)
    
    if company_url == None:
        return "no url to lookup"

    hostname = company_url.split("://")[1] # remove the protocol from the url
    init_url = "http://marketing.grader.com/report/init/%s" % hostname

    try:
        init = requests.get(init_url)
        response_json = json.loads(init.text)
        report_guid = response_json["report"]["guid"]
    except:
        return "error initing MG report"

    while True:
        partial_url = "http://marketing.grader.com/report/partial/%s" % (report_guid)
        partial = requests.get(partial_url)

        response_json = json.loads(partial.text)
        if response_json["success"] == True and response_json["report"]["finished"]:
            company_data["mg"] = response_json["report"]["finalGrade"]
            print " [x] Got final score for %s" % company_data["name"]
            break
        else:
            time.sleep(1) # wait and try polling the API again
            print " [-] Not ready yet, trying again"
            
    to_send = json.dumps(company_data)
    ch.basic_ack(delivery_tag = method.delivery_tag)
    
    # now that we've gotten the company's MG score, send the data to another worker to get it written to disk
    connection = BlockingConnection(ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, type='direct')
    channel.basic_publish(exchange=EXCHANGE_NAME, routing_key='write', body=to_send)

def write_data(ch, method, properties, body):
    """ write the company data to a file """
    
    c = json.loads(body)
    print " [x] Received %r" % (c["name"])
    
    with open('log.txt', 'a') as f:
        str = "%s. %s\t%s\t%s\n" % (c["rank"], c["name"], c["url"], c["mg"])
        f.write(str)
    
    ch.basic_ack(delivery_tag = method.delivery_tag)
    
if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "url":
            worker("url")
        elif sys.argv[1] == "mg":
            worker("mg")
        elif sys.argv[1] == "write":
            worker("write")
    else:
        main(demo=False)
