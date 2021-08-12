#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROCESSED FILE VERSION V1.0 built on multiPlot v1.2

multiPlot version v1.2 cleans up to make Pi and Windows use easier

multiPlot version v1.1 adds sunrise sunset times for location of lat long in first file
requires suntime library https://github.com/SatAgro/suntime

multiPlot version v1.0 plots up to 10 PSWS "rawdata" files and average value
modified from WWV_plt2.py @authors dkazdan jgibbons
expects a homepath directory with processed files in homepath or subdirs 
leaves plot in Mplot directory
plots files from multiple subdir to compare node results
plot title from first file

windows version hardcoded homepath directory location
for Pi comment out windows homepath and uncomment Pi  lines

uses WWV_utility2.py
Bob Benedict, KD8CGH, 7/29/2021

create text file "plotfiles.txt" in homepath directory
  keyword ('Doppler' or 'Power')
  keyword ('Average' or 'No Average')
  subdir/filename1 
  subdir/filename2
  filename3
  ...

Note - expects all data from the same beacon

if found 'Doppler' will plot Doppler shifts, else will plot Power
if found "Average" will add average plot

loads file names in list
plots first file and create axis and title info
plots rest in loop as curves on first plot
calculates average and plots
leaves plotfile in Mplot directory

uses
WWV_utility2.py
20 February 2020
WWV utility file
Routines and classes used in WWV file management and graphing
David Kazdan, AD8Y
John Gibbons, N8OBJ - mods to plot header 2/3/20

