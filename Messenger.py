from Driver import Driver
import pandas as pd

class Messenger:
    def __init__(self,csv_file):
        self.csv_file = csv_file

        self.subject_msg = 'Restaurant Industry Market Research'
        self.body_msg = '''Hello Mx. %s,

I am a student seeking to learn more about the restaurant industry. Specifically, I want to learn more about expenses incurred from servers dropping plates.

May I have 10 minutes of your time to interview you about your experiences as %s at %s?'''

        self.driver = Driver()

    def loadCSV(self,tag,num_pages):
        links = self.driver.getAllLinks(tag,num_pages)
        pd.DataFrame({'name': links}).to_csv(self.csv_file, index=False)

    def message(self):
        links = pd.read_csv(self.csv_file)

        for row in links.iterrows():
            link = row[1]['name']
            self.driver.message(link,self.subject_msg,self.body_msg)

        # link = links.iloc[11]['name']
        # self.driver.message(link,self.subject_msg,self.body_msg)

if __name__=='__main__':
    messenger = Messenger('links.csv')

    # messenger.loadCSV('restaurant',2)

    messenger.message()

