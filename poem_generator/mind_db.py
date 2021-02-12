# File for working with db

import sqlite3
import random
import time

connection = sqlite3.connect("mind.db")	# Database with poems data
cursor = connection.cursor()

SETTINGS_WORDS = cursor.execute("SELECT COUNT(*) FROM DATA").fetchone()[0] - 1
try: SETTINGS_RHYMES = cursor.execute("SELECT COUNT(*) FROM RHYMES").fetchone()[0] - 1
except sqlite3.OperationalError: SETTINGS_RHYMES = 0
SETTINGS_STRUCTURES = cursor.execute("SELECT COUNT(*) FROM STRS").fetchone()[0] - 1

count_pos = {0 : "NOUN", 1 : "ADJF", 2 : "ADJS", 3 : "COMP", 4 : "VERB", 5 : "INFN", 6 : "PRTF", 7 : "PRTS", 8 : "GRND", 9 : "NUMR", 10 : "ADVB", 11 : "NPRO", 12 : "PRED", 13 : "PREP", 14 : "CONJ", 15 : "PRCL", 16 : "INTJ", 17: "PNCT" , 18 : "None"}

def config_db(db_name):
	global connection, cursor
	global SETTINGS_WORDS, SETTINGS_RHYMES, SETTINGS_STRUCTURES
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()

	SETTINGS_WORDS = cursor.execute("SELECT COUNT(*) FROM DATA").fetchone()[0] - 1
	try: SETTINGS_RHYMES = cursor.execute("SELECT COUNT(*) FROM RHYMES").fetchone()[0] - 1
	except sqlite3.OperationalError: SETTINGS_RHYMES = 0
	SETTINGS_STRUCTURES = cursor.execute("SELECT COUNT(*) FROM STRS").fetchone()[0] - 1

def save(data):
	s = time.time()
	for word, value in data.items():
		command_params = [word]
		for pos in value[0].values():
			if len(pos) > 0: command_params.append(str(pos)[1:-1].replace("'", ""))
			else: command_params.append(None)

		script = "INSERT INTO DATA VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(Word) DO UPDATE SET "
		for e, val in enumerate(command_params[1:]):
			if val == None: continue
			script += f"{count_pos[e]} = \"{val}\" || ifnull(\", \" || {count_pos[e]}, \"\"), "
		if script != "INSERT INTO DATA VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(Word) DO UPDATE SET ":
			cursor.execute(script[:-2] + f" WHERE Word = \"{word}\"", command_params)

		command_params = [word]
		for pos in value[1].values(): command_params.append(pos)
		script = "INSERT INTO POS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(Word) DO UPDATE SET "
		for e, pos in enumerate(command_params[1:]):
			if pos > 0: script += f"{count_pos[e]} = {count_pos[e]} + {pos}, "
		if script != "INSERT INTO POS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(Word) DO UPDATE SET ":
			cursor.execute(script[:-2] + f" WHERE Word = \"{word}\"", command_params)
	print(f"           local script executed in {time.time() - s}")
def clear_db():
	cursor.execute("DELETE FROM DATA")
	cursor.execute("DELETE FROM RHYMES")
	cursor.execute("DELETE FROM STRS")
	cursor.execute("DELETE FROM POS")
	connection.commit()
	cursor.execute("VACUUM")
	connection.commit()

def optimize(dbname):
	print(f"Optimizing {dbname}")
	optimize_connection = sqlite3.connect(dbname)
	sel_cursor = optimize_connection.cursor()
	exec_cursor = optimize_connection.cursor()

	sel_cursor.execute("SELECT * FROM DATA")
	element = sel_cursor.fetchone()

	element_index = 1
	while element != None:
		# print(f"- {element_index}")
		local_script = "UPDATE DATA SET"

		for e, sub in enumerate(element[1:]):
			if sub == '' or sub == ", ":
				local_script += " {} = NULL,".format(count_pos[e])
				continue
			optimized = str(set(sub.replace("'", "").replace(",", "").replace("  ", " ").strip().split(" ")))[1:-1]
			if optimized != sub:
				local_script += " {} = \"{}\",".format(count_pos[e], optimized)
		if local_script != "UPDATE DATA SET":
			optimize_connection.execute(local_script[:-1] + f" WHERE Word = \"{element[0]}\"")
		element_index += 1
		element = sel_cursor.fetchone()

		if element_index % 300 == 0: print(time.strftime("%H:%M:%S"), element_index) 

	optimize_connection.commit()

def save_rhymes(data):
	for word, value in data.items():
		cursor.execute("INSERT INTO RHYMES VALUES (\"{0}\", \"{1}\") ON CONFLICT(Word) DO UPDATE SET Value = Value || \", {1}\"".format(word, str(value)[1:-1].replace("'", "")))

def save_structure(structure):
	cursor.execute("INSERT INTO STRS VALUES (?, ?, ?, ?)", (structure[0], str(structure[1])[1:-1], str(structure[2])[1:-1], str(structure[3])[1:-1]))

def save_structure_custom(structure):
	cursor.execute("INSERT INTO STRS VALUES (?, ?)", (structure[0], str(structure[1])[1:-1]))

def commit(): connection.commit()

def get_structure():
	try: cursor.execute("SELECT * FROM STRS LIMIT 1 OFFSET ?", (random.randint(1, SETTINGS_STRUCTURES),))
	except: cursor.execute("SELECT * FROM STRS LIMIT 1")
	temp = cursor.fetchone()
	structure = []

	structure.append(temp[1].split(", "))
	for e, x in enumerate(structure[0]): structure[0][e] = int(x)

	structure.append(temp[2].replace("[", "")[:-1].split("], "))
	for e, x in enumerate(structure[1]):
		structure[1][e] = x.split(", ")
		structure[1][e][0] = int(structure[1][e][0])
		structure[1][e][1] = int(structure[1][e][1])

	try:
		structure.append(temp[3].split(", "))
		for e, x in enumerate(structure[2]): structure[2][e] = int(x)
	except: structure[2] = []

	return structure

def get_structure_custom():
	cursor.execute("SELECT * FROM STRS LIMIT 1 OFFSET ?", (random.randint(1, SETTINGS_STRUCTURES), ))
	structure = cursor.fetchone()[1].split(", ")
	for e, x in enumerate(structure): structure[e] = int(x)
	return structure

def word_poses_count(word):
	return cursor.execute("SELECT * FROM POS WHERE Word = ?", (word,)).fetchone()[1:]

def word_pos(word, pos):
	cursor.execute("SELECT {} FROM DATA WHERE Word = \"{}\"".format(pos, word))

	try:
		result = cursor.fetchone()[0].split(", ")
		return result
	except TypeError: return []

def get_random_word():
	return cursor.execute("SELECT Word FROM DATA LIMIT 1 OFFSET ?", (random.randint(1, SETTINGS_WORDS),)).fetchone()[0]

def get_random_word_pos(word_pos):
	cursor.execute("SELECT {} FROM DATA WHERE {} != ''".format(word_pos, word_pos))
	return random.choice(cursor.fetchone()[0].split(", "))

def rhyme_to(word):
	cursor.execute("SELECT Value FROM RHYMES WHERE Word = ?", (word,))
	return cursor.fetchone()[0].split(", ")

def get_random_rhyme():
	cursor.execute("SELECT Word FROM RHYMES LIMIT 1 OFFSET ?", (random.randint(1, SETTINGS_RHYMES),))
	return cursor.fetchone()[0]

