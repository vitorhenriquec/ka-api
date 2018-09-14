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
	file = open('b.txt','r')
	content = file.read()
	file.close()

	#Tratando a string 
	content = treat(content)

	exercise_done = set()

	'''while(content.find("'exercise':")!=-1):
		aux = content[content.find("'exercise':"):]
		exercise_done.add(aux[aux.find(":")+2:aux.find(",")-1])
		content = content[aux.find(","):]
	'''
	#"name": ,
	#"last_done": ,
	#"longest_streak": ,
	'''
	"streak": ,
    "streak_start": ,
    "total_correct": ,
    "total_done": ,
	'''

	file = open('c.txt','r')
	content_exercise = file.read()
	file.close()

	content_exercise = treat(content_exercise)

	name = ""
	last_done = ""
	streak = ""
	total_correct = ""
	total_done = ""

	#print(content_exercise)

	exercise_info = []
	while(content_exercise.find("'streak':")!=-1):


		aux = content_exercise[content_exercise.find("'streak':"):]
		streak = int(aux[aux.find(":")+1:aux.find(",")].strip())

		aux = aux[aux.find("'exercise':"):]
		name = aux[aux.find(":")+2:aux.find(",")-1].strip()

		aux = aux[aux.find("'total_done':"):]
		total_done = int(aux[aux.find(":")+1:aux.find(",")].strip())
		
		aux = aux[aux.find("'total_correct':"):]
		total_correct = int(aux[aux.find(":")+1:aux.find(",")].strip())

		aux = aux[aux.find("'last_done':"):]
		last_done = aux[aux.find(":")+2:aux.find(",")-1].strip()

		#print(aux)

		'''
		aux = aux[aux.find("'streak':"):]
		streak = (aux[aux.find(":")+2:aux.find(",")-1].strip())

		aux = aux[aux.find(",")+1:] 

		aux = aux[aux.find("'streak_start':"):]
		streak_start = aux[aux.find(":")+2:aux.find(",")-1].strip()

		aux = aux[aux.find(",")+1:] 

		aux = aux[aux.find("'total_correct':"):]
		total_correct = aux[aux.find(":")+2:aux.find(",")-1].strip()

		aux = aux[aux.find(",")+1:] 

		aux = aux[aux.find("'total_done':"):]
		total_done = aux[aux.find(":")+2:aux.find(",")-1].strip()

		aux = aux[aux.find(",")+1:]
		'''
		content_exercise = aux
		#print(content)
		#break

	#print(content_exercise)
	print([name,last_done, streak, total_correct, total_done])

	#print(exercise_done)



main()
