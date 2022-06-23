/*
 * Copyright 2022 eldritchdreamer.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
 * either express or implied. See the License for the specific language
 * governing permissions and limitations under the License.
 */

import requests
import os
import tweepy
import random
import base64
from time import sleep

TEMP_FILENAME = 'temp.png'
POST_MESSAGE = "%%Your post message here%%" # text message to be added to the possts
DELAY_BETWEEN_POSTS_SECONDS = 60*60 # sets up delay between post attempts
QUERIES = ['%%query for image1%%', '%%query for image 2%%, '%%query for image N%%] # queries for Dall-E mini by which images will be generated, picking 1 randomly at each iteration
MAX_ITERATIONS = -1 # max posting attempts, leave negative for infitine loop
MAX_RETRIES = 10 # max attempts to get images from dalle-mini

def twitter_api():
	auth = tweepy.OAuth1UserHandler(
   	"%% YOUR TWITTER APP API KEY %%", "%% YOUR TWITTER APP API KEY SECRET %%",
   	"%% YOUR TWITTER ACCESS KEY SECRET%%", "%% YOUR TWITTER ACCESS KEY SECRET%%"
	)
	api = tweepy.API(auth)
	return api

def tweet_image(query, message):
    api = twitter_api()
    if not getDalleMiniImage(query):
        print("Didn't get image")
        return
    try:
    	api.update_status_with_media(message, TEMP_FILENAME)
    	print("Posted")
    except Exception as e:
        print(e)
        print("Posting failed")
    os.remove(TEMP_FILENAME)

def getDalleMiniImage(query):
	url = 'https://bf.dallemini.ai/generate'
	myobj = {'prompt': query}
	headers = {
    		"Accept": "application/json",
    		"Accept-Language": "en-US,en;q=0.9,ru-UA;q=0.8,ru;q=0.7,uk;q=0.6", 
    		"Connection": "keep-alive",
    		"Content-Type": "application/json",
    		"Sec-Fetch-Dest": "empty",
    		"Sec-Fetch-Mode": "cors",
    		"Sec-Fetch-Site": "cors",
    		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    		"sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\"",
    		"sec-ch-ua-mobile": "?0",
    		"sec-ch-ua-platform": "\"Windows\""    
		}


	response = requests.post(url, json = myobj, headers=headers)
	cntr = 0
	while response.status_code != 200 and cntr < MAX_RETRIES:
		print("Status code" + str(response.status_code) + "Going for retry")
		cntr+=1 
		response = requests.get(url)
	if response.status_code != 200:
		print("Status code" + str(response.status_code) + ", retries exhausted")
		return False

	try:
		respJson= response.json()
		x = random.choice(respJson['images'])
		with open(TEMP_FILENAME, "wb") as fh:
			fh.write(base64.b64decode(x))
		return True
	except Exception as e:
		print(e)
		return False
	
count = 0
while count < MAX_ITERATIONS or MAX_ITERATIONS < 0:
	print("Iteration " + str(count))
	count+=1
	tweet_image(random.choice(QUERIES), POST_MESSAGE)
	if count < MAX_ITERATIONS or MAX_ITERATIONS < 0:
		print("sleeping")
		sleep(DELAY_BETWEEN_POSTS_SECONDS)
