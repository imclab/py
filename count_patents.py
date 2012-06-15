import requests
from BeautifulSoup import BeautifulSoup

def find_patents():
    
    f = open('schools.txt', 'r')
    schools = [ school.strip().lower() for school in f]
    f.close()
    
    for school in schools:
        num = count_references(school, 2004)
    
def count_patents(school, year):    
    
    print "counting patents for %s..." % school
    
    school_str = school.replace(' ', '+')
    
    url = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&f=S&l=50&d=PTXT&RS=%28ISD%2F" + str(year) + "%24%24+AND+AN%2F%22" + school_str + "%22%29&Refine=Refine+Search&Refine=Refine+Search&Query=+%28ISD%2F%24%2F%24%2F" + str(year) + "+AND+AN%2F%22" + school_str + "%22%29+OR++%28ISD%2F%24%2F%24%2F2003+AND+LREP%2F%22massachusetts+institute+of+technology%22%29"
    
    #print url
    
    r = requests.get(url)
    
    try:
        results = r.text.split("</strong> out of <strong>")[1].split("</strong>")[0]
    except:
        results = "0"
    
    f = open('log.txt', 'a')
    f.write(results + "\n")
    f.close() 

def count_references(school, year):

    print "counting references for %s..." % school
    
    school_str = school.replace(' ', '+')
    
    url = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query=%28ISD%2F"+ str(year) +"%24%24+AND+REF%2F%22" + school_str + "%22%29+OR+%0D%0A%28ISD%2F" + str(year) + "%24%24+AND+FREF%2F%22" + school_str + "%22%29+OR+%0D%0A%28ISD%2F" + str(year) + "%24%24+AND+OREF%2F%22" + school_str + "%22%29&d=PTXT"
    r = requests.get(url)
    
    try:
        results = r.text.split("</strong> out of <strong>")[1].split("</strong>")[0]
    except:
        results = "0 for %s" % school
    
    f = open('log.txt', 'a')
    f.write(results + "\n")
    f.close()
    
if __name__ == "__main__":
    find_patents()