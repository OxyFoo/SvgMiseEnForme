import os, sys, signal
from lib.config import Config

def checkPythonVersion():
    '''
    Check the Python version.
    '''
    if sys.version_info[0] < 3:
        print("This program requires Python 3.x")
        sys.exit(1)

def defineHandler():
    signal.signal(signal.SIGINT, handler)

def handler(signum, frame):
    print('\nAborted...')
    exit(1)

def Debug(level, message):
    '''
    Print a debug message.

    Parameters
    ----------
    level : int
        The debug level.
        0: No debug
        1: Debug -> Errors / warnings
        2: Debug + verbose
    message : str
        The message to print.
    '''
    if Config.DEBUG_LEVEL >= level:
        if level == 1: print('\033[91m', end='')
        print(message)
        if level == 1: print('\033[0m', end='')

def printFullLine(char = '=', length = None):
    '''
    Print a line of characters of a given length.

    Parameters
    ----------
    char : str
        The character to use.
    length : int
        The length of the line.
        None means use the current terminal width.
    '''
    if length is None:
        length = os.get_terminal_size().columns
    print(char * length)

def getStringBetween(text, firstWord, lastWord, keepAroundWords = True):
    '''
    Get the string between two words.

    Parameters
    ----------
    text : str
        Le texte dans lequel on cherche
    firstWord : str
        Le mot qui débute la chaine
    lastWord : str
        Le mot qui termine la chaine

    Returns
    -------
    dict|None
        pos: position of the first word in the text
        length: length of the string between the first and last word
        content: the string between the first and last word

        None if the words are not found.
    '''

    firstPos = text.find(firstWord)
    if firstPos == -1:
        return None

    lastPos = firstPos + text[firstPos+len(firstWord):].find(lastWord)
    if lastPos == -1:
        return None

    output = {}
    if keepAroundWords:
        output['pos'] = firstPos
        output['length'] = lastPos - firstPos + len(firstWord) + len(lastWord)
        output['content'] = text[firstPos:lastPos + len(firstWord) + len(lastWord)]
    else:
        output['pos'] = firstPos + len(firstWord)
        output['length'] = lastPos - firstPos
        output['content'] = text[firstPos + len(firstWord):lastPos + len(firstWord)]
    return output

def GetFileContent(filePath, cleanContent = True):
    '''
    Get the content of a file.

    Parameters
    ----------
    filePath : str
        The path of the file.

    Returns
    -------
    str
        The content of the file.
    '''

    file = open(filePath, 'rb')
    fileContent = file.read()
    fileContent = fileContent.decode('utf8')
    file.close()

    if cleanContent:
        # Remove useless lines
        removeChars = [ '\n', '\r', '\t' ]
        for char in removeChars:
            fileContent = fileContent.replace(char, '')

    return fileContent

def SaveFileContent(filePath, fileContent):
    '''
    Save the content of a file.

    Parameters
    ----------
    filePath : str
        The path of the file.
    fileContent : str
        The content of the file.
    '''

    try:
        file = open(filePath, 'wb')
        file.write(fileContent.encode('utf8'))
        file.close()
        Debug(0, 'New SVG saved')
    except Exception as e:
        Debug(0, 'Error: SVG not saved')
        Debug(1, e)