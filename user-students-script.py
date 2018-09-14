import ast
import csv

def main():
	file = open('user-students.json','r')
	content = file.read()
	file.close()

	list_user = []

	#Tratando a string 
	content = content.replace('"',"'")
	content = content.replace('null',"None")
	content = content.replace('false',"False")
	content = content.replace('true',"True")
	content = content.strip()

	#Interpreta a string como um elemento no python[No caso list de dicts]
	list_user = eval(content)

	#Definem as keys
	specif_key = ['nickname','email','username','user_id','kaid','profile_root']
	keys_ = list_user[3].keys()

	#Delete as keys desnecessárias
	for i in list_user:
		for k in keys_:
			if k not in specif_key:
				del i[k]

	#Escreve os dados em um csv
	with open('students.csv', 'w') as f:
	    writer = csv.DictWriter(f,fieldnames=['nickname','email','username','user_id','kaid','profile_root'],delimiter=";")
	    writer.writeheader()
	    for i in list_user:
	    	writer.writerow(i)

	f.close()

main()