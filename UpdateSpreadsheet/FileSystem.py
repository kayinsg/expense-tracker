from abc import ABC, abstractmethod
import pendulum
import os
import openpyxl


class FileSystem:
    def __init__(self, spreadsheetParentDirectory):
        self.spreadsheetParentDirectory = spreadsheetParentDirectory

    @staticmethod
    def getCurrentDate():
        return pendulum.now().format('YYYY-MM-DD')

    def setUpSpreadsheet(self):
        monthFolder = self.createSpreadsheetMonthFolder()
        workbook = self.createSpreadsheetFile(monthFolder)
        worksheet = self.populateWorkbookWithWorksheetDates(workbook['Workbook'])
        workbook['Workbook'].save(workbook['FilePath'])
        return worksheet

    def createSpreadsheetMonthFolder(self):
        directoryCreator = DirectoryCreator(self.spreadsheetParentDirectory)
        currentDate = self.getCurrentDate()
        createdMonthDirectory = MonthDirectory(directoryCreator, currentDate).create()
        return createdMonthDirectory

    def createSpreadsheetFile(self, parentDirectory):
        currentDate = self.getCurrentDate()
        fileCreator = FileCreator(parentDirectory)
        return SpreadsheetFileCreator(fileCreator, currentDate).create()

    def populateWorkbookWithWorksheetDates(self, workbook): 
        return SpreadsheetPopulator(self.getCurrentDate()).populate(workbook)


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
        spreadsheetMonthDirectory = self.folderCreator.createDirectory(monthName)
        return self.standardizePath(spreadsheetMonthDirectory)


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


class SpreadsheetFileCreator(FileSystemInterface):
    def __init__(self, fileCreator, currentDate):
        self.fileCreator = fileCreator
        self.currentDate = currentDate

    def create(self):
        weekWithinMonth = self.getWeekInMonth(self.currentDate)
        spreadsheetFileName = self.getSpreadsheetFileName(weekWithinMonth)
        spreadsheetFile =  self.createSpreadsheetOnFileSystem(spreadsheetFileName)
        workbook = self.getWorkbook(spreadsheetFile)
        return {'FilePath': spreadsheetFile, 'Workbook': workbook}

    def getWeekInMonth(self, isoDate):
        date = pendulum.parse(isoDate)
        return date.week_of_month

    def getSpreadsheetFileName(self, weekWithinMonth):
        return f'Week {weekWithinMonth}'

    def createSpreadsheetOnFileSystem(self, spreadsheetFileName):
        return self.fileCreator.createFile(spreadsheetFileName)

    def getWorkbook(self, spreadsheetFilePath):
        return openpyxl.load_workbook(spreadsheetFilePath)


class FileCreator:
    def __init__(self, parentDirectory):
        self.parentDirectory = parentDirectory

    def createFile(self, fileName):
       completeFileName = self.completeFileName(fileName) 
       self.createSpreadsheetFile(completeFileName)
       return completeFileName

    def completeFileName(self, fileName):
        return f"{self.parentDirectory}{fileName}.xlsx"

    def createSpreadsheetFile(self, completeFileName):
        workbook = openpyxl.Workbook()
        workbook.save(completeFileName)


class SpreadsheetPopulator:
    def __init__(self, currentDate):
        self.currentDate = currentDate

    def populate(self, workbook):
        daysWithinWeek = self.getDaysWithinTheWeekOfCurrentDate(self.currentDate)
        return self.insertDateWorksheetsInWorkbook(workbook, daysWithinWeek)

    def getDaysWithinTheWeekOfCurrentDate(self, currentDate):
        return WeekNormalizer(currentDate).getWeekdays()

    def insertDateWorksheetsInWorkbook(self, workbook, daysWithinWeek):
        return DateWorksheetInserter(workbook).insert(daysWithinWeek)

    def insertDateWorksheetsInWorkbook(self, workbook, daysWithinWeek):
        for day in daysWithinWeek:
            workbook.create_sheet(day)
        return workbook

class DefaultWorksheetEraser:
    def __init__(self, workbook):
        self.workbook = workbook

    def getCleanWorkbook(self):
        defaultWorksheet = self.getDefaultWorksheet(self.workbook)
        self.removeDefaultWorksheet(defaultWorksheet)
        return self.workbook

    def getDefaultWorksheet(self, workbook):
        defaultWorksheet = workbook.active
        return defaultWorksheet

    def removeDefaultWorksheet(self, defaultWorksheet):
        self.workbook.remove(defaultWorksheet)


class WeekNormalizer:
    def __init__(self, currentDate):
        self.currentDate = currentDate

    def getWeekdays(self):
        currentDate = self.encodeCurrentDate(self.currentDate)
        startOfWeek = self.standardizeWeekToSunday(currentDate)
        return self.convertDateTimeObjectsToString(self.getListOfDatesForTheWeek(startOfWeek))

    def encodeCurrentDate(self, currentDate):
        return pendulum.parse(currentDate)

    def standardizeWeekToSunday(self, currentDate):
        dayOfWeek = currentDate.day_of_week
        if dayOfWeek == 6:
            startOfWeek = currentDate
        else:
            startOfWeek = currentDate.subtract(days=dayOfWeek + 1)
        return startOfWeek

    def getListOfDatesForTheWeek(self, startOfWeek):
        getDates = lambda dayNumber: startOfWeek.add(days=dayNumber)
        return list(map(getDates, range(7)))

    def convertDateTimeObjectsToString(self, dateTimeObjects):
        convert = lambda dateTime: dateTime.format('MMM.DD.YYYY')
        return list(map(convert, dateTimeObjects))
