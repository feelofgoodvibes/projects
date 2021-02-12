# Getting arts from online gallery gallerix.ru

import random
import os
import requests
from bs4 import BeautifulSoup

PAINTERS_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_RUS']
hdr = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
forb = set(r'<>:"/\|?*')

GID = 170614536
TOKEN = "AAAAAAAAAAA" # Vk token here

def save_art(info, folder = ""):
	dest = info[1] + ".jpg"
	e = 0
	for c in dest:
		if c in forb:
			dest = dest[:e] + dest[e+1:]
			e -= 1
		e += 1
	file_name = dest
	if folder: dest = folder + "/" + dest

	try:
		with open(dest, "wb") as file:
			file.write(requests.get(info[0], headers = hdr, proxies = {'https':None,'http':None}).content)
	except FileNotFoundError:
		os.mkdir(folder)
		with open(dest, "wb") as file:
			file.write(requests.get(info[0], headers = hdr, proxies = {'https':None,'http':None}).content)

	return file_name


def get_art():
	painter = BeautifulSoup(requests.get(f"https://gallerix.ru/storeroom/letter/{random.choice(PAINTERS_LETTERS)}/", headers = hdr, proxies = {'https':None,'http':None}).text, "html.parser")
	painter = painter.find("p", class_ = "sr-pntrs").find_all("a")
	painter = random.choice(painter)

	painter_page = BeautifulSoup(requests.get("https://gallerix.ru" + painter["href"], headers = hdr, proxies = {'https':None,'http':None}).text, "html.parser")
	painter_page = painter_page.find_all("div", class_ = "pic")

	painting_url = random.choice(painter_page).find("a")["href"]

	painting_url = BeautifulSoup(requests.get("https://gallerix.ru" + painting_url, headers = hdr, proxies = {'https':None,'http':None}).text, "html.parser")
	painting_url = painting_url.find("img", id = 'xpic')

	return (painting_url["src"], painting_url["title"])


def get_gallery():
	main_page = BeautifulSoup(requests.get("https://gallerix.ru/a1/", headers = hdr, proxies = {'https':None,'http':None}).text, "html.parser")
	main_page = main_page.find_all("div", class_ = "panel-body")[0].find_all("div", class_ = "row")
	all_a = []
	for row in main_page: all_a.extend(row.find_all("a"))

	painter_url = random.choice(all_a)["href"]

	while painter_url == "/storeroom/": painter_url = random.choice(all_a)["href"]
	painter_page = BeautifulSoup(requests.get("https://gallerix.ru" + painter_url, headers = hdr, proxies = {'https':None,'http':None}).text, "html.parser")

	all_paintings = painter_page.find("div", class_ = "tab-content").find("div", id = "tab-1").find_all("div", class_ = "pic")
	painting_url = random.choice(all_paintings).find("a")["href"]
	painting_page = BeautifulSoup(requests.get("https://gallerix.ru" + painting_url, headers = hdr, proxies = {'https':None,'http':None}).text, "html.parser")
	image_url = painting_page.find("img", id = 'xpic')

	if image_url == None:
		all_paintings = painting_page.find("div", class_ = "tab-content").find("div", id = "tab-1").find_all("div", class_ = "pic")
		painting_url = random.choice(all_paintings).find("a")["href"]
		painting_page = BeautifulSoup(requests.get("https://gallerix.ru" + painting_url, headers = hdr, proxies = {'https':None,'http':None}).text, "html.parser")
		image_url = painting_page.find("img", id = 'xpic')

	return (image_url["src"], image_url["title"])

def get_russians():
	main_page = BeautifulSoup(requests.get("https://gallerix.ru/album/Russians", headers = hdr, proxies = {'https':None,'http':None}).text, "html.parser")

	all_authors = main_page.find("div", class_ = "tab-content").find("div", id = "tab-1").find_all("div", class_ = "pic")
	author_url = random.choice(all_authors).find("a")["href"]
	author_page = BeautifulSoup(requests.get("https://gallerix.ru" + author_url, headers = hdr, proxies = {'https':None,'http':None}).text, "html.parser")
	all_paintings = author_page.find("div", class_ = "tab-content").find("div", id = "tab-1").find_all("div", class_ = "pic")
	painting_url = random.choice(all_paintings).find("a")["href"]

	painting_page = BeautifulSoup(requests.get("https://gallerix.ru" + painting_url, headers = hdr, proxies = {'https':None,'http':None}).text, "html.parser")
	image_url = painting_page.find("img", id = 'xpic')

	return (image_url["src"], image_url["title"])

def loadPhotoVk(filename, caption):
	server = requests.get('https://api.vk.com/method/photos.getWallUploadServer', params = {"access_token": TOKEN, "v": 5.21, "group_id": GID}).json()
	server = server["response"]["upload_url"]
	photo_post = requests.post(server, files = {"photo": open(filename, "rb")}).json()
	photo_save = requests.get("https://api.vk.com/method/photos.saveWallPhoto", params = {"access_token": TOKEN, "v": 5.21, "group_id": GID, "photo": photo_post["photo"], "server": photo_post["server"], "hash": photo_post["hash"], "caption": caption}).json()
	return f'photo{photo_save["response"][0]["owner_id"]}_{photo_save["response"][0]["id"]}'
