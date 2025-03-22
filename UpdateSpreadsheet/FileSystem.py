from abc import ABC, abstractmethod
import pendulum
import os


class FileSystem:
    def __init__(self, spreadsheetParentDirectory, currentDate):
        self.spreadsheetParentDirectory = spreadsheetParentDirectory
        self.currentDate = currentDate

    def createSpreadsheetMonthFolder(self):
        directoryCreator = DirectoryCreator(self.spreadsheetParentDirectory)
        currentDate = pendulum.now().format('YYYY-MM-DD')
        createdMonthDirectory = MonthDirectory(directoryCreator, currentDate).create()
        return createdMonthDirectory

class FileSystemInterface(ABC):

    @staticmethod
    def standardizePath(path):
        if not path.endswith("/"):
            path += "/"
        return path

    @abstractmethod
    def create(self):
        pass

class MonthDirectory(FileSystemInterface):
    def __init__(self, folderCreator, currentDate):
        self.folderCreator = folderCreator
        self.currentDate = currentDate

    def create(self):
        monthOfCurrentDate = self.getMonthOfCurrentDate(self.currentDate)
        return self.makeFolderRepresentingTheMonthOfSpreadsheet(monthOfCurrentDate)

    def getMonthOfCurrentDate(self, currentDate):
        return pendulum.parse(currentDate).format('MMMM')

    def makeFolderRepresentingTheMonthOfSpreadsheet(self, monthName):
        return self.folderCreator.createDirectory(monthName)


class DirectoryCreator:
    def __init__(self, parentDirectory):
        self.parentDirectory = parentDirectory

    def createDirectory(self, monthName):
        fullFilePath = self.createFullPathForDirectory(monthName)
        self.makeDirectoryOnFileSystem(fullFilePath)
        return fullFilePath 

    def createFullPathForDirectory(self, monthName):
        return f"{self.parentDirectory}{monthName}"

    def makeDirectoryOnFileSystem(self, monthName):
        try:
            os.makedirs(monthName)
            print(f"Folder '{monthName}' created successfully.")
        except FileExistsError:
            print(f"Folder '{monthName}' already exists.")
        except Exception as e:
            print(f"An error occurred while creating the folder: {e}")
