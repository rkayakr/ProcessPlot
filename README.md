# ProcessPlot
plots processed PSWS files
Bob Benedict, KD8CGH, 8/12/2021

version 1.0
plots up to 10 files from one or more nodes, dates and beacons

modified from WWV_plt2.py @authors dkazdan jgibbons

expects a homepath directory with raw files in subdirs, leaves plot in Mplot directory

windows version hardcoded homepath directory location
for Pi comment out windows homepath and uncomment Pi homepath lines

create text file "plotfiles.txt" in homepath directory
  keyword ('Doppler' or 'Power')
  keyword ('Average' or 'No Average')
  subdir/filename1 
  subdir/filename2
  filename3
  ...

if found 'Doppler' will plot Doppler shifts, else will plot Power
if found 'Average' will plot average of dada
loads file names in list
plots first file and create axis and title info
plots rest in loop as curves on first plot
calculates average and plots
includes sunrise, sunset times requested by Kristina Collins
leaves plotfile in Mplot directory

uses WWV_utility2.py
20 February 2020
WWV utility file
Routines and classes used in WWV file management and graphing
David Kazdan, AD8Y
John Gibbons, N8OBJ - mods to plot header 2/3/2020

uses Beacon.py to read headers
