#This file contains the functions needed to alert a user when theyre grade has been changed.
#In a real situation, this would be run for all users on a loop so they could get constant updates

import main
import json
import encryption
import emailer
import gradeGetter
import configparser

masterPw="12345"

#Given a users data from the names.json file, this function will retrieve their grades
def getGradesFromUserData(userData):
    pw=encryption.decrypt(userData["password"],masterPw,userData["salt"])
    return gradeGetter.getGrades(userData["username"],pw)
    # while(True):
    #     changes = main.getChanges(main.getStoredGrades(), main.gradeGetter.getGrades(username,password))
    #     gradeData = main.gradeGetter.getGrades(username,password)
    #     if main.getChanges(main.getStoredGrades(), main.gradeGetter.getGrades(username,password)) != "":
    #         pass
    #     else:
    #         main.emailer.send_email(email, emailPassword, email,"Powerschool update", changes)
    #         with open('gradeData.json', 'w') as file:
    #             json.dump(gradeData, file, indent=2)

#while(True):
    #updateAll()

#The main block of this file reads in a users data, gets their new grades, finds the changes, updates the cached grades, and emails them
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('account.config')

    #read the users data
    userData=json.loads(open("names.JSON").read())

    #get the users grades
    grades=getGradesFromUserData(userData["gfitez20"]);
    
    #see changes from the cached grades
    changes=main.getChanges(userData["gfitez20"]["cachedGrades"],grades)


    #update users cached grades
    userData["gfitez20"]["cachedGrades"]=grades
    print(changes)

    #email them if there are grade changes
    if changes!="":
        emailer.send_email(config['DEFAULT']["emailAddress"],config['DEFAULT']["emailPassword"],userData["gfitez20"]["email"],"Powerschool update",changes)

    #store the new grades
    with open('names.json', 'w') as file:
        json.dump(userData, file, indent=2)
