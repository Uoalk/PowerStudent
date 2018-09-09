import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os
from pprint import pprint
import datetime
import configparser

config = configparser.ConfigParser()
config.read('account.config')

#


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


def signOn(driver,usr,pw):
    driver.get("https://powerschool.kentdenver.org")
    driver.find_element_by_id("fieldAccount").send_keys(usr);
    driver.find_element_by_id("fieldPassword").send_keys(pw);
    driver.find_element_by_id("btn-enter").click();

def getGrades():
    allTd=driver.find_elements_by_css_selector("table>tbody>tr>td")
    i=6;
    classGrades=[];
    while(i<len(allTd)-6):
        classGrades.append({"name":allTd[i].text,"grade":allTd[i+6].text})
        i+=11
    return classGrades

scrapes=0;
while True:
    try:
        if __name__ == "__main__":
            gradesChanged=False;
            messageData="";
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Firefox(firefox_options=options, executable_path="geckodriver.exe")

            signOn(driver, config['DEFAULT']["powerschoolUsername"],config['DEFAULT']["powerschoolPassword"])



            allTd=driver.find_elements_by_css_selector("#content-main>div>table>tbody>tr>td");
            classNames=[];
            i=16;
            while(i<len(allTd)):
                classNames.append(allTd[i].text.split("\n")[0])
                i+=15


            fn="gradeData.json"
            try:
                file = open(fn, 'r')
            except IOError:
                file = open(fn, 'w')
                fn.write("{}")
            file.close();
            file=open(fn,"r")
            gradeData=json.load(file)
            file.close();



            for className in classNames:
                if(className not in gradeData):
                    gradeData.update({className:[]})
                    gradesChanged=True;
                    messageData+="New class: "+className+"<br>"


            elements=driver.find_elements_by_css_selector('#content-main>div>table>tbody>tr>td>a:not(.mini)')[:-1]
            #for n in range(0,len(elements)):
            #    elements[n].click();

            for n in range(0,len(elements)):
                elements=driver.find_elements_by_css_selector('#content-main>div>table>tbody>tr>td>a:not(.mini)')
                elements[n].click();
                grades=getGrades();
                if(len(gradeData[classNames[n]])!=len(grades)):
                    gradesChanged=True;
                    for i in range(len(gradeData[classNames[n]])-1, len(grades)):
                        messageData+="<b>New grade in "+classNames[n]+":</b> "+grades[i]["name"]+":"+grades[i]["grade"]+"<br>"
                for i in range(0,min(len(grades),len(gradeData[classNames[n]]))):

                    if(gradeData[classNames[n]][i]["grade"]!=grades[i]["grade"]):
                        messageData+="<b>New grade in "+classNames[n]+":</b> "+grades[i]["name"]+":"+grades[i]["grade"]+"<br>"
                gradeData[classNames[n]]=grades;
                driver.back();









            with open('gradeData.json', 'w') as outfile:
                json.dump(gradeData, outfile)

            scrapes+=1;
            if(messageData!=""):
                send_email(config['DEFAULT']["emailAddress"],config['DEFAULT']["emailPassword"],"gfitez20@kentdenver.org","Powerschool update",messageData)
                print(messageData)
            else:
                print(str(datetime.datetime.now())+": no change; total:"+str(scrapes))
            driver.close()
    except Exception as e:
        print(e)
