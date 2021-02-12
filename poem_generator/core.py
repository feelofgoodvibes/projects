#!/usr/bin/python
# -*- coding: utf-8 -*-

# File for generating poems

import pymorphy2
import time
import random
from bs4 import BeautifulSoup
import requests
from os import system
import traceback

import mind_db

analyzer = pymorphy2.MorphAnalyzer()
rus_alph = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя1234567890 \n")
punct = set(",.—-!?:;")
glasnie = set("аеёиоуыэюя")
count_pos = {0 : "NOUN", 1 : "ADJF", 2 : "ADJS", 3 : "COMP", 4 : "VERB", 5 : "INFN", 6 : "PRTF", 7 : "PRTS", 8 : "GRND", 9 : "NUMR", 10 : "ADVB", 11 : "NPRO", 12 : "PRED", 13 : "PREP", 14 : "CONJ", 15 : "PRCL", 16 : "INTJ", 17 : "PNCT" ,18 : "None"}

class Line():
	def __str__(self):
		if self.words[0] in punct: self.words.pop(0)
		line = self.words[0]
		for e, word in enumerate(self.words[1:], 1):
			if word in punct:
				try:
					if self.words[e+1] in punct: continue
				except IndexError: pass
				if word == "-" or word == "—": line += " "
				line += word
			else: line += " " + word 

		return line

	def __init__(self, *words):
		self.words = list(words)
		self.hits = count_hits("".join(self.words))

	def __add__(self, word):
		self.words.append(word)
		self.hits += count_hits(word)
		return self

	def last(self):
		res = -1
		while self.words[res] in punct: res -= 1
		return self.words[res]

	def add_to_begin(self, word):
		self.words = [word, *self.words]
		self.hits += count_hits(word)
		return self

	def place_pnct(self, pnct, pos = 1):
		self.words.insert(pos, pnct)
		return self

def choose_val_list(info):
	summa = 0
	for x in info: summa += x
	target = random.randint(1, summa)

	for key, val in enumerate(info):
		target -= val
		if target <= 0:
			result = key
			break

	return result

def url_to_poem(url):
	poem_text = BeautifulSoup(requests.get(url).text, "html.parser").find("div", class_ = "entry-content poem-text")
	if '(adsbygoogle' in str(poem_text): poem_text = BeautifulSoup(str(poem_text)[:str(poem_text).index('(adsbygoogle')],'html.parser')
	poem_text = poem_text.find_all('p')

	text = ""

	for p in poem_text:
		for x in p:
			if x.string == None: text += '\n'
			else: text += x.string.strip()
		text += '\n\n'

	text = text.strip()
	return text


def text_normalize(text, leave_punct = True):
	text = list(text.lower())

	for e, c in enumerate(text):
		if c not in rus_alph:
			if c in punct and leave_punct: text[e] = f" {c} "
			else: text[e] = ' '

	text = "".join(text)

	while "  " in text or "\n\n" in text or " \n" in text or "\n " in text:
		while "  " in text: text = text.replace("  ", " ")
		while "\n\n" in text: text = text.replace("\n\n", "\n")
		while " \n" in text: text = text.replace(" \n", "\n")
		while "\n " in text: text = text.replace("\n ", "\n")

	text = text.strip()
	return text

def get_rhymes(text, target_dict, normalize = True):
	if normalize: text = text_normalize(text, False)
	lines = text.split('\n')
	for e, line in enumerate(lines): lines[e] = line.split(' ')[-1]

	for e, line in enumerate(lines):
		for second in lines[e+1:e+4]:
			if compare_last_hit(line, second):
				if line in target_dict: target_dict[line].add(second)
				else: target_dict[line] = {second}

def compare_last_hit(word_1, word_2, compare_to = 58):
	if word_1 == word_2: return False
	for e, x in enumerate(word_1[::-1]):
		if x in glasnie:
			word_1 = word_1[len(word_1) - e - 2:]
			break
	else:
		return False

	for e, x in enumerate(word_2[::-1]):
		if x in glasnie:
			word_2 = word_2[len(word_2) - e - 2:]
			break
	else:
		return False

	result = 0
	for pair in zip(word_1, word_2):
		if pair[0] == pair[1]: result += 1

	if len(word_1) > len(word_2): result = (result / len(word_2)) * 100
	else: result = (result / len(word_1)) * 100

	if result >= compare_to: return True
	else: return False 

