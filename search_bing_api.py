from requests import exceptions
import argparse
import requests
import cv2
import os
from dotenv import load_dotenv

#Error handling
EXCEPTIONS = set([IOError, FileNotFoundError,
	exceptions.RequestException, exceptions.HTTPError,
	exceptions.ConnectionError, exceptions.Timeout])

# Load your key from .env
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Number of images and size of batch
MAX_RESULTS = 50
GROUP_SIZE = 50

# Set the endpoint API URL
URL = "https://api.bing.microsoft.com/v7.0/images/search"

# Argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True,
	help="Search query on Bing Image")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory of images")
args = vars(ap.parse_args())

# Store search tearms and setup the header
term = args["query"]
headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
params = {"q": term, "offset": 0, "count": GROUP_SIZE}

# Search
print("[INFO] searching Bing API for '{}'".format(term))
search = requests.get(URL, headers=headers, params=params)
search.raise_for_status()

# Grab results
results = search.json()
estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)
print("[INFO] {} total results for '{}'".format(estNumResults,
	term))

# initialize the nb of images
total = 0

for offset in range(0, estNumResults, GROUP_SIZE):
	# update the search parameters 
	print("[INFO] making request for group {}-{} of {}...".format(
		offset, offset + GROUP_SIZE, estNumResults))
	params["offset"] = offset
	search = requests.get(URL, headers=headers, params=params)
	search.raise_for_status()
	results = search.json()
	print("[INFO] saving images for group {}-{} of {}...".format(
		offset, offset + GROUP_SIZE, estNumResults))

	# loop over the results
	for v in results["value"]:
		# try to download the image
		try:
			print("[INFO] fetching: {}".format(v["contentUrl"]))
			r = requests.get(v["contentUrl"], timeout=30)
			# build the path to the output image
			ext = v["contentUrl"][v["contentUrl"].rfind("."):]
			p = os.path.sep.join([args["output"], "{}{}".format(
				str(total).zfill(8), ext)])
			# write the image to disk
			f = open(p, "wb")
			f.write(r.content)
			f.close()
		except Exception as e:
			if type(e) in EXCEPTIONS:
				print("[INFO] skipping: {}".format(v["contentUrl"]))
				continue
		image = cv2.imread(p)
		# Ignore "None" image
		if image is None:
			print("[INFO] deleting: {}".format(p))
			os.remove(p)
			continue
		
		total += 1
