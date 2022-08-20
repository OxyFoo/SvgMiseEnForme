from lib.config import Config

class Debug:
    '''
    Print a debug message.
    '''

    def Info(message: str, end: str = '\n'):
        '''
        Print an info message, will be always printed.
        '''
        print('[info] ' + message, end=end)

    def Warn(message: str):
        '''
        Print a warning message, will be printed if the debug level is >= 1 (show warn & errors).
        '''
        if Config.DEBUG_LEVEL >= 1:
            print('\033[93m[warn] ' + message + '\033[0m')

    def Error(message: str):
        '''
        Print an error message, will be printed if the debug level is >= 1 (show warn & errors).
        '''
        if Config.DEBUG_LEVEL >= 1:
            print('\033[91m[error] ' + message + '\033[0m')

    def Log(message: str):
        '''
        Print a log message, will be printed if the debug level is >= 2 (show verbose).
        '''
        if Config.DEBUG_LEVEL >= 2:
            print('[log] ' + message)
