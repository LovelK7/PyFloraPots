import os

class FileMngr():
    def checkFilePath(self, file_path):
        return os.path.exists(file_path)

    def openFileForReading(self, file_path):
        if not self.checkFilePath(file_path):
            return f'File {file_path} does not exist'
        try:
            file_reader = open(file_path,'r')
            return file_reader
        except Exception as ex:
            return f'An error occurred: {ex}'

    def readFromFilePathOpenClose(self, file_path):
        if not self.checkFilePath(file_path):
            return f'File {file_path} does not exist'
        try:
            with open(file_path,'r') as fileReader:
                return fileReader.read()
        except Exception as ex:
            return f'An error occurred while trying to read file: {ex}'

    def readLineWithFileReader(self, lineReader):
        try:
            line = lineReader.readline()
            if line.endswith('\n'):
                line = line.rstrip('\n')
            return line
        except Exception as ex:
            return f'An error occurred while trying to read a line: {ex}'

    def openFileForWriting(self, file_path):
        try:
            file_writer = open(file_path,'w')
            return file_writer
        except Exception as ex:
            return f'An error occurred: {ex}'

    def writeToFilePath(self, file_path, content):
        try:
            with open(file_path,'a') as fileWriter:
                fileWriter.write(content)
        except Exception as ex:
            return f'An error occurred while trying to write: {ex}'

    def writeLineWithFileWriter(self, lineWriter, lineContent):
        try:
            lineContent = lineContent + '\n'
            lineWriter.write(lineContent)
        except Exception as ex:
            return f'An error occurred while trying to write a line: {ex}'
    
    def deleteCSVFile(self, file_path):
        if not self.checkFilePath(file_path):
            return f'File {file_path} does not exist'
        try:
            os.remove(file_path)
        except Exception as ex:
            return f'An error occurred: {ex}'
