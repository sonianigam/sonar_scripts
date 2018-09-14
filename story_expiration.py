import requests
import re
import sys
import time
import pry

def main(argv):
    handle = argv[0]
    lookup(handle, 0)

def lookup(handle, hours):
    session = login()

    story = session.get(f'https://www.instagram.com/stories/{handle}/', allow_redirects=False)
    status_code = story.status_code
    #print(story.text)
    #print(story.content)

    if status_code != 200:
      error = requests.status_codes._codes[status_code][0]
      print(f'This story is no longer available.\n{status_code}: {error}')
    else:
      print(f'This story is still up!\n It has beeen up for *{hours} hours*')
      #the below is to check if the story remains up for a full 24 hours
      # if hours < 24:
      #   hours+=1
      #   time.sleep(1)
      #   lookup(handle, hours)
      # else:
      #   exit()

def login():
    start_session = requests.Session()
    credentials = {'username': 'ENTER IN HERE', 'password': 'ENTER IN HERE'}
    start_session.headers.update({'Referer': 'https://www.instagram.com/'})
    request = start_session.get('https://www.instagram.com/')

    start_session.headers.update({'X-CSRFToken': request.cookies['csrftoken']})

    response = start_session.post('https://www.instagram.com/accounts/login/ajax/', data=credentials, allow_redirects=True)
    response_data = bytes.decode(response.content)
    authenticated = bool(response_data.find('\"authenticated\": true'))

    if not authenticated:
        print("Login Failed.  Please check your credentials")
        exit()
    return start_session

if __name__ == '__main__':
    main(sys.argv[1:])
