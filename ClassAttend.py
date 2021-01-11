# Bot to go to learn.niituniversity and open the current class.

#%% Import Statements
from selenium import webdriver    
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import getpass
import time

#%% URL
url = 'https://learn.niituniversity.in/#/signin'

#%% Section to Collect Credentials if it dosen't exist.
while  True:
    try:
        with open('credentials.txt','r+') as file:
            Lines = file.readlines()
            Lines = [i.replace('Username: ','').replace('Password: ','').strip() for i in Lines]
            usn = Lines[0]
            password = Lines[1]
            break
    except FileNotFoundError:
        usn = input("Enter Username:(Skip the @st.niituniversity.in part) ")
        password = getpass.getpass()
        with open('credentials.txt','w+') as file:
            file.write(f"Username: {usn}\n")
            file.write(f"Password: {password}\n")


#%% Bot
prefs = {
    "download_restrictions": 3,
}
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs",prefs)



chrome = webdriver.Chrome(ChromeDriverManager().install(),options=options)    #Write the browser which you are using currently.
chrome.get(url)


chrome.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/form/div/a/img').click()   #Login Btn Click

chrome.find_element_by_xpath('//*[@id="identifierId"]').send_keys(usn)              #Enter Username
time.sleep(1)

chrome.find_element_by_xpath('//*[@id="identifierNext"]/div/button').send_keys(Keys.ENTER)  # Next Button
time.sleep(2)

chrome.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password) #Enter Password
chrome.find_element_by_xpath('//*[@id="passwordNext"]/div/button').send_keys(Keys.ENTER)        #Next Button
time.sleep(10)

#%% Validate Time and Enter the Current Class
Time = dict()
for i in range(0,10):
    try:
        clsTime = chrome.find_element_by_xpath(f'//*[@id="root"]/div[2]/div[2]/div[2]/div[2]/div[{i}]/div[2]/p[3]')
        temp = clsTime.text.replace(' (IST)','').replace(' AM','').replace(' PM','').replace(':00','').replace(' - ',',').split(',')
        Time[i+1] = [('start',int(temp[0])),('end',int(temp[1])),chrome.find_element_by_xpath(f'//*[@id="root"]/div[2]/div[2]/div[2]/div[2]/div[{i}]/div[2]/a')]
    except:
        pass
    
currentTime = time.localtime().tm_hour
if currentTime > 12:
    currentTime = currentTime - 12

if len(Time) != 0:
    for i in range(0,10):
        try:
            if Time[i][0][1] < Time[i][1][1]:
                if Time[i][0][1] <= currentTime and Time[i][1][1] > currentTime:
                    Time[i][2].click()
                    Window_List = chrome.window_handles
                    chrome.switch_to_window(Window_List[-1])
                    attended = True
                    #time.sleep(1)
                    #chrome.find_element_by_xpath('//*[@id="zoom-ui-frame"]/div[2]/div/div[1]/div').click()
                    break
            elif Time[i][0][1] > Time[i][1][1]:
                if Time[i][0][1] <= currentTime:
                    Time[i][2].click()
                    Window_List = chrome.window_handles
                    chrome.switch_to_window(Window_List[-1])
                    attended = True
                    #time.sleep(1)
                    #chrome.find_element_by_xpath('//*[@id="zoom-ui-frame"]/div[2]/div/div[1]/div').click()
                    break
        except:
            pass

else:
    print("Either there is no lecture going on currently or Lectures Are Over For Today!!!")
