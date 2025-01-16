import os
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class CommentFrameMaker:
    def __init__(self, RedditData):

        self.datafile = RedditData
        try:
            with open (RedditData, "r") as f:
                self.data = json.load(f)
                self.base_directory = self.data["directory_data"]["CommentFrame"]
        except (FileNotFoundError, json.JSONDecodeError):
            print("Please pass in RedditMakerData file")

    def get_title(self):
        title_of_submission = self.data["story_data"]["title"]
        print("Obtained title of submission")
        return title_of_submission
            

    def modify_CommentHTML(self,title_of_submission):
        with open(os.path.join(self.base_directory,"CommentFrameHTML.html"), "r", encoding="utf-8") as commentFrameHTMLfile:  
            #We must open the file to read and access its contents, and the encoding parameter specifies which encoding to use. 
            #By choosing Unicode encoding, we ensure that Python can correctly interpret the characters in the file, 
            #especially since Unicode supports a wide range of characters. 
            #This is important because the HTML document may contain special or non-ASCII characters that Python’s default encoding may not recognize, 
            #and using Unicode allows the interpreter to accurately handle those characters.
            soup = BeautifulSoup(commentFrameHTMLfile, 'html.parser')
            print("Intialized Parser object")
            
            target_div = soup.find('div', id='caption') #find the caption div
            print("Found location of input caption")
            target_div.string = title_of_submission     #change string in div

        with open(os.path.join(self.base_directory,"CommentFrameHTML.html"), "w", encoding="utf-8") as RevisedCommentFrameHTMLfile:  
            RevisedCommentFrameHTMLfile.write(soup.prettify())
            print("Inserted title of submission to input caption")

    def html_to_png(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
        driver = webdriver.Chrome(options=options)

        # Specify the correct path to your HTML file
        path = os.path.join(self.base_directory,"CommentFrameHTML.html")
        driver.get(f'file:///{path}')
        print("Processing to HTML to PNG...")
        #Wait for the page to load
        time.sleep(2)

        #Find a the div element to take picture of; if not selenium will take a picture of whole HTML page which include a lot of white space that we do not want 
        div_element = driver.find_element(By.CLASS_NAME, "post-container")
        # Take a screenshot of the specific div as a base64 string
        div_element.screenshot(os.path.join(self.base_directory,'CommentFrame.png'))
        driver.quit()
        print("Finished! CommentFrame.png has been created.")

    def createCommentFrame(self):
        self.modify_CommentHTML(self.get_title())
        self.html_to_png()


if __name__ == "__main__":
    CommentFrameMaker(r'C:/Users/Joseph/Documents/vscode/Reddit Project/Reddit Request/RedditMakerData.json').createCommentFrame()