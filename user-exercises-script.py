import ast
import csv
import re

def treat(content):
	content = content.replace('"',"'")
	content = content.replace('null',"None")
	content = content.replace('false',"False")
	content = content.replace('true',"True")
	content = content.strip()
	content = content.replace(" ","")
	content = re.sub(' +', ' ',content)
	return content

def main():
	file = open('c.txt','r')
	content = file.read()
	file.close()

	#Tratando a string 
	content = treat(content)
	#content = content[content.find("[{"):]
	while(content.find("'exercise'")!=-1):
		content = content[content.find("'exercise'"):]
		print(content[content.find(":")+1:content.find(",")])
		content = content[content.find(',')+1:]

main()
