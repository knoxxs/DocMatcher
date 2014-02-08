"""
Preprocess the RISOT Bengali Corpus. It includes:

- Giving the same name to internal directory structure and files.
- Making the two directories consistent (removing no-common files).

If you are running this file directly then you need to pass the path of corpus
else you need to set the path of the corpus in the global variable named
``corpusPath`` manualy.

Then you first need to call the function :func:``findOcredOrigDirectory`` (or
also you can set the path for ocred and original directorly in the variables
``ocredCorpusPath`` & ``origCorpusPath`` respectively). This is a pre-requisite to
all the other functions.
"""

# from docMatcher.risotCorpus import readDirectory as rd #TODO
import readDirectory as rd

import sys
import os
import re

def _renameYearDirectories(path):
	"""
	Renames subDirectories of the path to inlclude only the year as the name
	(removes any extra text from the name). 

	:arg path: path of the directory
	"""
	pattern = re.compile(r'\d+')

	for dir_ in os.walk(path).next()[1]:
		os.rename(os.path.join(path, dir_),
					os.path.join(path, pattern.findall(dir_)[0]))

def _renameFiles(fileGenerator):
	"""
	Renames the files from *fileName.blabla* to *fileName.txt*.

	:arg fileGenerator: a generator object which will generate all the file
	names. 
	"""
	separator = os.sep
	for file_ in fileGenerator():
		path, fileName = file_.rsplit(separator, 1)
		os.rename(file_, os.path.join(path, fileName.split('.')[0] + '.txt'))

def renameOcred():
	"""
	Renames ocred directory. Rename all the year directories to include only
	year names (no extra string) and all the files from *fileName.blabla* to
	*fileName.txt*.
	"""
	_renameYearDirectories(rd.ocredCorpusPath)

def renameOriginal():
	"""
	Renames original directory. Rename all the year directories to include only
	year names (no extra string) and all the files from *fileName.blabla* to
	*fileName.txt*.
	"""
	_renameYearDirectories(rd.origCorpusPath)

	_renameFiles(rd.readOrigDirectory)

def removeUnCommonFiles():
	"""
	Removes all the un-common files between the two directories: ocred and
	original. *Before calling this functoin `rename{Ocred,Original}` must be
	called*.
	"""
	for year in os.walk(rd.origCorpusPath).next()[1]:
		ocredYearPath = os.path.join(rd.ocredCorpusPath, year)
		origYearPath = os.path.join(rd.origCorpusPath, year)

		for dir_ in os.walk(os.path.join(rd.origCorpusPath, year)).next()[1]:
			origFiles = os.listdir(os.path.join(origYearPath, dir_))
			ocredFiles = os.listdir(os.path.join(ocredYearPath, dir_))

			if not origFiles == ocredFiles:
				ocredDirPath = os.path.join(ocredYearPath, dir_)
				origDirPath = os.path.join(origYearPath, dir_)

				for file_ in set(origFiles) - set(ocredFiles):
					print 'Removing', os.path.join(origDirPath, file_) 
					os.remove(os.path.join(origDirPath, file_))

				for file_ in set(ocredFiles) - set(origFiles):
					print 'Removing', os.path.join(ocredDirPath, file_)
					os.remove(os.path.join(ocredDirPath, file_))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        firstArg = sys.argv[1]
        if firstArg == '-h':
            print 'You have to pass the path to corpus like python \
            preProcess.py <corpus path>'
        elif os.path.isdir(firstArg):
            rd.corpusPath = firstArg
            rd.findOcredOrigDirectory(rd.corpusPath)
        else:
            print "ERROR: Directory(%s) don't exist" % firstArg
        # renameOriginal()
        # renameOcred()
        # removeUnCommonFiles()
    else:
        print 'Use python preProcess.py -h for help.'