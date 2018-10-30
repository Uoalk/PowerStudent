import main
import json

def autoUpdate():

    with open('names.JSON', 'r') as file:
        data = json.load(file)

    print(data)

    # while(True):
    #     changes = main.getChanges(main.getStoredGrades(), main.gradeGetter.getGrades(username,password))
    #     gradeData = main.gradeGetter.getGrades(username,password)
    #     if main.getChanges(main.getStoredGrades(), main.gradeGetter.getGrades(username,password)) != "":
    #         pass
    #     else:
    #         main.emailer.send_email(email, emailPassword, email,"Powerschool update", changes)
    #         with open('gradeData.json', 'w') as file:
    #             json.dump(gradeData, file, indent=2)
