import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys


import os
from pprint import pprint
import datetime
import configparser

config = configparser.ConfigParser()
config.read('account.config')

#


import smtplib


def signOn(driver,usr,pw):
    driver.get("https://powerschool.kentdenver.org")
    driver.find_element_by_id("fieldAccount").send_keys(usr);
    driver.find_element_by_id("fieldPassword").send_keys(pw);
    driver.find_element_by_id("btn-enter").click();





if __name__ == "__main__":
    gradesChanged=False;
    messageData="";
    options = Options()
    ptions.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options, executable_path="geckodriver.exe")

    signOn(driver, config['DEFAULT']["powerschoolUsername"],config['DEFAULT']["powerschoolPassword"])



    allTd=driver.find_elements_by_css_selector("#content-main>div>table>tbody>tr>td");
    classNames=[];
    i=16;
    while(i<len(allTd)):
        classNames.append(allTd[i].text.split("\n")[0])
        i+=15


    print(classNames)
    driver.close()
