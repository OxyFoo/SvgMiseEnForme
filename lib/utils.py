import os
import sys
import signal

from lib.config import Config
from lib.debug import Debug

def Init():
    '''
    Check the Python version.
    '''
    if sys.version_info[0] < 3:
        print("This program requires Python 3.x")
        sys.exit(1)

    if Config.clearOnStart:
        os.system('cls' if os.name == 'nt' else 'clear')

def DefineHandler():
    signal.signal(signal.SIGINT, handler)

def handler(signum, frame):
    print('\nAborted...')
    exit(1)

def PrintFullLine(char = '=', length = None):
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

def GetFileContent(filename: str, cleanContent: bool = True):
    '''
    Get the content of a file.

    Parameters
    ----------
    filename : str
        The name of the file.

    Returns
    -------
    str
        The content of the file or None if failed.
    '''

    # Check if file is a valid svg file
    filepath = os.path.join(Config.dirRaw, filename)
    if not filepath.endswith(".svg"): return None
    if not os.path.isfile(filepath): return None
    Debug.Info('Processing file "' + filename + '"')

    # Get file content
    try:
        file = open(filepath, 'rb')
        fileContent = file.read()
        fileContent = fileContent.decode('utf8')
        file.close()
    except Exception as e:
        Debug.Error('SVG not read')
        Debug.Log(e)
        return None

    if cleanContent:
        # Remove useless lines
        removeChars = [ '\n', '\r', '\t' ]
        for char in removeChars:
            fileContent = fileContent.replace(char, '')

        # Remove comments
        commentsInfo = ''
        while commentsInfo != None:
            commentsInfo = getStringBetween(fileContent, '<!--', '-->')
            if commentsInfo != None:
                fileContent = fileContent.replace(commentsInfo['content'], '', 1)

    if fileContent.startswith('<?'):
        # Remove XML declaration
        fileContent = fileContent[fileContent.find('>')+1:]

    return fileContent

def SaveFileContent(filename: str, fileContent: str):
    '''
    Save the content of a file.

    Parameters
    ----------
    filename : str
        The path of the file.
    fileContent : str
        The content of the file.
    '''

    filename = '.'.join(filename.split('.')[:-1])
    filename += '.js' if Config.convertToRN else '.svg'
    filepath = os.path.join(Config.dirSvg, filename)
    try:
        file = open(filepath, 'wb')
        file.write(fileContent.encode('utf8'))
        file.close()
        Debug.Info('New SVG saved')
    except Exception as e:
        Debug.Error('SVG not saved')
        Debug.Log(e)