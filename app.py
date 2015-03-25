import sys
import os
import subprocess
import urllib2


def download(url):
	return subprocess.call(["youtube-dl", "-x",
							"--audio-format", "mp3",
							"--audio-quality", "5",
							url, "-o", "%(title)s.%(ext)s"])


def clean_string(string):
	string = string.replace("Lyrics", "")
	string = string.replace("HQ", "")
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
	if len(sys.argv) != 2:
		print "python app.py <text file with links>"
		sys.exit(1)

	with open(sys.argv[1]) as arq:
		musics = arq.read().split("\n")
		downloaded = [f for f in os.listdir(".") if f.endswith(".mp3")]
		for music in musics:
			title = get_video_title(music)
			rtn_code = 1
			if title not in downloaded:
				while rtn_code != 0:
					print "--------------------------------------------------------------"
					print "Downloading", title, "..."
					print "--------------------------------------------------------------"
					rtn_code = download(music)
				