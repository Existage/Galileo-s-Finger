#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gpsdata.py
#  
#  Copyright 2019 Travis <travis@travis-Dell-System-XPS-L502X>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import subprocess

def getRaw(): #returns raw gpspipe data as string
	p = subprocess.Popen("gpspipe -r -n 50", stdout=subprocess.PIPE , shell=True)#opens pipe to gpspipe for 5 packets of data
	(output, err) = p.communicate()
	p_status = p.wait()
	#print "GPS NMEA DATA: ", output
	print "ERROR MESSAGES: ", err
	return output

def findFixes(data): #finds GPGGA sentences and returns list of entries
	term = "GPGGA"
	rawSentences = data.split("$")
	sentences = []
	for x in rawSentences: #loops through list and finds GPGGA sentences and removes \n char from entries
		if term in x:
			s = x.replace('\r\n' , '')
			sentences.append(s)
	
	return sentences

def sentenceToList(sentence):#splits up sentence into list
		out = sentence.split(',')
		return out
		 
def getTime(sentence): #fetches time from sentence
	out = sentence[1]
	return out[0:6]

def getLatitude(sentence): #fetches latitude from sentence and adds + or - to indicate N or S
	if sentence[3] == 'N':
		return sentence[2]
	else:
		return("-"+sentence[2])

def getLogitude(sentence): #fetches longitude from sentence and adds + or - to indicate E or W
	if sentence[5] == 'E':
		return sentence[4]
	else:
		return('-',sentence[4])

def getAlt(sentence):
	return sentence[10]

def average(data):
	total = 0
	count =0
	for k in data:
		#print k
		total += float(k)
		count += 1
	out = round(total/count , 4)
	if out >= 0:
		return '+' + str(out)
	else:
		return str(out)
	



def main(args):
	
	
	#data management
	raw = getRaw()
	fixList = findFixes(raw)
	#print fixList
	time = []
	lat = []
	lgt = []
	for i in fixList: #populate time, lat and lgt lists
		line = sentenceToList(i)
		time.append(getTime(line))
		lat.append(getLatitude(line))
		lgt.append(getLogitude(line))
	
	
	#print (average(lat),average(lgt),int(time[-1])) 	
	print '--latitude {}d{}\"{}\' --longitude {}d{}\"{}\' --time {}'.format(average(lat)[0:3],average(lat)[3:5],average(lat)[6:8]+'.'+average(lat)[8:], average(lgt)[0:3],average(lgt)[3:5],average(lgt)[6:8]+'.'+average(lgt)[8:], time[-1])
	
	
	#sortedList
	
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
