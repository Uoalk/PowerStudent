#This file contains all of the webscraping data to retreive the grades for a user
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from hashlib import sha256

from collections import OrderedDict




#Simply removes duplicates from a list
def removeDupes(l):
    return list(OrderedDict.fromkeys(l))

#signs onto the main screen of powerschool
def signOn(driver,usr,pw):
    driver.get("https://powerschool.kentdenver.org")
    driver.find_element_by_id("fieldAccount").send_keys(usr)
    driver.find_element_by_id("fieldPassword").send_keys(pw)
    driver.find_element_by_id("btn-enter").click()


#assuming the driver is on a page inside of a course, this function will return all the grade data from that class
def getGradesFromPage(driver):
    allTd2 = driver.find_elements_by_css_selector("#content-main>table>tbody>tr>td")
    #starts at 6th table cell because that's where the first assignment is
    k=4
    #corresponds to the grade number of the class
    num = 0
    grades={}
    while(k<(len(allTd2)-6)):


        assignmentName=allTd2[k+2].text.split("\n")[0]
        score=allTd2[k+8].text.split("\n")[0]
        if ("/" in score) and ("--" not in score):#If a score is input save it
            totalPoints=score.split("/")[1]
            earnedPoints=score.split("/")[0]
        else:#otherwise put it in as null
            totalPoints="null"
            earnedPoints="null"

        #grab the date and category of the grades
        date=allTd2[k].text.split("\n")[0]
        cat=allTd2[k+1].text.split("\n")[0]

        #hash the grade to get an identifier
        hash=sha256((assignmentName+score+date+cat).encode("utf-8")).hexdigest()


        #save all the scraped data
        grades[hash]=({
        'name': assignmentName,
        'rawScore': score,
        'earnedPoints' : earnedPoints,
        'totalPoints': totalPoints,
        'date' : date,
        'category' : cat,

        })
        #skip up 11 cells box because that is how many columns there are
        k+=11
        num+=1
    return grades

#Returns the the names of classes and their links, given that the driver is on the main page of powerschool
def getClassNamesAndLinks(driver):
    classNames=[];
    allTd=driver.find_elements_by_css_selector("#content-main>div>table>tbody>tr>td");
    links=[]
    i=16;#start at the 16th cell (because that's just how powerschool is arranged)
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
    return {"classNames":classNames, "links":links}


#uses the above function to get all grade data for a user
def getGrades(usr, pw):
    options = Options()
    #options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options, executable_path="geckodriver.exe")

    signOn(driver, usr, pw)

    nal=getClassNamesAndLinks(driver);
    links=nal['links'];

    #getting assignments and grades
    gradeData={};
    for n in range(len(links)):
        #clicks on the link to each class
        driver.get(links[n])

        #gets all the data
        allTd2 = driver.find_elements_by_css_selector("#content-main>table>tbody>tr>td")

        className=(allTd2[0].text.split("\n")[0])
        #the name of the class is the 0th element, so it adds the dictionary of grades to the key of the class name
        gradeData[className]=getGradesFromPage(driver);
    driver.close()
    return gradeData


#returns True if it can successfully log on to powerschool with the given credentials
def verifyUsernamePassword(usr,pw):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options, executable_path="geckodriver.exe")
    signOn(driver, usr, pw)
    try: 
        driver.find_element_by_css_selector(".feedback-alert")
        #If this errors, it means that they have successfully signed in
    except:
        return True
    return False

