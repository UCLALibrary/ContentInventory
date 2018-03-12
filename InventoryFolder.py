#!/usr/bin/python

import sys
import os
import json
import humanize
import operator

fCats = {'mp3':  'audio',
'ra':  'audio',
'rm':  'audio',
'rng':  'audio',
'sfk':  'audio',
'wav':  'audio',
'wma':  'audio',
'dwg':  'CAD',
'bmp':  'image',
'eps':  'image',
'jp2':  'image',
'jpeg':  'image',
'jpg': 'image',
'png':  'image',
'ps':  'image',
'psd':  'image',
'tif':  'image',
'tiff':  'image',
'atf': 'text',
'pdf':  'pdf',
'pff':  'pdf',
'pps':  'powerpoint',
'ppt':  'powerpoint',
'xls':  'speadsheet',
'doc':  'text',
'docx':  'text',
'rtf':  'text',
'txt':  'text',
'asf':  'video',
'avi':  'video',
'dcr':  'image',
'f4v':  'video',
'flv':  'video',
'gif':  'image',
'm4a':  'audio',
'mov':  'video',
'mp4_old':  'video',
'mp4':  'video',
'mpeg':  'video',
'mpg':  'video',
'ram':  'audio',
'swf':  'video',
'wmv':  'video',
'apf':  'data',
'asp': 'program',
'asp^language=english': 'program',
'asp^language=spanish': 'program',
'bat':  'program',
'cab':  'program',
'cache':  'misc',
'children':  'misc',
'class':  'program',
'css':  'markup',
'cvs':  'error',
'dat':  'data',
'db':  'data',
'dcl':  'CAD',
'ds_store':  'misc',
'dtd':  'markup',
'ent':  'error',
'exe':  'program',
'gz':  'data',
'htm':  'markup',
'html':  'markup',
'icc':  'data',
'jar':  'program',
'js':  'program',
'list':  'data',
'log':  'data',
'md5': 'data',
'mem':  'data',
'misc':  'misc',
'mpp':  'misc',
'php':  'program',
'pl':  'program',
'pm':  'program',
'rdf':  'data',
'rev':  'data',
'sh':  'program',
'shtml':  'markup',
'sit':  'data',
'soc':  'misc',
'tmpl':  'markup',
'tpl':  'misc',
'xlsx':  'spreadsheet',
'xml':  'markup',
'zip':  'data'
}

