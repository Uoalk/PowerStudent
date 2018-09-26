import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

import json
import os
from pprint import pprint
import datetime
import configparser
from collections import OrderedDict

config = configparser.ConfigParser()
config.read('account.config')

#

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
def send_email(user, pwd, recipient, subject, body):#https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = recipient


    msg.attach(MIMEText(body, 'html'))

    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(user,pwd)
    mail.sendmail(user, recipient, msg.as_string())
    mail.quit()



def removeDupes(l):
    return list(OrderedDict.fromkeys(l))

def signOn(driver,usr,pw):
    driver.get("https://powerschool.kentdenver.org")
    driver.find_element_by_id("fieldAccount").send_keys(usr);
    driver.find_element_by_id("fieldPassword").send_keys(pw);
    driver.find_element_by_id("btn-enter").click();


def getGrades():
    #starts at 6 because that's where the first assignment is
    k=6
    #corresponds to the grade number of the class
    num = 0
    grades=[]
    while(k<(len(allTd2)-6)):

        #adds the grades in format of 'assignment': assigment, 'grade': grade
        assignmentName=allTd2[k].text.split("\n")[0]
        score=allTd2[k+6].text.split("\n")[0]

        grades.append({
        'name': assignmentName,
        'score' : score
        })
        k+=11
        num+=1
    return grades

def getStoredGrades():
    fn="gradeData.json"
    try:
        file = open(fn, 'r')
    except IOError:
        file = open(fn, 'w+')
        file.write("{}")
    file.close()
    file=open(fn,"r")
    gradeData=json.load(file)
    file.close();
    return gradeData
if __name__ == "__main__":
    gradesChanged=False;
    messageData="";
    options = Options()
    #options.add_argument("--headless")
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

    classNames=removeDupes(classNames)#sometimes duplicate classes occur
    print(classNames)

    gradeData=getStoredGrades()


    for className in classNames:
        if(className not in gradeData):
            gradeData.update({className:[]})
            gradesChanged=True;
            messageData+="New class: "+className+"<br>"

    classes = {}

    grade={}
    #getting assignments and grades
    for n in range(len(links)):
        #clicks on the link to each class
        driver.get(links[n])

        #gets all the data
        allTd2 = driver.find_elements_by_css_selector("#content-main>table>tbody>tr>td")

        grades = {}


        className=(allTd2[0].text.split("\n")[0])
        #the name of the class is the 0th element, so it adds the dictionary of grades to the key of the class name

        grades=getGrades();
        if(len(gradeData[classNames[n]])!=len(grades)):
            gradesChanged=True;
            for i in range(len(gradeData[classNames[n]]), len(grades)):
                messageData+="<b>New grade in "+classNames[n]+":</b> "+grades[i]["name"]+":"+grades[i]["score"]+"<br>"
        for i in range(0,min(len(grades),len(gradeData[classNames[n]]))):

            if(gradeData[classNames[n]][i]["name"]!=grades[i]["name"]):
                messageData+="<b>New grade in "+classNames[n]+":</b> "+grades[i]["name"]+":"+grades[i]["score"]+"<br>"
        gradeData[classNames[n]]=grades;

        #goes back to main browser
        driver.execute_script("window.history.go(-1)")

    print(gradeData)
    with open('gradeData.json', 'w') as file:
        json.dump(gradeData, file, indent=2)

    if(messageData!=""):
        send_email(config['DEFAULT']["emailAddress"],config['DEFAULT']["emailPassword"],config['DEFAULT']["sendEmailTo"],"Powerschool update",messageData)
        print(messageData)
    else:
        print(str(datetime.datetime.now())+": no change")

    driver.close()
