#------------------------------------------------#
# Created by frogen10
# GitHub: https://github.com/frogen10
#------------------------------------------------#
from datetime import datetime


class Logger:
    def __init__(self) -> None:
        self.filename = 'logs.txt'

    def __del__(self) -> None:
        msg = "Program closed\n"
        self.WriteToFile(msg)

    def LogError(self, className: str, message:str) ->None:
        '''
        Log same error
        '''
        msg = "Class: " + className + ' ex: ' + message
        self.WriteToFile(msg)
    
    def LogReadDataError(self, className: str, message:str) ->None:
        '''
        Log read data error
        '''
        msg = "Class: " + className+ " Error to read data: " + message
        self.WriteToFile(msg)

    def LogMessage(self, className: str, message: str) -> None:
        '''
        Log informations
        '''
        msg = "Class: " + className + ' msg: ' + message
        self.WriteToFile(msg)

    def WriteToFile(self, msg):
        time = datetime.now()
        file = open(self.filename, 'a', encoding='utf-8')
        file.write(str(time) + ': ' + msg + '\n')
        file.close()