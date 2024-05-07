from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime 
import messenger 

booking_site = "https://umich.libcal.com/reserve/shapirorooms"

 # favoring the nicer/bigger rooms
rooms = {
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
    driver.get(booking_site)
    driver.implicitly_wait(3) # waiting for site to load

    logged_in = False

    for request in requests:
        request = request.split()
        finished_day = False
        date = request[0]
        del request[0]
        for room in list(rooms.keys()):
            for time in request:
                title = create_room_title(date, time, room)
                print(title)

                if not book_room(driver, title): # could not book room
                    break

                if not logged_in: # check if we previously logged 
                    if not login(driver, email, password): # check if the login failed
                        messenger.send_email(email, "Login Failed", 
                        '''
                        An error has occured while logging in. Either you did not
                        authenticate in time or the password you have entered is
                        not correct.
                        ''')
                        return
                    logged_in = True

                print(title)
                if not confirm_booking(driver): # cannot book anymore rooms for this day
                    finished_day = True
                    break
            
            if finished_day: # cannot book anymore rooms for this day
                break
    
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



def login(driver, email, password):
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "loginSubmit").click()

    # wait a minute for authentication 
    driver.implicitly_wait(120)

    try:
        driver.find_element(By.ID, "dont-trust-browser-button").click()
    except:
        return False
    
    return True


def book_room(driver, title):
    for i in range(3):
        try: #attempt to book a room
            driver.find_element(By.XPATH, title).click()
        except:
            if i == 2: # no more pages to move to
                driver.refresh()
                return False
        
            # move to next page
            driver.find_element(By.XPATH, '//*[@id="eq-time-grid"]/div[1]/div[1]/div/button[2]').click()
    
    driver.implicitly_wait(3)
    driver.find_element(By.NAME, "submit_times").click()
    driver.implicitly_wait(3)
    return True

def confirm_booking(driver):
    driver.find_element(By.ID, "nick").send_keys("Study")
    driver.find_element(By.ID, "btn-form-submit").click()
    driver.implicitly_wait(3)

    # checking if booking failed
    try:
        driver.find_element(By.CLASS_NAME, "btn btn-primary").click()
    except:
        driver.find_element(By.ID, "nick").clear()
        driver.implicitly_wait(1)
        driver.find_element(By.XPATH, '//*[@id="s-lc-public-bc"]/div/nav/ol/li[3]/a').click()
        driver.implicitly_wait(10)
        return False

    return True

#trust-browser-button
book("janajar", "Haideralikadhim3!", ["5/8/2024 2:00pm"])