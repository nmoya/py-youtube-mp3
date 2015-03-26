import sys
import os
import subprocess
import urllib2
import re


def download(url, title):
	return subprocess.call(["youtube-dl", "-x",
							"--audio-format", "mp3",
							"--audio-quality", "5",
							url, "-o", title+".%(ext)s"])


def clean_string(string):
	string = string.replace("Lyrics", "")
	string = string.replace("HQ", "")
	string = re.sub(r'\([^)]*\)', '', string)
	string = re.sub(r'\[[^)]*\]', '', string)
	string = re.sub(r'\{[^)]*\}', '', string)
	string = string.replace(" - YouTube", "")
	string = string.replace("&#39;", "'")
	string = string.replace("&nbsp", " ")
	rubbish = [("(", ")"), ("[", "]")]
	for r in rubbish:
		if r[0] in string and r[1] in string:
			begin = string.find(r[0])
			end = string.find(r[1]) + 1
			string = string[:begin] + string[end:]
			string = string.strip()
	string = string.strip()
	return string


def get_video_title(url):
	response = urllib2.urlopen(url)
	html = response.read()
	title_begin = html.find("<title>") + len("<title>")
	title_end = html.find("</title>")
	title = html[title_begin:title_end]
	title = clean_string(title)
	return title + ".mp3"


if __name__ == "__main__":
	command = "youtube-dl -t -x --audio-format mp3 --audio-quality 5 %s"
	if len(sys.argv) != 2 and len(sys.argv) != 3:
		print "python app.py <text file with links> [--force]"
		sys.exit(1)

	force = False
	if len(sys.argv) == 3:
		force = True

	if "downloaded.txt" not in os.listdir("."):
		fdown = open("downloaded.txt", "w")
		fdown.close()

	fdown = open("downloaded.txt", "r")
	content = fdown.read()
	downloaded = content.split("\n")
	fdown.close()

	with open(sys.argv[1]) as arq:
		urls = arq.read().split("\n")
		# downloaded = [f for f in os.listdir(".") if f.endswith(".mp3")]
		for video_url in urls:
			title = get_video_title(video_url)
			rtn_code = 1
			if video_url not in downloaded or force:
				while rtn_code != 0:
					print "--------------------------------------------------------------"
					print "Downloading", title, "..."
					print "--------------------------------------------------------------"
					rtn_code = download(video_url, title.replace(".mp3", ""))
				if video_url not in downloaded:
					downloaded.append(video_url)
			else:
				print "Title:", title, "was downloaded previously. Re-execute with --force"
	
	fdown = open("downloaded.txt", "w")
	fdown.write("\n".join(downloaded))
	fdown.close()