import urllib
import urllib2
import sys
import threading


class Fetcher(threading.Thread):
	def __init__(self, url, title):
		threading.Thread.__init__(self)
		self.url = url
		self.title = title
		
	def run(self):
		urllib.urlretrieve (self.url, self.title)

def open_links_file(file):
	arq = open(file)
	content = [l for l in arq.read().split("\n") if "%" not in l]
	arq.close()
	return content

def clean_string(string):
	string = string.replace("Lyrics", "")
	string = string.replace("HQ", "")
	string = string.replace(" - YouTube", "")
	rubbish = [("(", ")"), ("[", "]")]
	for r in rubbish:
		if r[0] in string and r[1] in string:
			begin = string.find(r[0])
			end = string.find(r[1]) + 1
			string = string[:begin] + string[end:]
			string = string.strip()
	string = string.strip()
	return string

def extract_title(html):
	title_begin = html.find("<title>") + len("<title>")
	title_end = html.find("</title>")
	title = html[title_begin:title_end]
	title = clean_string(title)
	return title + ".mp3"

def process_links(links):	
	threads = []
	for l in links:
		response = urllib2.urlopen(l)
		html = response.read()
		title = extract_title(html)
		print "Fetching: ", title
		threads.append(Fetcher("http://youtubeinmp3.com/fetch/?video="+l, title))
		threads[-1].start()
	for t in threads:
		t.join()

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "Call: python app.py <links_file.txt>"
		sys.exit(-1)

	links = open_links_file(sys.argv[1])
	process_links(links)
