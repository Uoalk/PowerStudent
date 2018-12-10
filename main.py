#This is a file for the broader functions that don't necessarily fit into another one of the files.
#These functions are mostly outdated but this was the original proof of concept

import configparser
import json

import gradeGetter
import emailer


config = configparser.ConfigParser()
config.read('account.config')


#Retrieve grades from a stored json file
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


#Takes two sets of grades and finds the differences
def getChanges(old,new):
    changes="";
    oldKeys=old.keys()
    for key in new.keys():
        #if there is a new class
        if key not in oldKeys:
            changes+="New class: "+key+"<br>"
        else:
            #now check if there are any new assignments in that class
            for assignment in new[key]:
                if assignment not in old[key]:
                    changes+="<b>New grade in "+key+":</b> "+new[key][assignment]["name"]+":"+new[key][assignment]["rawScore"]+"<br>"


    return changes


#gets a users grades, check for changes, and update them if there are any
def updateAndEmail():
    gradeData=gradeGetter.getGrades(config['DEFAULT']["powerschoolUsername"], config['DEFAULT']["powerschoolPassword"])
    changes=getChanges(getStoredGrades(), gradeData)
    print(changes)
    if changes!="":
        emailer.send_email(config['DEFAULT']["emailAddress"],config['DEFAULT']["emailPassword"],config['DEFAULT']["sendEmailTo"],"Powerschool update",changes)
    #save grades to file
    with open('gradeData.json', 'w') as file:
        json.dump(gradeData, file, indent=2)
