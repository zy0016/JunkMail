#!/usr/bin/python

import os
import sys
import time;
from time import sleep,ctime
import shutil

mailfolder_junk=""
mailfolder_normal=""
keywordfile_junk=""
keywordfile_normal=""
file_studied_mail_junk=""
file_studied_mail_normal=""
unknown_mail_list = ""
unknown_mail_check_result = ""
junklevel = 0.9
CheckedWords = 15
junk_mail_count = 0
normal_mail_count = 0
mailcount = 0
hs_junk=set()
hs_normal=set()
list_filestudied_junk=[]
list_filestudied_normal=[]
list_file_words_junk=[]
list_file_words_normal=[]
words_cur_mail = set()
filecontent_junk = []
filecontent_normal = []
file = ""

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
	global unknown_mail_list
	global unknown_mail_check_result
	global junklevel
	global CheckedWords
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
			elif strall.find("unknown_mail_list") != -1:
				unknown_mail_list = getLanguageParam(strall,"unknown_mail_list")
			elif strall.find("unknown_mail_check_result") != -1:
				unknown_mail_check_result = getLanguageParam(strall,"unknown_mail_check_result")
			elif strall.find("junklevel") != -1:
				junklevel = float(getLanguageParam(strall,"junklevel"))
			elif strall.find("CheckedWords") != -1:
				CheckedWords = int(getLanguageParam(strall,"CheckedWords"))

def WordIsValid(word):
	if len(word) < 3:
		return False
	charact=list(word)
	for i in charact:
		if i.isdigit() == True or i.isalpha() == False:
			return False
	
	return True

def SaveTextToFile(str,filename):
	resultfile = open(filename,'w')
	resultfile.write(str + "\n")
	resultfile.close()
	
def SaveTextToFileList(List,filename):
	str = ""
	for i in List:
		str = str + i + "\r\n"
	SaveTextToFile(str.strip(),filename)
	
def GetAllFilenameContent(filename):
	filelist = []
	with open(filename) as f:
		for line in f:
			strall = line.strip()
			arrline = []
			arrline = strall.split(" ")
			if len(arrline) == 0:
				continue
			else:
				if len(arrline[0]) > 3:
					filelist.append(arrline[0])
				
	return filelist

def GetAllFileContent(filename):
	filelist = []
	with open(filename) as f:
		for line in f:
			strall = line.strip()
			filelist.append(strall)
				
	return filelist
	
def read_mail(filename):
	global words_cur_mail
	with open(filename) as f:
		for line in f:
			strall = line.strip()
			arrstr = strall.split(" ")
			for i in arrstr:
				if WordIsValid(i):
					words_cur_mail.add(i)

def read_keywords_data():
	global filecontent_junk
	global filecontent_normal
	filecontent_junk = GetAllFileContent(keywordfile_junk)
	filecontent_normal = GetAllFileContent(keywordfile_normal)

def get_word_percent(word,filecontent):
	res = [0.01,0.01]
	for i in filecontent:
		single = i.split(" ")
		if word == single[0]:
			res[0] = float(single[1])
			res[1] = float(single[2])
	return res


def junk_mail():
	global file
	word_percentlist = []
	for word in words_cur_mail:
		word_percent_junk = [0.01,0.01]
		word_percent_normal = [0.01,0.01]
		word_percent_junk = get_word_percent(word,filecontent_junk)
		word_percent_normal = get_word_percent(word,filecontent_normal)
		
		pswps = word_percent_junk[0] * 0.5
		pswph = word_percent_normal[0] * 0.5
		psw_junk = pswps / (pswps + pswph)
		res=(word,psw_junk)
		word_percentlist.append(res)
	
	word_percentlist.sort(key=lambda x:x[1])
	word_percentlist_new = word_percentlist[::-1]
	
	finalwords = 0
	if CheckedWords > len(word_percentlist):
		finalwords = len(word_percentlist)
	else:
		finalwords = CheckedWords
	
	pswj = 1.0;
	pswn = 1.0;
	i = 0
		
	for j in word_percentlist_new:
		if i >= finalwords:
			break
		singleper = j[1]
		per = float(singleper)
		per_bak = per
		pswj = pswj * per
		pswn = pswn * (1 - per_bak)
		i += 1
		
	res = pswj / (pswj + pswn)
	print(str(res) + " for the \"" + file + "\".");
	if res >= junklevel:
		return True
	else:
		return False

def analyzemail(mailfile):
	global file
	file = mailfile
	if len(words_cur_mail) > 0:
		words_cur_mail.clear()
	if len(filecontent_junk) > 0:
		filecontent_junk.clear()
	if len(filecontent_normal) > 0:
		filecontent_normal.clear()
	
	read_mail(mailfile)
	read_keywords_data()
	return junk_mail()


def main():
	junkcount = 0
	normalcount = 0;
	allmail = 0
	listresult = []
	read_config()
	print("=========")
	print(mailfolder_junk)
	print(mailfolder_normal)
	print(keywordfile_junk)
	print(keywordfile_normal)
	print(file_studied_mail_junk)
	print(file_studied_mail_normal)
	print(unknown_mail_list)
	print(unknown_mail_check_result)
	print(junklevel)
	print(CheckedWords)
	
	filelist = GetAllFilenameContent(unknown_mail_list)
	allmail = len(filelist)
	for i in filelist:
		b = analyzemail(i)
		res = file
		if b == True:
			res = res + " is a junk mail."
			junkcount += 1
		else:
			res = res + " is a normal mail."
			normalcount += 1

		listresult.append(res)
	
	summary = str(allmail) + " emails and program finds " + str(junkcount) + " junk mail "   + str((junkcount * 100) / allmail) + "%," + " find " + str(normalcount) + " normal mail " + str((normalcount * 100) / allmail) + "%," +" with " + str(junklevel);
	listresult.append(summary);
	
	SaveTextToFileList(listresult, unknown_mail_check_result);
	print("end")

if __name__ == '__main__':
	main()
	
