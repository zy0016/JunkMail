#!/usr/bin/python

import os
import sys
import time;
from time import sleep,ctime
import shutil
import threading
import tkinter

mailfolder_junk=""
mailfolder_normal=""
keywordfile_junk=""
keywordfile_normal=""
file_studied_mail_junk=""
file_studied_mail_normal=""
junk_mail_count = 0
normal_mail_count = 0
mailcount = 0
hs_junk=set()
hs_normal=set()
list_filestudied_junk=[]
list_filestudied_normal=[]
list_file_words_junk=[]
list_file_words_normal=[]


def getLanguageParam(line,key):
	if line.find(key) == -1:
		return None
	else:
		return line.split("=")[1].replace("\"","").strip()

def read_config():
	global mailfolder_junk
	global mailfolder_normal
	global keywordfile_junk
	global keywordfile_normal
	global file_studied_mail_junk
	global file_studied_mail_normal
	with open("config.ini") as f:
		for line in f:
			strall = line.strip()
			if strall.find("mailfolder_junk") != -1:
				mailfolder_junk = getLanguageParam(strall,"mailfolder_junk")
			elif strall.find("mailfolder_normal") != -1:
				mailfolder_normal = getLanguageParam(strall,"mailfolder_normal")
			elif strall.find("keywordfile_junk") != -1:
				keywordfile_junk = getLanguageParam(strall,"keywordfile_junk")
			elif strall.find("keywordfile_normal") != -1:
				keywordfile_normal = getLanguageParam(strall,"keywordfile_normal")
			elif strall.find("file_studied_mail_junk") != -1:
				file_studied_mail_junk = getLanguageParam(strall,"file_studied_mail_junk")
			elif strall.find("file_studied_mail_normal") != -1:
				file_studied_mail_normal = getLanguageParam(strall,"file_studied_mail_normal")
	
def research(filepath_sour,h,list_filestudied,list_fileswords):
	global mailcount
	print("open the ",filepath_sour)
		
	filelist = os.listdir(filepath_sour)
	for num in range(len(filelist)):
		filename=filelist[num].strip()
		if os.path.isdir(filepath_sour + "\\" + filename):
			research(filepath_sour + "\\" + filename,h,list_filestudied,list_fileswords)
		else:
			result = filepath_sour+"\\"+filename
			# print(result)
			readsinglemail(result,list_filestudied,h,list_fileswords)
			mailcount+=1

def study_junk_mail(junkmailfolder):
	global mailcount
	global junk_mail_count
	global hs_junk
	global list_filestudied_junk
	global list_file_words_junk
	mailcount = 0
	research(junkmailfolder,hs_junk,list_filestudied_junk,list_file_words_junk)
	junk_mail_count = mailcount
	return junk_mail_count

def study_normal_mail(normalmailfolder):
	global mailcount
	global normal_mail_count
	global hs_normal
	global list_filestudied_normal
	global list_file_words_normal
	mailcount = 0
	research(normalmailfolder,hs_normal,list_filestudied_normal,list_file_words_normal)
	normal_mail_count = mailcount
	return normal_mail_count

def WordIsValid(word):
	if len(word) < 3:
		return False
	charact=list(word)
	for i in charact:
		if i.isdigit() == True or i.isalpha() == False:
			return False
	
	return True
	
def getwords(hset):
	result = ""
	for i in hset:
		result = result + i + " "
	return result.strip()
	
def readsinglemail(filename,list_filestudied,h,list_fileswords):
	hs_words = set()
	with open(filename) as f:
		for line in f:
			strall = line.strip()
			arrstr = strall.split(" ")
			for i in arrstr:
				if WordIsValid(i):
					h.add(i)
					hs_words.add(i)
					
	words = getwords(hs_words)
	list_filestudied.append(filename + " " + words)
	list_fileswords.append(filename + " " + words)

def getwords_detail(h,mailcount_junk,mailcount_normal,list_fileswords_junk,list_fileswords_normal):
	res = ""
	for word in h:
		bfindinjunk = False
		bfindinnormal = False
		pjunk = 0.0
		pnormal = 0.0
		fwordcount_junk = 0.0
		fwordcount_normal = 0.0
		iwordcount_junk = 0
		iwordcount_normal = 0
		for i in list_fileswords_junk:
			strsingle = []
			strsingle = i.split(" ")
			for j in strsingle:
				if word == j:
					iwordcount_junk = iwordcount_junk + 1
					fwordcount_junk = fwordcount_junk + 1.0
					bfindinjunk = True
					break
		
		pjunk = fwordcount_junk / mailcount_junk
		
		for i in list_fileswords_normal:
			strsingle = []
			strsingle = i.split(" ")
			for j in strsingle:
				if word == j:
					iwordcount_normal = iwordcount_normal + 1
					fwordcount_normal = fwordcount_normal + 1.0
					bfindinnormal = True
					break
		
		pnormal = fwordcount_normal / mailcount_normal
		
		line = ""
		if bfindinjunk and not bfindinnormal:
			pnormal = 0.01
			line = word + " " + str(pjunk) + " 0.01"
		elif not bfindinjunk and bfindinnormal:
			pjunk = 0.01
			line = word + " 0.01 " + str(pnormal)
		else:
			line = word + " " + str(pjunk) + " " + str(pnormal)
			
		line = line + " " + str(iwordcount_junk) + " " + str(iwordcount_normal)
		res = res + line + "\r\n"
		print(line)
		
	return res

def SaveTextToFile(str,filename):
	resultfile = open(filename,'w')
	resultfile.write(str + "\n")
	resultfile.close()
	
def SaveTextToFileList(List,filename):
	str = ""
	for i in List:
		str = str + i + "\r\n"
	SaveTextToFile(str.strip(),filename)
	
def Generate_datafiles():
	global hs_junk
	global hs_normal
	global junk_mail_count
	global normal_mail_count
	global list_file_words_junk
	global list_file_words_normal
	global keywordfile_junk
	global keywordfile_normal
	global file_studied_mail_junk
	global file_studied_mail_normal
	res_junk = getwords_detail(hs_junk,junk_mail_count,normal_mail_count,list_file_words_junk,list_file_words_normal)
	SaveTextToFile(res_junk,keywordfile_junk)
	res_normal = getwords_detail(hs_normal,junk_mail_count,normal_mail_count,list_file_words_junk,list_file_words_normal)
	SaveTextToFile(res_normal, keywordfile_normal)
	
	SaveTextToFileList(list_filestudied_junk, file_studied_mail_junk)
	SaveTextToFileList(list_filestudied_normal, file_studied_mail_normal)

def main():
	global junk_mail_count
	global normal_mail_count
	read_config()
	print("=========")
	print(mailfolder_junk)
	print(mailfolder_normal)
	print(keywordfile_junk)
	print(keywordfile_normal)
	print(file_studied_mail_junk)
	print(file_studied_mail_normal)
	
	junk_mail_count = study_junk_mail(mailfolder_junk)
	normal_mail_count = study_normal_mail(mailfolder_normal)
	Generate_datafiles()
	
	str1 = "file_studied_mail_junk:" + str(junk_mail_count) + " file_studied_mail_normal:" + str(normal_mail_count)
	print(str1)
	print("end")

if __name__ == '__main__':
	main()
	
	
