from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime 
rooms = { # favoring the nicer/bigger rooms
    2134 : "Study Room", 
    2124 : "Study Room",
    2140 : "Study Room",
    2142 : "Zoom Room",
    2144 : "Connect to Display",
    2122 : "Study Room",
    2126 : "Study Room",
    2128 : "Study Room",
    2130 : "Study Room",
    2132 : "Study Room",
    2136 : "Study Room",
    2138 : "Study Room"
}

def book(email, password, requests):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.get("https://umich.libcal.com/reserve/shapirorooms")
    driver.implicitly_wait(10)
    for request in requests:
        request = request.split()
        date = request[0]
        del request[0]
        for room in list(rooms.keys()):
            for time in request:
                title = create_room_title(date, time, room)
                try:
                    driver.find_element(By.XPATH, title).click()
                except:
                    print("Not Found")
                    continue 


    

def create_room_title(date, time, room):
    title = '//*[@title="'
    title += str(time) + ' '

    # properly formatting date from user inputted date
    date = datetime.strptime(date, '%m/%d/%Y')
    date = date.strftime('%A, %B %d, %Y')
    title += date.replace(" 0", " ") # remove leading 0s
    

    title += ' - 2nd Floor - '
    title += str(room) + ' - ' 
    title += rooms[room] + ' - '
    title += 'Available'
    title += '"]'
    return title



def login(email, password):
    pass
