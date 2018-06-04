"""

Program to use google's api to give a likelihood
if files in a folder are plagarized by searching for exact chunks
of documents on google 
Derick Falk

"""

from apiclient.discovery import build
import sys
from os import listdir
from os.path import isfile, join
import os
import docx

# Shows a usuage help text
def usuage():
	print("USUAGE: python PlagSearch.py [folder]\nDefault folder is the current directory")

def google_search(search_term, api_key, cse_id, **kwargs):
	service = build("customsearch", "v1", developerKey=api_key)
	res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()

	try:
		return res['items']
	except KeyError:
		return 0

def readword(filename):
	if 

def main():
	api_key = os.environ.get("api_key")
	cse_id = os.environ.get("cse_id")
	folder = "./"
	files = []
	nof = False
	results = {}
	
	try:
		x = sys.argv[1]
	except:
		nof = True

	try:
		if nof is False:
			folder += sys.argv[1]
		files = [f for f in listdir(folder) if isfile(join(folder,f))]
	except:
		usuage()

	#iterate through files and give a likelihood of plagarism
	for i in files:
		if i[-4:] == 'docx':
			file = readword()
		else:
			file  = open(f'{folder}\{i}','r')
		lines = [x.strip('\n').rstrip() for x in file.readlines()]
		lines = [line for line in lines if line]
		total = 0
		line_count = 0
		sites = []
		tot_results = []

		for line in lines:
			results = google_search("\"" + line + "\"", api_key, cse_id)
			if results == 0:
				line_count += 1
				continue
			else:
				total += 1
				line_count += 1
				tot_results.append(results)
		likelihood = round(total / len(lines),2)*100
		if likelihood > 100: likelihood=100.00
		if len(tot_results) > 0:
			print(f'*** Excerpt of Results {i}***')
			
			for r in range(2):
				print(10*'*')
				print(results[r]['title'])
				print(results[r]['link'])
				print(10*'*')
		print(f"Likelihood that {i} is plagarized: {likelihood}% ")
		if len(files) > 1:
			print("\n")



		file.close()


if __name__ == "__main__":
	main()
