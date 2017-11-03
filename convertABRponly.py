from os import listdir, chdir
#import os
from os.path import isfile, join
from optparse import OptionParser
import pandas as pd
import numpy as np
import argparse
import math
import sys



#current 12/08/2015
class conversion():

	def __init__(self):
		global state 
		self.SPLs = []
		self.freqs = []
		self.ABRlevels =[]

	def parse_and_go(self):
		global state
		parser = argparse.ArgumentParser("convertABR.py")
		parser.add_argument('-c', '--click', action='store_true', dest='click',default=False,help='click waveforms')
		parser.add_argument('-f', '--freqs', action='store_true', dest='freqs',default=True, help='frequency waveforms')
		parser.add_argument('-d', '--directory', action='store', dest='directory',help='Default directory for files')
		options = parser.parse_args()
		if options.freqs is True:
			state = False
		if options.click is True:
			state = True
		self.Pullfiles(options.directory)

	def Pullfiles(self,directory=''):
		freqs=[]
		#create the header
		#mypath = "/Users/tjropp/Desktop/data/ABR_DATA/11-23-2015_ABR_P96_M_Noise_Exposed"
		#mypath = "/Users/tessajonneropp/Desktop/data/ABR_data/Tessa_ABR_data/08-16-2016_ABR_P148_F3_Noise_Exposed"
		# mypath = "/Volumes/TROPPDATA/ABR_data/Ruili_ABR_data/backed_up/04272012-P120-CBAnormal-F-1-note"
		global state
		mypath=directory
		onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
		print 'onlyfiles:', onlyfiles

		striptxt=[]
		filetypes = ['p', 'n']
		#print filebase
		if state is False:
			for f in onlyfiles:
				if 'kHz' in f:
					freqs = pd.io.parsers.read_csv(join(mypath, f),delim_whitespace=True, lineterminator='\r', names='ab',header=None, skip_blank_lines=True)
					# freqs = pd.io.parsers.read_csv(join(mypath, f),sep='\r\t',lineterminator='\r', skip_blank_lines=True)
					# freqs = pd.io.parsers.read_csv(join(mypath, f),usecols=0,lineterminator='\r', skip_blank_lines=True)
					# striptxt = freqs.tolist()
					for col in freqs.columns:
						for i in range(len(freqs)):
							striptxt.append(freqs[col][i])
					print 'freqlist:', striptxt
			temp =[]
			for i in range(len(striptxt)):
				if striptxt[i]!='\n':
					if math.isnan(float(striptxt[i])) is False:
						temp.append(int(float(striptxt[i])))
			print 'freqlist (2nd printing):', temp
			striptxt = []
			self.freqs = temp
			datadate = filebase[:8]
		else:
			onlythese =[]
			avoid = []
			for f in onlyfiles:
				if len(f)<22:
					if len(f)>14:	
						onlythese.append(f)
				
				
				
			onlyfiles = onlythese
			print 'onlyfiles:', onlyfiles
		# for f in onlyfiles:
		# 	if state is False:
		# 		striptxt.append(f[16:-8])
		# 	else:
		# 		striptxt.append(f[14:-4])
		# print 'striptxt',striptxt
		#ABRfiles = onlyfiles
		ABRfiles = self.combinepolarity(mypath,onlyfiles)
		#print range(len(ABRfiles))
		print 'ABRfiles:', ABRfiles
		for i in range(len(ABRfiles)):
			#if any(ABRfiles[i][14] in s for s in filetypes) & (ABRfiles[i][:14]==filebase):
			header1 = ":RUN-3	LEVEL SWEEP	TEMP:207.44 20120427 8:03 AM	-3852.21HR: \n"
			if state is False:
				header2 = ":SW EAR: R	SW FREQ: " + str(self.freqs[i]) + "9.00	# AVERAGES: 512	REP RATE (/sec): 40	DRIVER: Starship	SAMPLE (usec): 10 \n"
			else:
				header2 = ":SW EAR: R	SW FREQ: 19	# AVERAGES: 512	REP RATE (/sec): 40	DRIVER: Starship	SAMPLE (usec): 10 \n"
			header3 = ":NOTES- \n"
			header4 = ":CHAMBER-412 \n"
			header5 = self.ABRlevels+"\n"
			header6 = ":DATA \n"
			# header1 = ":RUN-3  LEVEL SWEEP   TEMP:207.44   4/6/2007  8:03 AM  -3852.21HR: \n"
			# header2 = ":SW EAR:R    SW FREQ:" + striptxt[i] + "  #AVERAGES: 400   REP RATE(/sec): 40  DRIVER: Starship  SAMPLE(usec): 10 \n" 
			# header3 = ":NOTES- \n"
			# header4 = ":CHAMBER-412 \n"
			# header5 = "LEVELS: 20;25;30;35;40;45;50;55;60;65;70;75;80;85;90; \n"
			# header6 = ":DATA \n"

			header = header1 + header2 + header3 + header4 + header5 + header6
			chdir(mypath)

			self.WriteHeader(ABRfiles[i],header)
			#print(ABRfiles[i])



		# #list of ABR frequencies
		# fl1 = [2, 4, 8, 12, 16, 32, 48]

		# if any("kHz" in s for s in onlyfiles):
		# 	freqlist = [s for s in onlyfiles if "kHz" in s]
		# 	fr = mypath + freqlist[0]
		# 	freqfile = open(fr,'r')
		# 	freqs = [line for line in freqfile]
		# #	intfreqs = [int(i) for i in freqs]
		# 	#check that the frequencies in freqs match those in fl1 (the default) list
		# #	set(intfreqs) & set(fl1)

		# #list of ABR SPLs
		# sl1=[20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]

		# if any("SPL" in s for s in onlyfiles):
		# 	levellist = [s for s in onlyfiles if "SPL" in s]
		# 	lvl = mypath + levellist[0]
		# 	levelfile = open(lvl,'r')
		# 	levels = [line for line in levelfile]
			
		# open the levels file and read the levels into a variable

		#open the frequencies file and read the frequencies into a variable

		#read the date from the folder/first file name

		#write the new header to the text file

		#filename = "/Users/tessajonneropp/Desktop/data/10-29-2015_ABR_P74_M_Noise_Exposed/20151029-1100-n-16000.000.txt"
		return
	def combinepolarity(self,mypath,onlyfiles):
		global state
	
		pf = []
		ABRfiles=[]
		
		if state is False:
			for f in onlyfiles:
				if len(f)>22:
					if 'p' in f:
						pf.append(f)
					
		else:
			for f in onlyfiles:
				if 'p' in f:
					pf.append(f)


		print 'pf:', pf

		#list of ABR frequencies
		# fl1 = ['02000.000', '4000.000', '8000.000', '12000.000', '16000.000', '24000.000', '32000.000', '48000.000']

		# fl1 = striptxt[8:-1]

		pff=[]
		fl1 = self.freqs
		for ABRfreq in fl1:
			print 'ABRfreq', ABRfreq
			ABRfreq = str(ABRfreq)
			if any(ABRfreq in pff for pff in pf):
			# nindex = nf.find(ABRfreq)
			# pindex = pf.find(ABRfreq)
			# if nindex != -1:
				
				pff = [genfile for genfile in pf if ABRfreq in genfile]
				print 'positive file:', pff
				chdir(mypath)
				posf = pd.io.parsers.read_csv(pff[0],delim_whitespace=True, lineterminator='\r', skip_blank_lines=True, header=0)
				posseries=[]
				
				for col in posf.columns:
					for i in range(len(posf)):
						posseries.append(posf[col][i])

					#posseries.append(posf[col])
			
				wvfmdata = posseries
				
				print 'lenght of wvfmdata:', len(wvfmdata)
				wvnumpts = len(posf[col])
				print 'num wvpts:', len(posf[col])
				print 'length of posseries:', len(posseries)
				
				SPLfile = pff[0][:14]+'SPL.txt'
				print 'SPLfile:', SPLfile
				# freqs = pd.io.parsers.read_csv(join(mypath, f),delim_whitespace=True, lineterminator='\r', names='ab',header=None, skip_blank_lines=True)
				SPLdata = pd.io.parsers.read_csv(SPLfile,delim_whitespace=True, lineterminator='\r', names='ab',skip_blank_lines=True, header=None)
				
				print 'SPLdata:', SPLdata
				levels = []
				for lcol in SPLdata.columns:
					for i in range(len(SPLdata)):
						levels.append(SPLdata[lcol][i])
				
				temp =[]
				for i in range(len(levels)):
					if levels[i]!='\n':
						if math.isnan(float(levels[i])) is False:
							temp.append(int(float(levels[i])))
				levels= []
				levels=temp
				print 'levels:', levels
				self.ABRlevels = ':LEVELS:'
				for i in range(len(levels)):
					self.ABRlevels = self.ABRlevels + str(levels[i]) + ';'
				# numSPL = 15
				waves=np.reshape(wvfmdata,(len(levels),wvnumpts))
				twaves=waves.T
				
				if state is False:
					denote = 'ABR-' + ABRfreq + '9-3'
				else:
					denote = 'ABR-19-3'

				np.savetxt(denote,twaves,delimiter='\t ',newline='\r\n')
				ABRfiles.append(denote)
			else:
				print 'No file with this frequency', ABRfreq
		if len(fl1)==0:
			print 'up in here'
			pff = [genfile for genfile in pf if 'p' in genfile]
			print 'positive file:', pff
			chdir(mypath)
			posf = pd.io.parsers.read_csv(pff[0],delim_whitespace=True, lineterminator='\r', skip_blank_lines=True, header=0)
			posseries=[]
			
			for col in posf.columns:
				for i in range(len(posf)):
					posseries.append(posf[col][i])
		
			wvfmdata = posseries
			
			print 'lenght of wvfmdata:', len(wvfmdata)
			wvnumpts = len(posf[col])
			print 'num of wvpts:', len(posf[col])
			print 'length of posseries:', len(posseries)
			
			SPLfile = pff[0][:14]+'SPL.txt'
			print 'SPLfile:', SPLfile
			# freqs = pd.io.parsers.read_csv(join(mypath, f),delim_whitespace=True, lineterminator='\r', names='ab',header=None, skip_blank_lines=True)
			SPLdata = pd.io.parsers.read_csv(SPLfile,delim_whitespace=True, lineterminator='\r', names='ab',skip_blank_lines=True, header=None)
			
			print 'SPLdata:', SPLdata
			levels = []
			for lcol in SPLdata.columns:
				for i in range(len(SPLdata)):
					levels.append(SPLdata[lcol][i])
			
			temp =[]
			for i in range(len(levels)):
				if levels[i]!='\n':
					if math.isnan(float(levels[i])) is False:
						temp.append(int(float(levels[i])))
			levels= []
			levels=temp
			print 'levels:', levels
			countmax = len(levels)-1
			self.ABRlevels = ':LEVELS:'
			for i in range(len(levels)):
				self.ABRlevels = self.ABRlevels + str(levels[countmax-i]) + ';'
			# numSPL = 15
			print 'number of levels:', len(levels)
			waves=np.reshape(wvfmdata,(len(levels),wvnumpts))
			twaves=waves.T
			if state is False:
				denote = 'ABR-' + ABRfreq + '9-3'
			else:
				denote = 'ABR-19-3'
			np.savetxt(denote,twaves,delimiter='\t ',newline='\r\n')
			ABRfiles.append(denote)
		return	ABRfiles
	def WriteHeader(self,filename, header):


		ABRfile = open(filename, 'r')

		# remove any matching 'header' from the file, in case ther are duplicate header rows in the wrong places

		lines = [line for line in ABRfile if not line == header]
		ABRfile.close()

		# rewrite the file, appending the header to row 1
		ABRfile = open(filename, 'w')
		ABRfile.write(''.join(header))
		ABRfile.write('\n' .join(lines))
		ABRfile.write(''.join('\r\r'))
		ABRfile.close()
		return True


if __name__ == '__main__':
	cons = conversion()
	cons.parse_and_go()

		
    # if WriteHeader(filename, header):
    #     file = open(filename, 'a')
    # # 	file.write()
    #     file.close()
    # else:
    #     print 'there was a problem...'