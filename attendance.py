# -*- coding: utf-8 -*-
"""
Created on Sun Sept 29 4:15:23 2019
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
courses = ['CS321', 'CS322', 'CS323', 'CS399', 'HS321', 'CSL7080', 'CSL7091']
temp = [(course,"attendanceViewStudent.do?code=" + course + "&opt=View" ) for course in courses]
courses = temp

# Pattern for attendance matching
AttendancePattern = re.compile("^[0-9]+ / [0-9]+[.]*[0-9]* %$")

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
    attendanceResult = requestSession.get(baseUrl + attendanceUrl)
    if attendanceResult.status_code != 200:
        print("Invalid credentials. Login again.")

    else:
        print("=================")
        print("ATTENDANCE REPORT")
        print("=================")
        # Scraping attendance page and appropriately printing attendance and
        # course title in console
        for course in courses:
            attendanceScraper = BeautifulSoup(requestSession.get(baseUrl + course[1]).content.decode(), "html.parser")
            courseTitle = attendanceScraper.find('h3', {'class' : 'blank1'})
            arr = attendanceScraper.find_all('td', {'align' : 'center'})
            attendances = []
            print(courseTitle.text)
            for element in arr:
                if AttendancePattern.match(element.text):
                    attendances.append(element.text)
            if len(attendances) == 0:
                print("No attendance data.")
            elif len(attendances) == 1:
                print("Lectures : " + attendances[0])
            elif len(attendances) == 2:
                print("Lectures : " + attendances[0])
                print("Lab      : " + attendances[1])
            print()
        print("=================")

if __name__ == "__main__":
    main()
