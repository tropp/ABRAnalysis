from os import listdir, chdir
#import os
from os.path import isfile, join
from optparse import OptionParser

def Pullfiles():
	#create the header
	# mypath = "/Users/tessajonneropp/Desktop/data/10-29-2015_ABR_P74_M_Noise_Exposed/"
	mypath = "/Volumes/TROPPDRIVE/05-31-2017_ABR_P40_CNTNAP2WT/"
	
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	singlefile = onlyfiles[8]
	filebase = singlefile[:14]
	striptxt=[]
	filetypes = ['p', 'n']
	#print filebase
	
	datadate = filebase[:8]
	
	for f in onlyfiles:
		striptxt.append(f[16:-4])

	print striptxt
	# header1 = ":RUN-3  LEVEL SWEEP   TEMP:207.44   4/6/2007  8:03 AM  -3852.21HR: \n"
	# header2 = ":SW EAR:R    SW FREQ:", \n" 
	# header3 = ":NOTES- \n"
	# header4 = ":CHAMBER-412 \n"
	# header5 = "LEVELS: \n"
	# header6 = ":DATA \n"

	# header = header1 + header2 + header3 + header4 + header5 + header6
	print range(len(onlyfiles))
	# print onlyfiles
	#print onlyfiles[7][14]
	for i in range(len(onlyfiles)):
		if any(onlyfiles[i][14] in s for s in filetypes) & (onlyfiles[i][:14]==filebase):
			header1 = ":RUN-3  LEVEL SWEEP   TEMP:207.44   4/6/2007  8:03 AM  -3852.21HR: \n"
			header2 = ":SW EAR:R    SW FREQ:" + striptxt[i] + "  #AVERAGES: 400   REP RATE(/sec): 40  DRIVER: Starship  SAMPLE(usec): 10 \n" 
			header3 = ":NOTES- \n"
			header4 = ":CHAMBER-412 \n"
			header5 = "LEVELS: 20;25;30;35;40;45;50;55;60;65;70;75;80;85;90; \n"
			header6 = ":DATA \n"

			header = header1 + header2 + header3 + header4 + header5 + header6
			chdir(mypath)
			WriteHeader(onlyfiles[i],header)
			print(onlyfiles[i])



	#list of ABR frequencies
	fl1 = [2, 4, 8, 12, 16, 32, 48]

	if any("kHz" in s for s in onlyfiles):
		freqlist = [s for s in onlyfiles if "kHz" in s]
		fr = mypath + freqlist[0]
		freqfile = open(fr,'r')
		freqs = [line for line in freqfile]
	#	intfreqs = [int(i) for i in freqs]
		#check that the frequencies in freqs match those in fl1 (the default) list
	#	set(intfreqs) & set(fl1)

	#list of ABR SPLs
	sl1=[20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]

	if any("SPL" in s for s in onlyfiles):
		levellist = [s for s in onlyfiles if "SPL" in s]
		lvl = mypath + levellist[0]
		levelfile = open(lvl,'r')
		levels = [line for line in levelfile]
		
	# open the levels file and read the levels into a variable

	#open the frequencies file and read the frequencies into a variable

	#read the date from the folder/first file name

	#write the new header to the text file

	#filename = "/Users/tessajonneropp/Desktop/data/10-29-2015_ABR_P74_M_Noise_Exposed/20151029-1100-n-16000.000.txt"
	return

def WriteHeader(filename, header):

	ABRfile = open(filename, 'r')
	
	# remove any matching 'header' from the file, in case ther are duplicate header rows in the wrong places

	lines = [line for line in ABRfile if not line == header]
	ABRfile.close()

	# rewrite the file, appending the header to row 1
	ABRfile = open(filename, 'w')
	ABRfile.write(''.join(header))
	ABRfile.write('\n' .join(lines))
	ABRfile.close()
	return True

if __name__ == '__main__':
	Pullfiles()
    # if WriteHeader(filename, header):
    #     file = open(filename, 'a')
    # # 	file.write()
    #     file.close()
    # else:
    #     print 'there was a problem...'