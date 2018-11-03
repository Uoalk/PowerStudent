import requests, hmac, base64, json, os
from bs4 import BeautifulSoup
from hashlib import md5



dir = os.path.dirname(__file__)

class cla():
    name = ''
    teacher = ''
    gradeS1 = ''
    gradeS1Url = ''
    gradeS2 = ''
    gradeS2Url = ''

classes = []
temp = cla()

def getGrades(usr, rawPw, debugPrint):
    url = "https://powerschool.kentdenver.org/guardian/home.html"
    s = requests.Session()
    home = s.get(url)
    homeHT =  BeautifulSoup(home.text, "html5lib")
    key = homeHT.find('input', {'name':'contextData'})["value"]
    tok = homeHT.find('input', {'name':'pstoken'})["value"]
    pw = md5(str(rawPw)).digest().encode('base64')[:-3]
    pw = hmac.new(str(key), pw, md5).hexdigest()
    db = base64.b64encode(hmac.new(str(key), rawPw.lower(), md5).digest()).decode("base64").encode("hex")[:-3]
    ses = str(s.cookies.get_dict()['JSESSIONID'])
    payload = "pstoken=" + tok + "&contextData=" + key + "&dbpw=" + db + "&translator_username=&translator_password=&translator_ldappassword=&returnUrl=&serviceName=PS%2BParent%2BPortal&serviceTicket=&pcasServerUrl=%252F&credentialType=User%2BId%2Band%2BPassword%2BCredential&ldappassword=" + rawPw + "&account=" + usr + "&pw=" + pw + "&translatorpw="
    headers = {
        'cookie': "_ga=GA1.2.2121594659.1493402183; uiStateNav=expanded; uiStateCont=null; lastHref=https%3A%2F%2Fpowerschool.kentdenver.org%2Fguardian%2Fhome.html; Alert=done; JSESSIONID=" + ses,
        'origin': "https://powerschool.kentdenver.org",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.8",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'cache-control': "no-cache",
        'referer': "https://powerschool.kentdenver.org/public/home.html",
        'connection': "keep-alive",
        'postman-token': "88d72377-3663-9480-84c7-b2c2785601fb"
        }
    grade = s.post( url, data=payload, headers=headers)
    gradeHT =  BeautifulSoup(grade.text, "html5lib")
    allInfo = gradeHT.find_all('td')
    temp = cla()
    for i in range(0, len(allInfo)):
        if(allInfo[i].find('a', {'class':'button mini dialogM'}) != None):
            temp.name = (allInfo[i].contents[0])
            temp.teacher = allInfo[i].contents[3][1:]
            if allInfo[i+1].find('a') != None:
                if "scores.html?frn=" in str(allInfo[i+1].find('a')['href']):
                    temp.gradeS1 = allInfo[i+1].contents[0].text
                    temp.gradeS1Url = allInfo[i+1].find('a')['href']
            if allInfo[i+2].find('a') != None:
                if "scores.html?frn=" in str(allInfo[i+2].find('a')['href']):
                    temp.gradeS2 = allInfo[i+2].contents[0].text
                    temp.gradeS2Url = allInfo[i+2].find('a')['href']
            classes.append(temp)
            temp = cla()
    if debugPrint == True:
        print("key : " + key)
        print("tok : " + tok)
        print("pw : " + pw)
        print("db : " + db)
        print("\nClasses: ")
        for i in classes:
            print ("Class : " + i.name + "\nTeacher : " + i.teacher + "\nS1 Grade : " + i.gradeS1 + "\nS1 Grade Url : " + i.gradeS1Url + "\nS2 Grade : " + i.gradeS2 + "\nS2 Grade Url : " + i.gradeS2Url)
    return classes

getGrades("gfitez20","k31415",True)

"""
@api {get} /api/v1/getGrades/?usr=USERNAME&pas=PASSWORD Request User information
@apiName getGrades
@apiGroup User
@apiParam usr PowerSchool Username
@apiParam pas PowerSchool Password
@apiSuccessExample {json} Success-Response:
                {
                "grades":1,
                "data":[
                    {
                    "name":"Class Name",
                    "gradeS2":"A+",
                    "gradeS1":"A-",
                    "gradeS2Url":"scores.html?frn=012345&begdate=01/01/2000&enddate=07/01/2000&fg=C2",
                    "teacher":"Smith, Joe",
                    "gradeS1Url":"scores.html?frn=012345&fg=S1"
                    }
                }
"""