def parse_word(word):
	res = analyzer.parse(word)[0].tag

	if len(res) == 1: return str(res)
	else: return str(res.POS)

def count_hits(word):
	result = 0
	for c in word:
		if c in glasnie: result += 1
	return result

def analyze_text(text, target_dict):
	text = text_normalize(text)
	text = text.replace("\n", r" -nl- ").split(" ")
	
	for e, word in enumerate(text[:-1]):
		if word in punct: continue

		next_word_index = 1
		target_word = text[e+next_word_index]

		try:
			while target_word in punct:
				if word not in target_dict:
					target_dict[word] = [{"NOUN" : set(), "ADJF" : set(), "ADJS" : set(), "COMP" : set(), "VERB" : set(), "INFN" : set(), "PRTF" : set(), "PRTS" : set(), "GRND" : set(), "NUMR" : set(), "ADVB" : set(), "NPRO" : set(), "PRED" : set(), "PREP" : set(), "CONJ" : set(), "PRCL" : set(), "INTJ" : set(), "PNCT": set(), "None": set()},
											{"NOUN" : 0, "ADJF" : 0, "ADJS" : 0, "COMP" : 0, "VERB" : 0, "INFN" : 0, "PRTF" : 0, "PRTS" : 0, "GRND" : 0, "NUMR" : 0, "ADVB" : 0, "NPRO" : 0, "PRED" : 0, "PREP" : 0, "CONJ" : 0, "PRCL" : 0, "INTJ" : 0, "PNCT": 0, "None": 0}]
				target_dict[word][0]["PNCT"].add(target_word)
				target_dict[word][1]["PNCT"] += 1
				next_word_index += 1
				target_word = text[e+next_word_index]
		except IndexError: continue

		if target_word not in target_dict:
			target_dict[target_word] = [{"NOUN" : set(), "ADJF" : set(), "ADJS" : set(), "COMP" : set(), "VERB" : set(), "INFN" : set(), "PRTF" : set(), "PRTS" : set(), "GRND" : set(), "NUMR" : set(), "ADVB" : set(), "NPRO" : set(), "PRED" : set(), "PREP" : set(), "CONJ" : set(), "PRCL" : set(), "INTJ" : set(), "PNCT": set(), "None": set()},
										{"NOUN" : 0, "ADJF" : 0, "ADJS" : 0, "COMP" : 0, "VERB" : 0, "INFN" : 0, "PRTF" : 0, "PRTS" : 0, "GRND" : 0, "NUMR" : 0, "ADVB" : 0, "NPRO" : 0, "PRED" : 0, "PREP" : 0, "CONJ" : 0, "PRCL" : 0, "INTJ" : 0, "PNCT": 0, "None": 0}]

		if word == '-nl-': parse = "None"
		else: parse = parse_word(word)

		try:
			target_dict[target_word][0][parse].add(word)
			target_dict[target_word][1][parse] += 1
		except:
			target_dict[target_word][0]["None"].add(word)
			target_dict[target_word][1]["None"] += 1

def generate_line_classic(hits_count):
	line = Line()
	current_word = mind_db.get_random_word()
	while current_word == "-nl-": current_word = mind_db.get_random_word()

	while line.hits < hits_count:
		if current_word == "-nl-":
			line += "."
		else: line += current_word

		next_word_pos = count_pos[choose_val_list(mind_db.word_poses_count(current_word))]
		if next_word_pos == "PNCT":
			line += random.choice(mind_db.word_pos(current_word, "PNCT"))

			try:
				next_word_pos = list(mind_db.word_poses_count(current_word))
				next_word_pos[17] = 0
				next_word_pos = count_pos[choose_val_list(next_word_pos)]
				current_word = random.choice(mind_db.word_pos(current_word, next_word_pos))
			except:
				line += "."
				current_word = mind_db.get_random_word()
		else:
			current_word = random.choice(mind_db.word_pos(current_word, next_word_pos))
	return line

