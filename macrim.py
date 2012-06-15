#selenium 2.23.0
from selenium import selenium, webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from BeautifulSoup import BeautifulSoup 
from datetime import datetime
import time

def main():
    browser = webdriver.Firefox()
    browser.get("http://tools.relevantweb.com/login.aspx")
    
    assert "Login Page" in browser.title
    
    # login
    username = browser.find_element_by_name("txtUsername")
    username.send_keys("imu.admin")
    
    password = browser.find_element_by_name("txtPassword")
    password.send_keys("password" + Keys.RETURN)
    
    # get report page
    browser.get("http://tools.relevantweb.com/reporting/execute.aspx?id=4")
    
    report_type = Select( browser.find_element_by_name("_transform_id") )
    report_type.select_by_visible_text("Generic HTML")
    
    exam_type = Select( browser.find_element_by_name("_column_values") )
    exam_type.select_by_visible_text("Inbound Marketing Exam")
    
    today = datetime.now()
    month = str(today.month).zfill(2)
    day = str(today.day).zfill(2)
    year = str(today.year).zfill(2)
    today_string = month + "/" + day + "/" + year

    browser.find_element_by_css_selector("#_cal_values_31").clear()
    browser.find_element_by_css_selector("#_cal_values_31").send_keys("01012010")
    browser.find_element_by_css_selector("#_cal_values_41").clear()
    browser.find_element_by_css_selector("#_cal_values_41").send_keys(today_string)
    
    # submit report params
    browser.find_element_by_xpath("//input[@value='Execute']").click()
    
    # parse response
    html = browser.page_source
    soup = BeautifulSoup(html)
    entries = soup.table.table.findAll("tr")[7:]
    
    for entry in entries:
        fields = entry.findAll("td")
        try:
            stud_id = fields[1].pre.string
            full_name = fields[2].pre.string
            email = fields[3].pre.string
            date = fields[4].pre.string
            time_taken = fields[5].pre.string
            score = fields[6].pre.string
            status = fields[7].pre.string
        except IndexError:
            break # reached the end of the list
    
    # import pdb; pdb.set_trace()
    
    browser.close()

if __name__ == "__main__":
    main()