def writeReports(data, reportsPath, targetName):

  subPath = os.path.join(reportsPath, 'subdirs')
  if (not os.path.isdir(subPath)):
    os.mkdir(subPath)

  summaryFile = open(os.path.join(reportsPath, targetName) + '.txt', 'w')

  summaryFile.write('TOTALS for ' + targetName + ":\n\n")

  summaryFile.write('TOTAL FILES: ' + "{:,}".format(data['count']) + "\n")
  summaryFile.write('SPACE USED: ' + humanize.naturalsize(data['size'], gnu=True) + "\n")
  
  summaryFile.write("\nFILE TYPES:\n")

  def getSize(item):
    return item[1]['size']
  
  sortedCats = sorted(data['cats'].items(), key=getSize, reverse=True)
  for fileInfo in sortedCats:
    fileCat = fileInfo[0]
    summaryFile.write(fileCat + ": " + "{:,}".format(data['cats'][fileCat]['count']) + " (" + humanize.naturalsize(data['cats'][fileCat]['size'], gnu=True) + ")\n")
  
  summaryFile.write("\nFILE EXTENSIONS:\n")

  sortedTypes = sorted(data['types'].items(), key=getSize, reverse=True)
  for fileInfo in sortedTypes:
    fileType = fileInfo[0]
    summaryFile.write(fileType + ": " + "{:,}".format(data['types'][fileType]['count']) + " (" + humanize.naturalsize(data['types'][fileType]['size'], gnu=True) + ")\n")
    
  for folder in data['dirs']:
    if (folder == 'root'):
      summaryFile.write("\nFILES IN ROOT FOLDER ONLY\n\n")
    else:
      summaryFile.write("\nSUB-FOLDER " + folder + "\n\n")

    subFile = folder.split('/')[-1]

    folderFile = open(os.path.join(subPath, subFile) + ".txt", "w")

    summaryFile.write('TOTAL FILES: ' + "{:,}".format(data['dirs'][folder]['count']) + "\n")
    summaryFile.write('SPACE USED: ' + humanize.naturalsize(data['dirs'][folder]['size'], gnu=True) + "\n")
  
    summaryFile.write("\nFILE TYPES:\n")

    sortedCats = sorted(data['dirs'][folder]['cats'].items(), key=getSize, reverse=True)
    #for fileType in data['dirs'][folder]['cats']:
    for fileInfo in sortedCats:
      fileCat = fileInfo[0]
      summaryFile.write(fileCat + ": " + "{:,}".format(data['dirs'][folder]['cats'][fileCat]['count']) + " (" + humanize.naturalsize(data['dirs'][folder]['cats'][fileCat]['size'], gnu=True) + ")\n")
    
    summaryFile.write("\nFILE EXTENSIONS:\n")

    sortedTypes = sorted(data['dirs'][folder]['types'].items(), key=getSize, reverse=True)
    #for fileType in data['dirs'][folder]['types']:
    for fileInfo in sortedTypes:
      fileType = fileInfo[0]
      summaryFile.write(fileType + ": " + "{:,}".format(data['dirs'][folder]['types'][fileType]['count']) + " (" + humanize.naturalsize(data['dirs'][folder]['types'][fileType]['size'], gnu=True) + ")\n")
    
    folderFile.write("SUB-FOLDER " + folder + "\n\n")
    folderFile.write('TOTAL FILES: ' + "{:,}".format(data['dirs'][folder]['count']) + "\n")
    folderFile.write('SPACE USED: ' + humanize.naturalsize(data['dirs'][folder]['size'], gnu=True) + "\n")
    
    folderFile.write("\nFILE TYPES:\n")

    sortedCats = sorted(data['dirs'][folder]['cats'].items(), key=getSize, reverse=True)
    for fileInfo in sortedCats:
      fileCat = fileInfo[0]
      folderFile.write(fileCat + ": " + "{:,}".format(data['dirs'][folder]['cats'][fileCat]['count']) + " (" + humanize.naturalsize(data['dirs'][folder]['cats'][fileCat]['size'], gnu=True) + ")\n")
  
    folderFile.write("\nFILE EXTENSIONS:\n")

    sortedTypes = sorted(data['dirs'][folder]['types'].items(), key=getSize, reverse=True)
    #for fileType in data['dirs'][folder]['types']:
    for fileInfo in sortedTypes:
      fileType = fileInfo[0]
      folderFile.write(fileType + ": " + "{:,}".format(data['dirs'][folder]['types'][fileType]['count']) + " (" + humanize.naturalsize(data['dirs'][folder]['types'][fileType]['size'], gnu=True) + ")\n")

    folderFile.close()

  summaryFile.close()

def countFile(filepath):
  
  targetFile = filepath.split(os.sep)[-1]

  #print("Counting file " + targetFile)

  if (targetFile.find('.') < 0):
    fileType = 'misc'
    fileCat = 'misc'
  else:
    fileType = targetFile.split(".")[-1].lower()
    if (fileType in fCats):
      fileCat = fCats[fileType]
    else:
      print("Uncategorized file extension: " + fileType)
      fileCat = 'misc'
  #fullFilepath = os.path.realpath(filepath)
  try:
    fileSize = os.path.getsize(filepath)
  except:
    print("Unable to access " + filepath)
    fileSize = 0

  return({'fileType': fileType, 'fileCat': fileCat, 'fileSize': fileSize})

