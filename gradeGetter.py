import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from hashlib import sha256

from collections import OrderedDict





def removeDupes(l):
    return list(OrderedDict.fromkeys(l))

def signOn(driver,usr,pw):
    driver.get("https://powerschool.kentdenver.org")
    driver.find_element_by_id("fieldAccount").send_keys(usr)
    driver.find_element_by_id("fieldPassword").send_keys(pw)
    driver.find_element_by_id("btn-enter").click()


def getGradesFromPage(driver):
    allTd2 = driver.find_elements_by_css_selector("#content-main>table>tbody>tr>td")
    #starts at 6 because that's where the first assignment is
    k=4
    #corresponds to the grade number of the class
    num = 0
    grades={}
    while(k<(len(allTd2)-6)):

        #adds the grades in format of 'assignment': assigment, 'grade': grade
        assignmentName=allTd2[k+2].text.split("\n")[0]
        score=allTd2[k+8].text.split("\n")[0]
        if ("/" in score) and ("--" not in score):
            totalPoints=score.split("/")[1]
            earnedPoints=score.split("/")[0]
        else:
            totalPoints="null"
            earnedPoints="null"
        date=allTd2[k].text.split("\n")[0]
        cat=allTd2[k+1].text.split("\n")[0]
        hash=sha256((assignmentName+score+date+cat).encode("utf-8")).hexdigest()

        grades[hash]=({
        'name': assignmentName,
        'rawScore': score,
        'earnedPoints' : earnedPoints,
        'totalPoints': totalPoints,
        'date' : date,
        'category' : cat,

        })
        k+=11
        num+=1
    return grades
def getClassNamesAndLinks(driver):
    classNames=[];
    allTd=driver.find_elements_by_css_selector("#content-main>div>table>tbody>tr>td");
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
    return {"classNames":classNames, "links":links}



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



def verifyUsernamePassword(usr,pw):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options, executable_path="geckodriver.exe")
    signOn(driver, usr, pw)
    try: 
        driver.find_element_by_css_selector(".feedback-alert")
    except:
        return True
    return False