def generate_line(hits_count, rhyme_to = None, start_with = None):
	line = Line()
	if start_with: current_word = start_with
	elif rhyme_to: current_word = random.choice(mind_db.rhyme_to(rhyme_to))
	else: current_word = mind_db.get_random_word()

	while line.hits < hits_count:
		if current_word == "-nl-": line.place_pnct(".", 0)
		else: line.add_to_begin(current_word)

		try: next_word_pos = count_pos[choose_val_list(mind_db.word_poses_count(current_word))]
		except:
			current_word = mind_db.get_random_word()
			next_word_pos = count_pos[choose_val_list(mind_db.word_poses_count(current_word))]

		if next_word_pos == "PNCT":
			insert_punct = random.choice(mind_db.word_pos(current_word, "PNCT"))
			line.place_pnct(insert_punct)

			try:
				next_word_pos = list(mind_db.word_poses_count(current_word))
				next_word_pos[17] = 0
				next_word_pos = count_pos[choose_val_list(next_word_pos)]
				current_word = random.choice(mind_db.word_pos(current_word, next_word_pos))
			except:
				line.place_pnct(".", 0)
				current_word = mind_db.get_random_word()

		else:
			current_word = random.choice(mind_db.word_pos(current_word, next_word_pos))

	return line

def analyze_structure(text, lines_amount = 20):
	structure = []
	lines = text.split("\n")[:lines_amount]
	lines_amount = len(lines)

	for l in lines:
		line_hits = count_hits(l)
		if line_hits != 0: structure.append(line_hits)

	rhymes = []
	rhymed = set()
	rhymes_text = text.split('\n')[:lines_amount]
	for e, line in enumerate(rhymes_text): rhymes_text[e] = line.split(' ')[-1]

	for e1, line in enumerate(rhymes_text):
		if e1 in rhymed: continue
		for e2, second in enumerate(rhymes_text[e1+1:e1+4]):
			if e1+e2+1 in rhymed: continue
			if compare_last_hit(line, second):
				rhymes.append([e1, e1+e2+1])
				rhymed.add(e1)
				rhymed.add(e1+e2+1)
				break

	for x in range(0, len(lines)):
		if x in rhymed: continue
		size = 1
		while True:
			if x + size not in rhymed:
				if (x + size) > lines_amount - 1: break
				rhymed.add(x)
				rhymed.add(x + size)
				rhymes.append([x, x+size])
				break
			else:
				if size == 3: break
				size += 1


	return [structure, sorted(rhymes)]

def analyze_spaces(text, lines_amount = 20):
	spaces = []
	text = text.split("\n")[:lines_amount]

	while True:
		try: i = text.index('')
		except: break
		text.pop(i)
		spaces.append(i)

	return spaces

def generate_structure_hokku(structure):
	text = ""
	for x in structure: text += str(generate_line_classic(x)) + "\n"
	return text.strip()

def generate_structure(structure):
	rhymes = [[], []]
	for r in structure[1]:
		rhymes[0].append(r[0])
		rhymes[1].append(r[1])
	poem = []

	for e, line in enumerate(structure[0]):
		if e in rhymes[1]:
			try: poem.append(generate_line(line, rhyme_to = poem[rhymes[0][rhymes[1].index(e)]].last()))
			except: poem.append(generate_line(line))
		elif e in rhymes[0]: poem.append(generate_line(line, start_with = mind_db.get_random_rhyme()))
		else: poem.append(generate_line(line))

	text = ''
	for e, l in enumerate(poem):
		if e in structure[2]: text += "\n"
		text += str(l) + "\n"

	return text

# STRUCTURE OF POEM:
# 1: Hits count
# 2: Rhymes
# 3: Spaces

# print(generate_structure([(5, 7, 5, 7, 8, 8), ((0, 1), (2, 3), (4, 5)), [1]]))