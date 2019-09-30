# -*- coding: utf-8 -*-
"""
Created on Sun Sept 29 4:48:57 2019
@author: Shashwat Kathuria
"""

# Importing required libraries
import requests, re
from bs4 import BeautifulSoup
from getpass import getpass

# Initializing required variables
baseUrl = "http://intra.iitj.ac.in:8080/Aryabhatta/"
loginUrl = "login.do"
attendanceUrl = "attendanceReport.do"
courses = ['CS311', 'CS312', 'CS313', 'CS314', 'HS311', 'HSL4020']
temp = [(course,"performanceReport.do?code=" + course + "&opt=View" ) for course in courses]
courses = temp

# Pattern for date(mentioned alongwith exam name in page) and marks matching
DatePattern = re.compile("[0-3][0-9]-[0-1][0-9]-2019")
MarksPattern = re.compile("^[0-9]+[.]*[0-9]*$")

username = "kathuria.1"
# Hidden input in console by getpass
password = getpass("Enter password for " + username + " : ")
payload = {
    "userid" : username,
    "password" : password
}

def main():

    # Initializing a session object
    requestSession = requests.session()

    # Logging in
    loginResult = requestSession.post(
        baseUrl + loginUrl,
        data = payload,
        headers = dict(referer = baseUrl + loginUrl)
    )

    # Checking if successfully logged in and required page opens correctly
    performanceResult = requestSession.get(baseUrl + attendanceUrl)
    if performanceResult.status_code != 200:
        print("Invalid credentials. Login again.")

    else:
        print("=================")
        print("MARKS REPORT")
        print("=================")
        # Scraping performance page and appropriately printing marks, exam details
        # and course title in console
        for course in courses:
            marksScraper = BeautifulSoup(requestSession.get(baseUrl + course[1]).content.decode(), "html.parser")
            courseTitle = marksScraper.find('h3', {'class' : 'blank1'})
            arr = marksScraper.find_all('td', {'align' : 'center'})
            marks = []
            exams = []
            print(courseTitle.text)
            for element in arr:
                # If Date Pattern appears in any substring of element,
                # replacing separator <br> with space using get_text function
                if DatePattern.search(element.get_text(separator=u' ')):
                    exams.append(element.get_text(separator=u' '))
                if DatePattern.match(element.text) or MarksPattern.match(element.text):
                    marks.append(element.text)

            if exams != [] and marks != []:
                marks = marks[1:]
                [print(performance[0] + " : " + performance[1]) for performance in zip(exams, marks)]
            else:
                print("No data.")
            print()
        print("=================")

if __name__ == "__main__":
    main()