def walkPath(targetPath):

  localStats = {'count': 0, 'size': 0, 'types': {}, 'cats': {}, 'sizes': []}

  for dirpath, dirnames, filenames in os.walk(targetPath):
    for thisFile in filenames:
      #print os.path.join(dirpath, thisFile)
      filepath = dirpath + os.sep + thisFile

      fileInfo = countFile(filepath)
      fileType = fileInfo['fileType']
      fileCat = fileInfo['fileCat']
      fileSize = fileInfo['fileSize']

      if (fileType not in localStats['types']):
        localStats['types'][fileType] = {'count': 1, 'size': fileSize, 'sizes': [fileSize]}
      else:
        localStats['types'][fileType]['count'] += 1
        localStats['types'][fileType]['sizes'].append(fileSize)
        localStats['types'][fileType]['size'] += fileSize

      if (fileCat not in localStats['cats']):
        localStats['cats'][fileCat] = {'count': 1, 'size': fileSize, 'sizes': [fileSize]}
      else:
        localStats['cats'][fileCat]['count'] += 1
        localStats['cats'][fileCat]['sizes'].append(fileSize)
        localStats['cats'][fileCat]['size'] += fileSize

      localStats['count'] += 1
      localStats['size'] += fileSize
      localStats['sizes'].append(fileSize)

  return localStats

if (len(sys.argv) > 1):
  targetDir = sys.argv[1]
  targetPath = os.path.realpath(targetDir)
  targetName = targetPath.split(os.sep)[-1]
else:
  targetPath = os.getcwd()
  targetDir = targetPath.split(os.sep)[-1]
  targetName = targetDir

reportsPath = os.path.join(os.getcwd(), '_' + targetName + '_reports')
if (not os.path.isdir(reportsPath)):
  os.mkdir('_' + targetName + '_reports')

if (not os.path.isfile(os.path.join(reportsPath, '_cache.json'))):
  #cacheFile = open(os.path.join(reportsPath + '_cache.json', 'w'))
  print("No cache file found, beginning count from scratch.")
  data = {'count': 0, 'size': 0, 'dirs': {}, 'types': {}, 'cats': {}}
else:
  print("Restoring progress from cache file...")
  with open(os.path.join(reportsPath, '_cache.json'), 'r') as cacheFile:
    data = json.load(cacheFile)
    if ((data is None) or ('count' not in data)):
        data = {'count': 0, 'size': 0, 'dirs': {}, 'types': {}, 'cats': {}}

# Walk all non-folder objects in the base folder first
if ('root' not in data['dirs']):

  print("Counting files in root folder " + str(targetPath))
  data['dirs']['root'] = {'count': 0, 'size': 0, 'types': {}, 'cats': {}}

  for obj in os.listdir(targetPath):

    objPath = os.path.join(targetPath, obj)
    if (not os.path.isdir(objPath)):
      fileInfo = countFile(objPath)
      fileCat = fileInfo['fileCat']
      fileType = fileInfo['fileType']
      fileSize = fileInfo['fileSize']

      # Global counts for the entire tree
      if (fileType not in data['types']):
        data['types'][fileType] = {'count': 1, 'size': fileSize, 'sizes': [fileSize]}
      else:
        data['types'][fileType]['count'] += 1
        data['types'][fileType]['size'] += fileSize
        data['types'][fileType]['sizes'].append(fileSize)

      if (fileCat not in data['cats']):
        data['cats'][fileCat] = {'count': 1, 'size': fileSize, 'sizes': [fileSize]}
      else:
        data['cats'][fileCat]['count'] += 1
        data['cats'][fileCat]['size'] += fileSize
        data['cats'][fileCat]['sizes'].append(fileSize)

      data['count'] += 1
      data['size'] += fileSize

      # Counts for the root folder only
      if (fileType not in data['dirs']['root']['types']):
        data['dirs']['root']['types'][fileType] = {'count': 1, 'size': fileSize, 'sizes': [fileSize]}
      else:
        data['dirs']['root']['types'][fileType]['count'] += 1
        data['dirs']['root']['types'][fileType]['size'] += fileSize
        data['dirs']['root']['types'][fileType]['sizes'].append(fileSize)

      if (fileCat not in data['dirs']['root']['cats']):
        data['dirs']['root']['cats'][fileCat] = {'count': 1, 'size': fileSize, 'sizes': [fileSize]}
      else:
        data['dirs']['root']['cats'][fileCat]['count'] += 1
        data['dirs']['root']['cats'][fileCat]['size'] += fileSize
        data['dirs']['root']['cats'][fileCat]['sizes'].append(fileSize)

      data['dirs']['root']['count'] += 1
      data['dirs']['root']['size'] += fileSize

  with open(os.path.join(reportsPath, '_cache.json'), 'w') as cacheFile:
    json.dump(data, cacheFile)

  writeReports(data, reportsPath, targetName)

