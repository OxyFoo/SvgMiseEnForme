import os

class Config:
    '''
    Configuration class.
    '''

    clearOnStart = True
    '''
    Clear the console on start.
    '''

    dirRaw = './raw'
    '''
    Directory containing the raw svg files.
    '''

    dirSvg = './svg'
    '''
    Directory containing the final svg files.
    '''

    DEBUG_LEVEL = 1
    '''
    Debug level.
    0: No debug
    1: Debug -> Errors / warnings
    2: Debug + verbose
    '''

    identSpace = '    '
    '''
    Space to use for identation. (4 spaces or so)
    Set to None to disable identation and show all the tags on one line.
    '''

    convertToRN = True
    '''
    Convert parsed svg content to react-native format.
    '''

    def CheckFolders():
        if not os.path.isdir(Config.dirRaw):   os.mkdir(Config.dirRaw)
        if not os.listdir(Config.dirRaw):      exit('Directory "' + Config.dirRaw + '" is empty.\nAborted...')
        if not os.path.isdir(Config.dirSvg):   os.mkdir(Config.dirSvg)
        if os.listdir(Config.dirSvg):
            response = input('Directory "' + Config.dirSvg + '" is not empty, remove all files ? (y/N) : ')
            if response.lower() != 'y': exit('Aborted...')
            for file in os.listdir(Config.dirSvg):
                os.remove(Config.dirSvg + '/' + file)