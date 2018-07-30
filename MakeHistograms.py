#!/usr/bin/python

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import humanize

# https://stackoverflow.com/questions/5328556/histogram-matplotlib#5328669

allSizes = []
allCats = {}
cats = ['image', 'audio', 'pdf', 'video', 'text', 'markup', 'other']
for cat in cats:
  allCats[cat] = []

def makeHist(title, data, bins=100):
  print("Generating histogram for " + title + ", number of points " + str(len(data)))
  fig = plt.figure()
  ax = fig.add_subplot(1,1,1)
  counts, bins, patches = ax.hist(data, bins, histtype='bar')
  #width = 0.7 * (bins[1] - bins[0])
  #width = np.diff(bins)
  #ax.set_xticks(bins)
  #bin_centers = 0.5 * np.diff(bins) + bins[:-1]
  #fig, ax = plt.subplots(figsize=(8,4))
  ax.set_xlabel('File size')
  ax.set_ylabel('# of files')
  xlabels = ax.get_xticks().tolist()
  print(xlabels)
  #ax.set_xscale('log')
  ax.set_yscale('log')
  #otherxlabels = [j.get_text() for j in ax.get_xticklabels()]
  #print(otherxlabels)
  newXlabels = [humanize.naturalsize(x, gnu=True) for x in xlabels]
  print(newXlabels)
  ax.set_xticklabels(newXlabels)
  #xlabels = ax.xaxis.get_major_ticks()
  #ax.set_xticklabels([humanize.naturalsize(x, gnu=True) for x in xlabels])
  #print(newXlabels)
  #ax.set_xticklabels(newXlabels)
  #ax.set_xticks(bins)
  #ax.set_xticks(chunk_sizes)
  #ax.bar(center, hist, align='center', width=width)
  #plt.bar(center, hist, align='center', width=width)
  fig.suptitle(title)
  plt.subplots_adjust(bottom=0.15)
  titleClass = title.split("_")[0]
  if (not os.path.exists('figs/' + titleClass)):
    os.makedirs('figs/' + titleClass)
  fig.savefig('figs/' + titleClass + '/' + title + "_hist.png")
  plt.close(fig)
  # plt.show()

def processFile(fn):

  global allCats, allSizes, cats

  folder = fn.split('.')[0]
  inTotals = False
  folderSizes = []
  with open(fn, 'r') as f:
    for line in f:
      if (line.find('ALL SIZES BY FILE TYPE:') == 0):
        print("Found totals line")
        inTotals = True
        continue
      else:
        if (inTotals == True):
          print("Looking at totals line")
          if (line.strip() == ""):
            inTotals = False
          else:
            lineA = line.strip().split(": ")
            fileCat = lineA[0]
            print("cat is " + fileCat)
            if(fileCat not in cats):
              fileCat = 'other'
            fileSizes = lineA[1].split(" ")
            fileSizes = [float(i) for i in lineA[1].split(" ")] 
            folderSizes += fileSizes
            allCats[fileCat] += fileSizes
            allSizes += fileSizes
            makeHist(folder + "_" + fileCat, fileSizes)
  if (len(allSizes) > 0):
    makeHist(folder + "_" + 'all', folderSizes)

# MAIN
if (not os.path.exists('figs')):
  os.makedirs('figs')

processFile('dlmasters.txt')
processFile('othermasters.txt')
processFile('Maps.txt')
processFile('Livingstone.txt')
processFile('EMEL.txt')
processFile('CDLIMasters.txt')
#processFile('DEP.txt')
   
for cat in allCats:
  makeHist('all_' + cat, allCats[cat])
makeHist('all_DL_files', allSizes)
