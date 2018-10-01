# -*- coding: utf-8 -*-
import json

def _main_():
	#Quando eu faço a busca para um exercício específico, a API retorna um dicionario
	file = open('continuitychris.json')
	content = file.read()
	file.close()
	jsoni  = json.loads(content)
	print(jsoni['exercise'])
	print(jsoni['kind'])
	print(jsoni['longest_streak'])
	print(jsoni['last_done'])
	print(jsoni['streak'])
	print(jsoni['total_correct'])
	print(jsoni['total_done'])
	print(jsoni['user'])

def __main__():
	
	#Abra o arquivo
	file = open('chris.json')
	content = file.read()
	file.close()

	#Interpreta a string conteudo que contem json 
	pythojson = json.loads(content) 
	
	
	file = open('exercise.txt','w')
	for i in pythojson:
		file.write(str(i['exercise'])+'\n')
		print(i['exercise'])
		print(i['exercise_model']['ka_url'])
		#if(str(i['exercise_model']['ka_url']).find('logarithmic-differentiation') !=-1):
		print("Feito: " + str(i['last_done']))
		print("Maior sequência: " + str(i['longest_streak']))
		print("Sequência: " + str(i['streak']))
		print("Totais corretos: " + str(i['total_correct']))
		print("Totais feito: " + str(i['total_done']))
		print("\n")
			#break
		#print(i['exercise_model']['ka_url'])
	file.close()
	
__main__()

#_main_()