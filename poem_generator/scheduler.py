#	Scheduler for group for VK

import core
import art
import mind_db

import requests
import sys
import time
import datetime
import os
import random

GID = 000000000			# ID of VK Group
TOKEN = "AAAAAAAAAAA" 	# Vk token here
ART_FOLDER = "ARTS_1"	# Folder with arts

DELAY = 10800
POEM_TYPES = {"poem": 8, "hokku": 1}
ART_TYPES = {"russian": 4, "gallery": 8, "collection": 4}

def get_last_postponed():
	while True:
		try:
			get = requests.get("https://api.vk.com/method/wall.get", params = {"access_token": TOKEN, 'v': 5.21, "owner_id": -GID, "filter": "postponed", "count": 100})
			break
		except:
			print(f"Error on getting last postponed: {sys.exc_info()}")
			time.sleep(5)

	get = get.json()["response"]["items"]
	if len(get) == 0: return 0
	else: return get[-1]["date"]

def postpone_post(text, attachments, post_date):
	while True:
		try:
			get = requests.get("https://api.vk.com/method/wall.post", params = {"access_token": TOKEN, 'v': 5.21, "owner_id": -GID, "from_group": "1", "message": text, "attachments": attachments, "publish_date": post_date})
			break
		except:
			print(f"Error on postponing: {sys.exc_info()}")
			time.sleep(5)
	return get.json()

def val_from_dict(powers):
	summa = 0
	for x in powers.values(): summa += x
	target = random.randint(1, summa)

	for key, val in powers.items():
		target -= val
		if target <= 0: return key
	return list(powers.keys())[-1]

def generate_post_poem(poem_type):
	if poem_type == "poem":
		text = core.generate_structure(core.mind_db.get_structure())
	if poem_type == "hokku":
		core.mind_db.config_db("hokku_mind.db")
		text = core.generate_structure_hokku(core.mind_db.get_structure_custom())
		core.mind_db.config_db("mind.db")

	return text

def generate_post_art(art_type):
	if art_type == "russian":
		art_info = art.get_russians()
		art_name = art.save_art(art_info, ART_FOLDER)

	if art_type == "gallery":
		art_info = art.get_gallery()
		art_name = art.save_art(art_info, ART_FOLDER)

	if art_type == "collection":
		art_info = art.get_art()
		art_name = art.save_art(art_info, ART_FOLDER)

	try: os.rename(ART_FOLDER + "\\" + art_name, ART_FOLDER + "\\" + "WORKING_FILE.jpg")
	except FileExistsError:
		os.remove(ART_FOLDER + "\\" + "WORKING_FILE.jpg")
		os.rename(ART_FOLDER + "\\" + art_name, ART_FOLDER + "\\" + "WORKING_FILE.jpg")

	while True:
		try:
			vk_photo = art.loadPhotoVk(ART_FOLDER + "\\" + "WORKING_FILE.jpg", art_name[:-4])
			break
		except requests.exceptions.ProxyError:
			print("ProxyError while loading photo, trying again")
			time.sleep(3)
	while True:
		try:
			os.rename(ART_FOLDER + "\\" + "WORKING_FILE.jpg", ART_FOLDER + "\\" + art_name)
			break
		except PermissionError:
			print("PermissionError, waiting")
			time.sleep(3)

	return vk_photo


os.system("CLS")
topost_data = get_last_postponed()
if topost_data == 0: topost_data = int(input("Post date:")) - DELAY

topost_data += DELAY

if len(sys.argv) > 1 and sys.argv[1] == "gen":
	poem_type = val_from_dict(POEM_TYPES)
	art_type = val_from_dict(ART_TYPES)

	print(f"[{time.strftime('%H:%M:%S')}] Generating post. Poem_Type: {poem_type}. Art_Type: {art_type}")
	print(f"[{time.strftime('%H:%M:%S')}] Generating text")
	post_text = generate_post_poem(poem_type)
	
	print(post_text)

	sys.exit()

while True:
	print(f"\n\tNext post in {datetime.datetime.fromtimestamp(topost_data)}")
	poem_type = val_from_dict(POEM_TYPES)
	art_type = val_from_dict(ART_TYPES)

	print(f"[{time.strftime('%H:%M:%S')}] Generating post. Poem_Type: {poem_type}. Art_Type: {art_type}")
	print(f"[{time.strftime('%H:%M:%S')}] Generating text")
	post_text = generate_post_poem(poem_type)
	print(f"[{time.strftime('%H:%M:%S')}] Getting art")
	
	while True:
		try:
			post_art = generate_post_art(art_type)
			break
		except: pass

	print(f"[{time.strftime('%H:%M:%S')}] Posting . . . Poem: {post_text[:15]}, Art: {post_art}")
	try:
		if "post_id" in postpone_post(post_text, post_art, topost_data)["response"]:
			topost_data += DELAY
		else:
			continue
	except:
		print("Something went wrong while posting...")
