import configparser
import json

import gradeGetter
import emailer


config = configparser.ConfigParser()
config.read('account.config')


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

def getChanges(old,new):
    changes="";
    oldKeys=old.keys()
    for key in new.keys():
        if key not in oldKeys:
            changes+="New class: "+key+"<br>"
        else:
            for assignment in new[key]:
                if assignment not in old[key]:
                    changes+="<b>New grade in "+key+":</b> "+new[key][assignment]["name"]+":"+new[key][assignment]["rawScore"]+"<br>"


    return changes

def updateAndEmail():
    gradeData=gradeGetter.getGrades(config['DEFAULT']["powerschoolUsername"], config['DEFAULT']["powerschoolPassword"])
    changes=getChanges(getStoredGrades(), gradeData)
    print(changes)
    if changes!="":
        emailer.send_email(config['DEFAULT']["emailAddress"],config['DEFAULT']["emailPassword"],config['DEFAULT']["sendEmailTo"],"Powerschool update",changes)
    with open('gradeData.json', 'w') as file:
        json.dump(gradeData, file, indent=2)
updateAndEmail()