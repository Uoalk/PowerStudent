import main
import json
import encryption

def updateAll():

    with open('names.JSON', 'r') as file:
        names = json.load(file)

    print(names)

masterPw="12345"


def getGradesFromUserData(userData):
    pw=encryption.decrypt(userData["password"],masterPw,userData["salt"])
    print(pw)
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
if __name__ == "__main__":
    userData=json.loads(open("names.JSON").read())
    getGradesFromUserData(userData["gfitez20"]);