"""

#import os # uncomment for pi
from os import path
import sys
import csv
import math
#import shutil  # uncomment for pi
#from datetime import date, timedelta  # uncomment for pi
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import filtfilt, butter
import datetime  
from suntime import Sun, SunTimeException
#import subprocess
from WWV_utility2 import time_string_to_decimals
from Beacon import readheader

'''  #uncomment for Pi
# ~ points to users home directory - usually /home/pi/
homepath = os.path.expanduser('~')

# imbed the trailing / in the home path
homepath = homepath + "/PSWS/"

#comment out windows homepath
'''

homepath = "E:\\Documents\\PSWS\\"  # set your windows path, comment out for Pi

names = open(homepath+"Processfiles.txt","r")

PlotTarget = names.readline()
PlotTarget = PlotTarget.strip('\n')
PlotAverage = names.readline()
if PlotAverage[0:7] == 'Average':
    doavg=True
else:
    doavg=False

Filenames=['a' for a in range (10)]
Filedates=['a' for a in range (10)]
PrFilenames=['a' for a in range (10)]
Nodenum=['a' for a in range (10)]
Beaconname=['a' for a in range (10)]
beaconfreq=np.zeros(10)

nfiles = 0  # holder for number of files to plot

colors=['b','g','r','c','m','y','tab:orange','tab:gray','tab:purple','tab:brown']

while True:
    temp = names.readline()
    if  len(temp) <= 1:
        break
    Filenames[nfiles]=temp.strip("\n")
    fdate = Filenames[nfiles].find("/") # find start of filename after subdirectory
    if fdate==-1 :  # if / not found try \
        fdate = Filenames[nfiles].find("\\")
#    print(" position ",fdate)
    # if neith / nor \ found file is in homepath, fdate=-1, following assignment still works
    Filedates[nfiles]=temp[fdate+1:fdate+11]
    nfiles=nfiles + 1
        
#print(Filenames[0:9])
#print(Filedates[0:9])
print('number of files',nfiles)
if nfiles > 10 :
    print('10 file limit')
    sys.exit(0)

PROCESSDIR = homepath

#saved plot directrory
PlotDir = homepath + 'Mplot/'

'''
read first file
'''
PrFilenames=(PROCESSDIR + Filenames[0])

if (path.exists(PrFilenames)):
    print('File ' + PrFilenames + ' found!\nProcessing...')
else:
    print('File ' + PrFilenames + ' not available.\nExiting disappointed...')
    sys.exit(0)

with open(PrFilenames, 'r') as dataFile:
    dataReader=csv.reader(dataFile)
    data = list(dataReader)
    Header = data.pop(0)

#    print('return',readheader(0,Header))
    Nodenum[0], Beaconname[0], beaconfreq[0], Lat, Long = readheader(Header)
#    print('\n returned ', Nodenum[0], Beaconname[0], beaconfreq[0], Lat, Long, '\n')

''' ###########################################################################
'''
print('Ready to start processing records')

# Prepare data arrays
hours=[[],[],[],[],[],[],[],[],[],[]]
Doppler=[[],[],[],[],[],[],[],[],[],[]]
#Vpk=[[],[],[],[],[],[],[],[],[],[]]
Power_dB=[[],[],[],[],[],[],[],[],[],[]] # will be second data set, received power 9I20
filtDoppler=[[],[],[],[],[],[],[],[],[],[]]
filtPower=[[],[],[],[],[],[],[],[],[],[]]

LateHour=False # flag for loop going past 23:00 hours

# eliminate all metadata saved at start of file - Look for UTC (CSV headers)
#find first row of data0
FindUTC = 0

for row in data:
    if (FindUTC == 0):
        #print('looking for UTC - row[0] =',row[0])
        if (row[0] == 'UTC'):
            FindUTC = 1
#            print('UTC found =', row[0])
    else:
        #print('Processing record')
        decHours=time_string_to_decimals(row[0])
#        if (NewHdr != 'New'):
#            if (calccnt  < 101):
#                calcnt = calcnt+1
#                freqcalc = freqcalc + (float(row[1])/100)
#        if decHours > 23:
#            LateHour=True # went past 23:00 hours
        if (not LateHour) or (LateHour and (decHours>23)): # Otherwise past 23:59:59.  Omit time past midnight.
            hours[0].append(decHours) # already in float because of conversion to decimal hours.
            Doppler[0].append(float(row[1])-beaconfreq[0]) # frequency offset from col 2
#            Vpk[0].append (float(row[2])) # Get Volts peak from col 3
            Power_dB[0].append (20*math.log10(float(row[2]))) # log power from col 4

#print('nf ',0,'len hours',len(hours[0]))

###############################################################################################
# Find max and min of Power_dB for graph preparation:
min_power=np.amin(Power_dB[0]) # will use for graph axis min
max_power=np.amax(Power_dB[0]) # will use for graph axis max

min_Doppler=np.amin(Doppler[0]) # min Doppler
max_Doppler=np.amax(Doppler[0]) # max Doppler

print('\nDoppler min: ', min_Doppler, '; Doppler max: ', max_Doppler)
print('dB min: ', min_power, '; dB max: ', max_power)

#%% Create an order 3 lowpass butterworth filter.
# This is a digital filter (analog=False)
# Filtering at .01 to .004 times the Nyquist rate seems "about right."
# The filtering argument (Wn, the second argument to butter()) of.01
# represents filtering at .05 Hz, or 20 second weighted averaging.
# That corresponds with the 20 second symmetric averaging window used in the 1 October 2019
# Excel spreadsheet for the Festival of Frequency Measurement data.
#FILTERBREAK=.005 #filter breakpoint in Nyquist rates. N. rate here is 1/sec, so this is in Hz.
FILTERBREAK=0.005 #filter breakpoint in Nyquist rates. N. rate here is 1/sec, so this is in Hz.
FILTERORDER=6
b, a = butter(FILTERORDER, FILTERBREAK, analog=False, btype='low')
#print (b, a)
#%%
# Use the just-created filter coefficients for a noncausal filtering (filtfilt is forward-backward noncausal)


filtDoppler[0] = filtfilt(b, a, Doppler[0])

filtPower[0] = filtfilt(b, a, Power_dB[0])

##################################################################################################
# sunrise sunset times in UTC
sun = Sun(float(Lat), float(Long))

UTC_DT=Filedates[0]
print(UTC_DT)
SDAY=int(UTC_DT[8:10])
SMON=int(UTC_DT[5:7])
SYEAR=int(UTC_DT[0:4])
sdate = datetime.date(SYEAR, SMON, SDAY)
today_sr = sun.get_sunrise_time(sdate)
today_ss = sun.get_sunset_time(sdate)
#print(today_sr)
srh=int(format(today_sr.strftime('%H')))
srm=int(format(today_sr.strftime('%M')))
srx=srh+srm/60
ssh=int(format(today_ss.strftime('%H')))
ssm=int(format(today_ss.strftime('%M')))
ssx=ssh+ssm/60

# set up x-axis with time
fig = plt.figure(figsize=(19,10)) # inches x, y with 72 dots per inch
ax = fig.add_subplot(111)
ax.set_xlabel('UTC Hour')
ax.set_xlim(0,24) # UTC day
ax.set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24], minor=False)

# plot first curve
if (PlotTarget == 'Doppler'):
    ax.plot([srx,srx],[-1,1],'y',label='sunrise',linestyle='dashed')
    ax.plot([ssx,ssx],[-1,1],'b',label='sunset',linestyle='dashed')
    ax.plot(hours[0], filtDoppler[0], colors[0],label=Beaconname[0] +' '+Nodenum[0]+' '+Filedates[0]) # color k for black
    ax.set_ylabel('Doppler shift, Hz '+ Filedates[0])
    ax.set_ylim([-1.0, 1.0]) # -1 to 1 Hz for Doppler shift
    plt.axhline(y=0, color="gray", lw=1) # plot a zero freq reference line for 0.000 Hz Doppler shift
    
    
else:
    ax.plot([srx,srx],[-90,0],'y',label='sunrise',linestyle='dashed')
    ax.plot([ssx,ssx],[-90,0],'b',label='sunset',linestyle='dashed')
    ax.plot(hours[0], filtPower[0], colors[0],label=Beaconname[0] +' '+ Nodenum[0]+' '+Filedates[0]) # color k for black
    ax.set_ylabel('Power, dB '+ Filedates[0])
    ax.set_ylim(-90, 0)    
    
    
# add grid lines - RLB
plt.grid(axis='both')

'''
######################################################################
read and plot files loop
'''

for nf in range(1, nfiles):
# splot second curve
# read second file, skip header
    print('process file ',nf, Filenames[nf])
    PrFilenames=(PROCESSDIR + Filenames[nf])
    with open(PrFilenames, 'r') as dataFile: # read second set
        dataReader=csv.reader(dataFile)
        data = list(dataReader)
        Header = data.pop(0)
        Nodenum[nf]= Header[2]
    FindUTC = 0
    
    Nodenum[nf], Beaconname[nf], beaconfreq[nf], Lat, Long = readheader(Header)
#    print('\n returned ', Nodenum[nf], Beaconname[nf], beaconfreq[nf], Lat, Long, '\n')

    for row in data:
        if (FindUTC == 0):
            #print('looking for UTC - row[0] =',row[0])
            if (row[0] == 'UTC'):
                FindUTC = 1
#            print('UTC found =', row[0])
        else:
            decHours=time_string_to_decimals(row[0])
            hours[nf].append(decHours) # already in float because of conversion to decimal hours.
            Doppler[nf].append(float(row[1])-beaconfreq[nf]) # frequency offset from col 2
#            Vpk[nf].append (float(row[2])) # Get Volts peak from col 3
#            Power_dB[nf].append (float(row[4])) # log power from col 4    
            Power_dB[nf].append (20*math.log10(float(row[2]))) # log power
# filter  file data
    filtDoppler[nf] = filtfilt(b, a, Doppler[nf])
    filtPower[nf] = filtfilt(b, a, Power_dB[nf])

    if (PlotTarget == 'Doppler'):    
        ax.plot(hours[nf], filtDoppler[nf], colors[nf], label=Beaconname[nf] +' '+ Nodenum[nf]+' '+Filedates[nf]) # color k for black
    else:
        ax.plot(hours[nf], filtPower[nf], colors[nf], label=Beaconname[nf] +' '+ Nodenum[nf]+' '+Filedates[nf]) # color k for black

'''
#############################################################################
end for read and plot loop, start average
'''
# find shortest data set, limit average to that
if doavg :
    al=1000000
    ak=0

    for k in range(nfiles):
        templ=len(hours[k])
        if templ < al:
            al=templ
            ak=k

    avg=[]

    if (PlotTarget == 'Doppler'):
        for i in range(al):
            temp=0.0
            for j in range(nfiles):
                temp=temp+filtDoppler[j][i]
            temp=temp/nfiles
            avg.append(temp)
    else:
        for i in range(al):
            temp=0.0
            for j in range(nfiles):
                temp=temp+filtPower[j][i]
            temp=temp/nfiles
            avg.append(temp)

    #print('avg',len(avg))

    ax.plot(hours[ak], avg, 'k', label='Average') # color k for black

'''
end average
'''
ax.legend(loc="lower right",  frameon=False)


# Create Plot Title
plt.title(' Grape Data Plot')
#plt.title(beaconlabel + ' Grape Data Plot\nNode:  ' + node + '     Gridsquare:  '+ GridSqr + '\nLat= ' + Lat + '    Long= ' + Long + '    Elev= ' + Elev + ' M\n' )
# Create Plot File Nam
#GraphFile = yesterdaystr + '_' + node + '_' + RadioID + '_' + GridSqr + '_' + beacon + '_graph.png'
GraphFile = 'multi'+ PlotTarget + '.png'
PlotGraphFile = PlotDir + GraphFile

# create plot
#plt.savefig(PlotDir + yesterdaystr + '_' + node + '_' +  GridSqr + '_' +  RadioID + '_' +  beacon + '_graph.png', dpi=250, orientation='landscape')
plt.savefig(PlotDir + GraphFile, dpi=250, orientation='landscape')
# =============================================================================

print('Plot File: ' + GraphFile + '\n')  # indicate plot file name for crontab printout


#-------------------------------------------------------------------
print('Exiting python multi plot program gracefully')
