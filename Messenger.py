from Driver import Driver
import pandas as pd

class Messenger:
    def __init__(self,csv_file):
        self.csv_file = csv_file

        self.subject_msg = 'Dietetics Career Advice'
        self.body_msg = '''Hello Mx. %s,

My sister is an undergraduate studying dietetics and is looking for an internship this summer. She is new to the internship scene and doesn't have the resources to find an opportunity. I want to help her with that.

May I have 10 minutes of your time to chat about your professional journey as a dietician?'''

        self.driver = Driver()

    def loadCSV(self,tag,num_pages):
        links = self.driver.getAllLinks(tag,num_pages)

        # for debugging
        # for i,l in enumerate(links):
        #     print(i,l)

        pd.DataFrame({'name': links}).to_csv(self.csv_file, index=False)

    def message(self):
        links = pd.read_csv(self.csv_file)

        for row in links.iterrows():
            index = row[0]
            print(index)

            link = row[1]['name']
            self.driver.message(link,self.subject_msg,self.body_msg)

        # link = links.iloc[11]['name']
        # self.driver.message(link,self.subject_msg,self.body_msg)

if __name__=='__main__':
    messenger = Messenger('links.csv')

    # messenger.loadCSV('dietetics intern',5)

    messenger.message()

