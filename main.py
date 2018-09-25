import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

import json
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
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options, executable_path="geckodriver.exe")

    signOn(driver, config['DEFAULT']["powerschoolUsername"],config['DEFAULT']["powerschoolPassword"])



    allTd=driver.find_elements_by_css_selector("#content-main>div>table>tbody>tr>td");
    allLinks=driver.find_elements_by_css_selector("#content-main>div>table>tbody>tr>td>a");

    classNames=[];

    links=[]
    i=16;
    while (i<(len(allTd)-2)):
        classNames.append(allTd[i].text.split("\n")[0])
        #adds the link of the grade of each class
        try:
            links.append(allTd[i+1].find_elements_by_css_selector("a")[0].get_attribute("href"))
        #it does a try except because second semester classes don't have links with them, throwing an IndexError
        except IndexError:
            pass
        i+=15
    print(classNames)

    #removes the last 4 links, becuse those are advisory and reflections, not classes
    newLinks = links[0:(len(links)-4)]

    classes = {}

    #getting assignments and grades
    for j in range(len(newLinks)):
        #clicks on the link to each class
        driver.get(newLinks[j])

        #gets all the data
        allTd2 = driver.find_elements_by_css_selector("#content-main>table>tbody>tr>td")

        grades = {}

        #starts at 6 because that's where the first assignment is
        k=6
        #corresponds to the grade number of the class
        num = 0
        while(k<(len(allTd2)-6)):
            #adds the grades in format of 'assignment': assigment, 'grade': grade
            grades[num] = {
            'assignment': (allTd2[k].text.split("\n")[0]),
            'grade' : (allTd2[k+6].text.split("\n")[0])
            }
            #gradesDic[(allTd2[k].text.split("\n")[0])] = (allTd2[k+6].text.split("\n")[0])
            k+=11
            num+=1

        #the name of the class is the 0th element, so it adds the dictionary of grades to the key of the class name
        classes[(allTd2[0].text.split("\n")[0])] = grades

        #goes back to main browser
        driver.execute_script("window.history.go(-1)")


        with open('grades.json', 'w') as file:
            json.dump(classes, file, indent=2)

    driver.close()