# Now count all of the subfolders
for obj in os.listdir(targetPath):

  # Make a separate report for each 
  objPath = os.path.join(targetPath, obj)

  if (not os.path.isdir(objPath)):
    continue

  thisPath = str(objPath)
  
  # If data for the folder is already in the cache file, don't re-crawl it
  # Note that this means the only way to refresh the count data is to
  # delete the cache JSON file (or delete the folder's entry in the cache JSON,
  # if you're feeling ambitious)
  if (thisPath in data['dirs']):
    print("File counts already in cache, skipping for " + str(targetPath))
    continue
  
  print("Counting all files (including subfdirs) in " + str(targetPath))

  data['dirs'][thisPath] = {'size': 0, 'count': 0, 'types': {}, 'cats': {}}

  print("Walking " + objPath)
  results = walkPath(objPath)
      
  # Global counts for the entire tree
  data['size'] += results['size'] 
  data['count'] += results['count']
      
  data['dirs'][thisPath]['count'] += results['count']
  data['dirs'][thisPath]['size'] += results['size']

  for fileType in results['types']:
    typeSize = results['types'][fileType]['size']
    typeCount = results['types'][fileType]['count']
    typeSizes = results['types'][fileType]['sizes']

    # Update global file type counts
    if (fileType not in data['types']):
      data['types'][fileType] = {'count': typeCount, 'size': typeSize, 'sizes': typeSizes}
    else:
      data['types'][fileType]['count'] += typeCount
      data['types'][fileType]['size'] += typeSize
      data['types'][fileType]['sizes'].extend(typeSizes)

    # Counts for this (top-level parent) folder only
    if (fileType not in data['dirs'][thisPath]['types']):
      data['dirs'][thisPath]['types'][fileType] = {'count': typeCount, 'size': typeSize, 'sizes': typeSizes}
    else:
      data['dirs'][thisPath]['types'][fileType]['count'] += typeCount
      data['dirs'][thisPath]['types'][fileType]['size'] += typeSize
      data['dirs'][thisPath]['types'][fileType]['sizes'].extend(typeSizes)

  for fileCat in results['cats']:
    catSize = results['cats'][fileCat]['size']
    catCount = results['cats'][fileCat]['count']
    catSizes = results['cats'][fileCat]['sizes']

    # Update global file category counts
    if (fileCat not in data['cats']):
      data['cats'][fileCat] = {'count': catCount, 'size': catSize, 'sizes': catSizes}
    else:
      data['cats'][fileCat]['count'] += catCount
      data['cats'][fileCat]['size'] += catSize
      data['cats'][fileCat]['sizes'].extend(catSizes)

    # Counts for this (top-level parent) folder only
    if (fileCat not in data['dirs'][thisPath]['cats']):
      data['dirs'][thisPath]['cats'][fileCat] = {'count': catCount, 'size': catSize, 'sizes': catSizes}
    else:
      data['dirs'][thisPath]['cats'][fileCat]['count'] += catCount
      data['dirs'][thisPath]['cats'][fileCat]['size'] += catSize
      data['dirs'][thisPath]['cats'][fileCat]['sizes'].extend(catSizes)

  with open(os.path.join(reportsPath, '_cache.json'), 'w') as cacheFile:
    json.dump(data, cacheFile)

  writeReports(data, reportsPath, targetName)
