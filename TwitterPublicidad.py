# -*- coding: utf-8 -*-
__author__="AritzBi"
import nltk
import csv
import re
from nltk.stem.snowball import SpanishStemmer
from nltk import word_tokenize
import random
diasDeLaSemana = { " lunes ", " martes ", " miercoles ", " jueves ", " viernes " }
signosDePuntacion = { ";", "¿", ": ", " ? ", " : ", " ¿ ", "\\? ", " +"}
pronombres = { " me ", " te ", " se ", " nos ", " os " }
determinantes = { " su ", " al ", " esta ", " ese " , " mi ", " la ", " el ", " lo ", " las ", " los " , " l@s ", " tus ", " ellos ", " ellas ", " tu ", " un ", " una ", " del ", " y ", " o ", " nuestras ", " nuestros ", " cualquier ", " nuestra", " cada "}
prepositions={" a ", " ante ", " bajo ", " cabe ", " con ", " contra ", " de ", " desde ", " durante ", " en ", " entre ", " hacia ", " hasta ", " mediante ", " para ", " por ", " según ", " sin ", " so ", " sobre ", " tras ", " versus ", " vía ", "la ", " si "}
stopWords={' unas ', ' una ', ' unos ', ' un ', ' del ', ' al ', ' el ', ' la ', ' los ', ' lo ', ' las ', ' de ', ' en ', ' sobre ', ' por ', ' dentro ', ' hacia ',
' desde ', ' fuera ', ' como ', ' así ', ' tal ', ' o ', ' y ', ' esos ', ' esas ', ' este ', ' esta ', ' aquellas ', ' aquellos ', ' ese ', ' esa ',
' para ', ' es ', ' fue ', ' era ',  ' soy ', ' eres ', ' sido ', ' eras '}
st = SpanishStemmer()
publicidad=[]
noPublicidad=[]
def stemmer(word):
	return st.stem(word)

def cargarListas(file,lista):
	with open(file,'rb') as csvfile:
		data=csv.reader(csvfile,delimiter=',')
		for row in data:
			lista.append(Tuit(row[0],row[1],row[2],row[3]))
def getNumberOfMentions(lista):
	pattern=re.compile(r"@\w*")
	for tuit in lista:
		matches=re.findall(pattern,tuit.texto)
		tuit.texto=pattern.sub(" ",tuit.texto)
		tuit.numMentions=len(matches)

def getNumberOfUrls(lista):
	pattern=re.compile(r'(https?|ftp|file)://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]')
	for tuit in lista:
		matches=re.findall(pattern,tuit.texto)
		tuit.texto=pattern.sub(" ",tuit.texto)
		tuit.numURLs=len(matches)

def reemplazarValores(texto, restricciones):
	for restriccion in restricciones:
		tuit.texto=tuit.texto.replace(restriccion," ",100)
def getNumberMatches(texto,palabra):
	cont=0
	for token in texto:
		if token==palabra:
			cont=cont+1
	return cont
def getNumNumbers(lista):
	pattern=re.compile(r"\d+")
	for tuit in lista:
		matches=re.findall(pattern,tuit.texto)
		tuit.numNumbers=len(matches)

class Tuit(object):
	def __init__(self,texto,seguidores,siguiendo,tuits):
		self.texto=" "+texto
		self.seguidores=seguidores
		self.siguiendo=siguiendo
		self.tuits=tuits
		self.numURLs=0
		self.numMentions=0
		self.numNumbers=0

cargarListas("csv/Publicidad.csv",publicidad)
cargarListas("csv/NoPublicidad.csv",noPublicidad)
getNumberOfMentions(publicidad)
getNumberOfMentions(noPublicidad)
getNumberOfUrls(publicidad)
getNumberOfUrls(noPublicidad)
getNumNumbers(publicidad)
getNumNumbers(noPublicidad)
for tuit in publicidad:
	reemplazarValores(tuit.texto,diasDeLaSemana)
	reemplazarValores(tuit.texto,signosDePuntacion)
	reemplazarValores(tuit.texto,pronombres)
	reemplazarValores(tuit.texto,determinantes)
	reemplazarValores(tuit.texto,prepositions)
	reemplazarValores(tuit.texto,stopWords)
for tuit in noPublicidad:
	reemplazarValores(tuit.texto,diasDeLaSemana)
	reemplazarValores(tuit.texto,signosDePuntacion)
	reemplazarValores(tuit.texto,pronombres)
	reemplazarValores(tuit.texto,determinantes)
	reemplazarValores(tuit.texto,prepositions)
	reemplazarValores(tuit.texto,stopWords)
for tuit in publicidad:
	tokens=word_tokenize(tuit.texto.decode('utf-8'))
	array=[]
	for token in tokens:
		array.append(stemmer(token))
	tuit.texto=array

for tuit in noPublicidad:
	tokens=word_tokenize(tuit.texto.decode('utf-8'))
	array=[]
	for token in tokens:
		array.append(stemmer(token))
	tuit.texto=array
stringToInsert=""
file=open('NoPublicidad.txt', 'w')
for tuit in noPublicidad:
	tmp=', '.join(tuit.texto)+"\n"
	stringToInsert=stringToInsert+tmp.encode('utf-8')
file.write(stringToInsert)
stringToInsert=""
file=open('Publicidad.txt', 'w')
for tuit in publicidad:
	tmp=', '.join(tuit.texto)+"\n"
	stringToInsert=stringToInsert+tmp.encode('utf-8')
file.write(stringToInsert)

keyWords={"descuent","ofert","compr","product","prueb","rebaj","%","person","videojueg","amor","agradec","dto","nuev","regal","busc","ahorr","navid","adquier","form","no","cuand","quer","algo","muy","tod","gratis","€".decode('utf-8'),"segu"}
arrayData=[]
for tuit in publicidad:
	data=[];
	for keyWord in keyWords:
		matches=getNumberMatches(tuit.texto,keyWord)
		data.append(matches)
	data.append(tuit.numURLs)
	data.append(tuit.numMentions)
	#data.append(tuit.numNumbers)
	#data.append(tuit.siguiendo)
	#data.append(tuit.seguidores)
	#data.append(tuit.tuits)
	data.append(1)
	arrayData.append(data)


for tuit in noPublicidad:
	data=[];
	for keyWord in keyWords:
		matches=getNumberMatches(tuit.texto,keyWord)
		data.append(matches)
	data.append(tuit.numURLs)
	data.append(tuit.numMentions)
	#data.append(tuit.numNumbers)
	#data.append(tuit.siguiendo)
	#data.append(tuit.seguidores)
	#data.append(tuit.tuits)
	data.append(0)
	arrayData.append(data)
random.shuffle(arrayData)
stringToInsert=""
file=open('FinalData.txt', 'w')
for data in arrayData:
	tmp=""
	for value in data:
		tmp=tmp+str(value)+','
	tmp = tmp[:-1]
	stringToInsert=stringToInsert+tmp.encode('utf-8')+"\n"
file.write(stringToInsert)



