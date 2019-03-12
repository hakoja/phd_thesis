import sys
import re
import urllib.request
from itertools import dropwhile, takewhile

months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

if len(sys.argv) != 2:
	print("Provide RFC number")
	sys.exit()

draft = False	
	
if sys.argv[1].isnumeric():
	rfc_number = sys.argv[1]
	rfc_id = "rfc" + rfc_number 
	url = "https://tools.ietf.org/rfc/" + rfc_id + ".txt"
else:
	draft = True
	rfc_id = sys.argv[1]
	url = "https://tools.ietf.org/id/" + rfc_id + ".txt"

	
with urllib.request.urlopen(url) as response:
	rfc = response.read().decode('utf-8').splitlines()



def get_title(xs):
	xs = dropwhile(lambda l: l == "", xs)
	xs = dropwhile(lambda l: l != "", xs)
	xs = dropwhile(lambda l: l == "", xs)
	xs = takewhile(lambda l: l != "", xs)
	return " ".join(list(map(lambda x: x.lstrip(), list(xs))))

def get_month_and_year(xs):
	for line in rfc:
		for m in months:
			if m in line and "Expires: " not in line:
				y = str([y for y in map(int, re.findall('\d+', line)) if int(y) > 1969].pop())
				return [m, y]

def get_authors(xs):		
	author_index = 0
	authors = []
	
	for line in xs:
		if any(x in line for x in ["Author's Address", "Authors' Addresses", "Editors' Addresses"]):
			author_index = rfc.index(line) + 1

	temp = []
	for line in xs[author_index:]:
		if line == "" or any(x in line for x in ["URI: ", "Phone: ", "Fax: "]):
			continue
		temp.append(line)
		if "EMail:" in line or "Email:" in line:
			authors.append(temp[0].lstrip())
			temp = []	
	
	return authors

rfc_title = get_title(rfc)
rfc_month, rfc_year = get_month_and_year(rfc)
rfc_authors = get_authors(rfc)
rfc_num_pages = str(len([l for l in rfc if "[Page " in l]))
rfc_url = "https://tools.ietf.org/html/" + rfc_id
		
print("@techreport{IETF:" + ("RFC" + rfc_number if not draft else "DRAFT")  + ",")
print("\t author = {" + " and ".join(rfc_authors) + "},")	
print("\t title = \"{" + rfc_title + "}\",")
print("\t howpublished = {Internet Requests for Comments},")
print("\t type = {" + ("Internet-draft" if draft else "RFC " + rfc_number) + "},")
# print("\t number = \"{" + (rfc_number if not draft else "(Informational)") + "}\",")	
print("\t pages = {1-" + rfc_num_pages + "},")
print("\t year = {" + rfc_year + "},")
print("\t month = {" + rfc_month + "},")
print("\t publisher = \"{RFC Editor}\",")
print("\t institution = \"{RFC Editor}\",")
print("\t url = {" + rfc_url + "},")
print(("%" if draft else "") + "\t shorthand = {" + rfc_id.upper() + "}")	
print("}")	




