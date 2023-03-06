# workflow (terminal):
# cd 'C:\Program Files\Google\Chrome\Application’
# `chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\ChromeProfile"`
# https://www.linkedin.com/feed/
# python3 .\driver.py

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# PATH = 'C:\Browser Drivers\chromedriver.exe'

class Driver():
    def __init__(self):
        self.URL = 'https://www.linkedin.com/search/results/people/?keywords=%s&origin=CLUSTER_EXPANSION&page=%s&sid=eoo'

        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(options=options)

    def fe(self,path):
        return self.driver.find_elements(By.XPATH,path)

    def goToPage(self,tag,index):
        self.driver.get(self.URL % (tag,index))

    def getProfileLinks(self):
        
        container = self.fe('//*[@id="main"]/div/div')[0]

        profiles = container.find_elements(By.TAG_NAME,'li')

        link = [profile.find_element(By.CLASS_NAME,'app-aware-link').get_attribute('href') for profile in profiles]
        return link

    def getAllLinks(self,tag,num_pages):
        links = []

        for i in range(1,num_pages+1):
            print('PAGE %s'%str(i))
            self.goToPage(tag,i)
            links += self.getProfileLinks()
        
        return links

    def getPersonalData(self):
        
        last_name = self.driver.find_element(By.CSS_SELECTOR,'h1.text-heading-xlarge').get_attribute('innerText').split(' ')[-1]
        
        data_container = []
        while not len(data_container):
            data_container = self.driver.find_elements(By.ID,'experience')

        data_container = self.driver.find_element(By.CSS_SELECTOR,'#experience + div + div').find_elements(By.TAG_NAME,'li')[0].find_elements(By.TAG_NAME,'span')

        data = [span.get_attribute('innerText') for span in data_container]

        data = list(filter(lambda span: span!=' ' and -1==span.find('\n'),data))
        data = list(dict.fromkeys(data))

        position = data[0]
        firm = data[1].split(' · ')[0]
        
        return last_name,position,firm

    def closeConversation(self):
        buttons = self.driver.find_elements(By.TAG_NAME,'button')

        buttons = list(filter(lambda btn:btn.get_attribute('innerText').find('Close your conversation')!=-1,buttons))

        # print([button.get_attribute('innerText') for button in buttons])

        for btn in buttons:
            btn.click()
    
    def message(self,profile_link,subject_msg,body_msg):
        self.driver.get(profile_link)

        last_name,position,firm = self.getPersonalData()

        # open message tab
        href_container = self.driver.find_elements(By.CLASS_NAME,'pvs-profile-actions')[1]
        message_href = href_container.find_elements(By.CLASS_NAME,'entry-point')
        
        # profile does not have 'message' button
        if not len(message_href):
            return

        message_href[0].find_element(By.TAG_NAME,'a').click()

        # LINKEDIN MUST BE > SPLIT SCREEN
        iter = 0
        message_container = []
        while not len(message_container):
            message_container = self.driver.find_elements(By.CLASS_NAME,'msg-inmail-compose-form-v2')
            
            # if person has already been messaged, return
            iter += 1
            if (iter > 5):
                self.closeConversation()
                return
            time.sleep(1)

        message_container = message_container[0].find_elements(By.XPATH,'./div')

        # get input fields
        subject = message_container[1].find_element(By.TAG_NAME,'input')
        body = message_container[2].find_element(By.TAG_NAME,'p')

        # hydrate input fields
        subject.send_keys(subject_msg)
        body.send_keys(body_msg % (last_name,position,firm))

        # submit
        send_btn = message_container[2].find_element(By.CSS_SELECTOR,'button.msg-form__send-button')
        # send_btn.click()      

if __name__=='__main__':
    driver = Driver()

    links = driver.getAllLinks('restaurant',2)

    print(len(links))
    print(links[0])