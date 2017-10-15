# Scrape-youtube
# Installation
1 - open your shell and type 'git clone https://github.com/a7mad3akef/inmobly-akef.git'

2 - cd scrape-youtube

3 - virtualenv . (you can install it by 'sudo pip install virtualenv' if it wasn't installed)

4 - source bin/activate

5 - pip install -r requirements.txt

6 - export PAFY_BACKEND=internal

7 - python create_db.py

8 - python app.py

9 - open http://localhost:9999/ on your browser

## Design
I tried to make it run in the shell but the sign (&) made a problem, so I decided to make its interface as a webpage.
I used Flask as web frame work and Sqlite as a database, I also used Ajax to deliver a good user experience.

## WorkFlow
After installation and open the webpage you will find text input with backend validation that you will enter one of the two formats, then it differentiate between the two formats, also get the status of your checkbox input to decide if it will download the videos or not.

After it determined the link either playlist or channel, there are two functions in the backend (get_channel_info) and (get_playlist_info) to extract videos' ids from YouTube Data Api, each function checks if the user have enterd this link before to retrieve it from the database and doesn't wait to avoid network latency when retrieving it from YouTube Api again.

After getting the videos' ids we call (get_video_info) function to retrieve data from YouTube Api and download the images and save :
a. Video URL
b. Title
c. Duration
d. Views
e. Thumbnail image path (which i downloaded before)
f. Original full-sized image (which i downloaded before)
it also checks for download_flag to decide download videos or not.

Then retrieve some data about your url's videos and show them after the request is done on the webpage using jquery

