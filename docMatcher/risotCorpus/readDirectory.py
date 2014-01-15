"""
Read the RISOT corpus to provide the list of directories,if any, and files in
it. It requires the presence of two directories, one with 'original' in its
name and other with 'ocred' in its name, to be present in the corpus directory
at the top level.

If you are running this file directly then you need to pass the path of corpus
else you need to set the path of the corpus in the global variable named
``corpusPath``.

Then you first need to call the function :func:`findOcredOrigDirectory`. This
is a pre-requisite to all the other functions.
"""
import sys
import os

corpusPath, origCorpusPath, ocredCorpusPath = None, None, None

def findOcredOrigDirectory(corpusPath):
    """
    Find the ocred and original directory name inside the corpus directory to
    set the global variables ``origCorpusPath`` & ``ocredCorpusPath``
    accordingly.

    :arg corpusPath: path of the corpus
    """
    global origCorpusPath, ocredCorpusPath

    for content in os.listdir(firstArg):
        if os.path.isdir(content):
            if content.find('original') >= 0:
                origCorpusPath = firstArg + '/' + content
            elif content.find('ocred') >= 0:
                ocredCorpusPath = firstArg + '/' + content
    if not (origCorpusPath and ocredCorpusPath):
        print 'ERROR: Following two directories are not in the\
            directory(%s):' % firstArg
        print "One directory with the word 'original' in its name and\
            other with the word 'ocred' in it."

def _readDirectory(dirPath):
    """
    Read a directory to yield all the files *recursively* in this directory.

    :arg dirPath: path of the directory to read

    :return: its a gnerator of filenames relative to the corpus path
    """
    for (path, dirnames, filenames) in os.walk(dirPath):
        for file_ in filenames:
            yield path + '/' + f

def readOcredDirectory():
    """
    Read a the ocred directory to yield all the files *recursively*.

    :return: its a gnerator of filenames relative to the corpus path
    """
    _readDirectory(ocredCorpusPath)

def readOrigDirectory():
    """
    Read a the original directory to yield all the files *recursively*.

    :return: its a gnerator of filenames relative to the corpus path
    """
    _readDirectory(origCorpusPath)

def readBothDirectory():
    """
    Read both the ocred and original directory simultaneously to yield both the
    versions *(original and ocred)* of a file *recursively*.

    *This functions need both the directory to contain the same number of
    files with the same names. By default, both requirements are false for
    the RISOT bengali dataset. To meet these requirements use the module
    :mod:`clean`.* TODO: Check for clean linking.

    :return: its a gnerator of filenames relative to the corpus path in the
        form ``(origFile, ocredFile)``
    """
    for origFile, ocredFile in izip(readOrigDirectory(), readOcredDirectory()):
        yield (origFile, ocredFile)
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        firstArg = sys.argv[1]
        if firstArg == '-h':
            print 'You have to pass the path to corpus like python read.py \
            <corpus path>'
        elif os.path.isdir(firstArg):
            corpusPath = firstArg
        else:
            print "ERROR: Directory(%s) don't exist" % firstArg

    else:
        print 'Use python read.py -h for help.'