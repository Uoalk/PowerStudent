# PowerStudent

# HOW TO GET POWERSTUDENT WORKING

What you need to have downloaded

  -FireFox: https://mzl.la/2FJrvvO

  -GeckoDriver: https://bit.ly/2joYOJD

Additionally, you should install selenium:
  -Go to your command prompt and install selenium

Now for the rest of the dependencies, just open command prompt and type:
```
  -pip install configparser

  -pip install flask

  -pip install encryption

  -pip install MIMEText

  -pip install BeautifulSoup
```

![picture](https://github.com/Uoalk/PowerStudent/blob/master/images/ReadMe3.jpg)

First, pull from the GitHub: https://bit.ly/2TSyxSa

Second, open command prompt. Then, access the PowerStudent folder. Once you're in the folder, type: python server.py

![picture](https://github.com/Uoalk/PowerStudent/blob/master/images/ReadMe1.jpg)

Go to that link, click register, and you should be able to input your PowerSchool username, password, and the email that you want your notifications to go to.

![picture](https://github.com/Uoalk/PowerStudent/blob/master/images/ReadMe2.jpg)

However, for the email notifier to work, the program must be able to log into your email: https://myaccount.google.com/lesssecureapps
![picture](https://github.com/Uoalk/PowerStudent/blob/master/images/ReadMe4.jpg)

YAY! Now it should work!


Versions:
1.0
The very first iteration was much more of a proof of concept. The code is able to scrape grades and notify users on an individual level. With this version, a user would have to manually run the code on their computer in order to be notified from their.

2.0
Version 2 has formal website and server for users to sign up for the application. It now has the basic functionality that a normal user would be able to use, without having to interact with any files, terminal commands, or code.

3.0
This iteration completely overhauled the back end of the system. The passwords are now stored in a semi-secure way, using a master password and a salt. It also overhauled the way in which grades were stored by using hashes so the system is more robust in it's handling of complex grade changes such as updates, deletions, category changes, and out of order insertions.


Files :
emailer.py: Contains all the functions to send emails
account.config: stores private username and password information to send emails through gmail
encryption.py: contains all the functions related to encrypting and decrypting passwords
gradeAlerter.py: contains the functions needed to alert a user when their grade has been changed. It also serves as the primary file the demo currently.
gradeData.json: stores all the cached grade data
gradeGetter.py: contains all of the webscraping functions to retreive the grades for a user
main.py: contains all functions that don't necessarily fit into another file. It also contains many outdated functions from the prototypes.
server.py: runs the flask server for users to sign up and see grades


Primary bugs:
- Not compatible with the new powerschool format that Mr. Clement uses.
- The monthly, weekly, daily, and ASAP notification settings are not fully implemented as the grade Alerter currently has to be run manually.
