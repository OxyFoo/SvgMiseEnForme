import os
from lib.config import Config

def Debug(level, message):
    '''
    Print a debug message.

    Parameters
    ----------
    level : int
        The debug level.
    message : str
        The message to print.
    '''
    if Config.DEBUG_LEVEL >= level:
        print(message)

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
