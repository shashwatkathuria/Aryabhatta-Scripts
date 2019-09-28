import requests, re
from bs4 import BeautifulSoup
from getpass import getpass

baseUrl = "http://intra.iitj.ac.in:8080/Aryabhatta/"
loginUrl = "login.do"
attendanceUrl = "attendanceReport.do"

courses = ['CS311', 'CS312', 'CS313', 'CS314', 'HS311', 'HSL4020']
temp = []
for course in courses:
    temp.append((course,"attendanceViewStudent.do?code=" + course + "&opt=View" ))
courses = temp

AttendancePattern = re.compile("^[0-9]+ / [0-9]+ %$")

username = "kathuria.1"

password = getpass("Enter password for " + username + " : ")

payload = {
    "userid" : username,
    "password" : password
}

def main():
    requestSession = requests.session()
    loginResult = requestSession.post(
        baseUrl + loginUrl,
        data = payload,
        headers = dict(referer = baseUrl + loginUrl)
    )
    attendanceResult = requestSession.get(baseUrl + attendanceUrl)
    if attendanceResult.status_code != 200:
        print("Invalid credentials. Login again.")

    else:
        print("=================")
        print("ATTENDANCE REPORT")
        print("=================")
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