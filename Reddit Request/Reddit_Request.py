import json
import requests

class RedditAPIClient:
    def __init__(self, RedditData):

        self.datafile = RedditData
        try:
            with open (RedditData, "r") as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Please pass in RedditMakerData file")

        self.base_directory = self.data["directory_data"]["RequestInitalizer"]

    def authenticate(self):
        client_id = self.data["SystemInformation"]["key"]["Client_ID "]
        secret_key = self.data["SystemInformation"]["key"]["Secret_Key"]
        username = self.data["SystemInformation"]["login_info"]["username"]
        password = self.data["SystemInformation"]["login_info"]["password"]
        headers = self.data["SystemInformation"]["headers"]


        auth = requests.auth.HTTPBasicAuth(client_id, secret_key)
        data = {
            'grant_type': 'password',
            'username': username,
            'password': password
        }

    #.auth is a submodule of the request library              
    #HTTPBasicAuth is a method to send our credentails 
    #HTTPBasicAuth class takes the Client_ID and Secret_Key, and encodes them into a string
    #When you make the API request (e.g., requests.post()), the auth object is passed along with the request, automatically adding this Authorization header
   
    #user_data is body of our request. It contains the data used to log into our account. 
    #headers is the header of our request, it contains the data used to access the endpoint

        response = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
        if response.status_code == 200:
            token = response.json()["access_token"]
            headers["Authorization"] = f"bearer {token}"
            print("OBTAINED ACCESS TOKEN")

            with open(self.datafile, "r") as f:
                currentdata = json.load(f)        #load into py dict
                currentdata["SystemInformation"]["headers"] = headers    #update the key

            with open(self.datafile, "w") as f:
                json.dump(currentdata, f, indent=4)  #write dict back, this ensures only the target key is changed
        else:
            print(f"Error: {response.status_code}")
            print(response.json())

    def grab_story(self):

        subreddit = self.data['SystemInformation']['query']['subreddit']
        sort = self.data['SystemInformation']['query']['sort']
        params = self.data["SystemInformation"]["parms"]

        with open(self.datafile, "r") as f:
            currentdata = json.load(f)
            headers = currentdata["SystemInformation"]["headers"] 

        url = f'https://oauth.reddit.com/r/{subreddit}/{sort}/'
        API_Retu_Sub = requests.get(url, headers=headers, params=params)

        if API_Retu_Sub.status_code == 200:
            APIdata = API_Retu_Sub.json() 
            submissions = APIdata['data']['children']
            print("OBTAINED STORIES")
            return submissions
        
        else:
            print(f"Error: {API_Retu_Sub.status_code}")
            print(API_Retu_Sub.json())

    def load_ids(self):
        with open(self.datafile, "r") as f:
            currentdata = json.load(f)
            list_of_ids = currentdata.get('submission_id', [])  # Use .get() to provide a default value if key doesn't exist
            
            if isinstance(list_of_ids, list):  # Use isinstance to check the type
                return list_of_ids
            else:
                print("Starting fresh; either first time or id list got corrupted")
                list_of_ids = []
                return list_of_ids

    def check_submissions(self, submissions, list_of_ids):
        checked_submissions = []
        for submission in submissions:                                             #iterates directly over the elements 
            if submission['data']['id'] not in list_of_ids:                        #in operator iterates over each element of list_of_ids                   
                checked_submissions.append(
                    {"title": submission['data']['title'], 
                    "selftext": submission['data']['selftext'],
                    "id" : submission['data']['id']
                    })
        print("CHECKED SUBMISSIONS")
        return checked_submissions

  
            
    def filter_submissions(self, checked_submissions, list_of_ids):
        min = self.data["SystemInformation"]["length_submission"]["min_length"]
        max = self.data["SystemInformation"]["length_submission"]["max_length"]

        with open(self.datafile, "r") as f:
            currentdata = json.load(f)  # Load the data from the file

        for submission in checked_submissions:
            if len(submission["selftext"].split()) >= min and len(submission["selftext"].split()) <= max:
                currentdata['story_data'] = submission  # Update dictionary
                currentdata['submission_id'].append(submission["id"])  # Append to existing list
                break
    
        with open(self.datafile, "w") as f:
            json.dump(currentdata, f, indent=4)
 

    def enhance_submission(self):
        with open(self.datafile, "r") as f:
            currentdata = json.load(f)
            processed_story = currentdata["story_data"]

        while True:
            user_answer = input("Do you wish to enhance Reddit Submission? (Yes/No): ").strip().lower()
            if user_answer == "yes":
                print(processed_story["title"])
                print("Place the following prompt into ChatGPT for submission title.\nRevise the following Reddit story title to make it more captivating and attention-grabbing for a TikTok audience. Keep the revised title concise and similar in length to the original.")
                processed_story["title"] = input("Input the enhanced title here: ").strip()

                print(processed_story["selftext"])
                print("Place the following prompt into ChatGPT for submission title.\nEnhance the following Reddit story to make it more compelling and engaging while preserving the original tone. Use sensory detail and strong vocabulary to enhance the story. Correct all grammar errors, but retain and properly format any slang to ensure it feels natural and authentic. The goal is to elevate the story’s appeal while keeping it relatable and entertaining for the audience. Write in paragraph form.")
                processed_story["selftext"] = input("Input the enhanced story here: ").strip()

                currentdata["story_data"] = processed_story

                with open(self.datafile, "w") as f:
                    json.dump(currentdata, f, indent=4)
                print("Updated Submissioned data")
                print("Done")

                break
            elif user_answer == "no":
                print("Exiting the enhancement process.")
                print("Done")
                break
            else:
                print("Invalid input. Please enter 'Yes' or 'No'.")

    def run_RedditRequest(self):
        while True:
            self.authenticate()
            user_answer = input("Begin Generating? (Yes/No/Wait): ").strip().lower()
            if user_answer == "yes":
                submissions = self.grab_story()
                list_of_ids = self.load_ids()
                new_submissions = self.check_submissions(submissions, list_of_ids)
                self.filter_submissions(new_submissions, list_of_ids)
                self.enhance_submission()
                break
            elif user_answer == "wait":
                print("Waiting...")
            elif user_answer == "no":
                break
            else:
                print("Invalid input. Please enter 'Yes', 'No', or 'Wait'.")

if __name__ == "__main__":
    RedditAPIClient(r'C:/Users/Joseph/Documents/vscode/Reddit Project/Reddit Request/RedditMakerData.json').run_RedditRequest()