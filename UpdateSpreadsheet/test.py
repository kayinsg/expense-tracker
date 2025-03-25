import unittest
from FileSystem import MonthDirectory, DirectoryCreator, SpreadsheetFileCreator, FileCreator
from WorkbookPopulator import WeekNormalizer
from SpreadsheetWriter import SpreadsheetDataPopulator
import pendulum
import openpyxl
from pandas import DataFrame
from colour_runner.runner import ColourTextTestRunner


class SpreadsheetWorkbookPopulationTest(unittest.TestCase):

        @staticmethod
        def firstDayOfWeek(weekDays):
            return weekDays[0].format('dddd')

        @staticmethod
        def lastDayOfWeek(weekDays):
            return weekDays[-1].format('dddd')

        def testPreviousMonth(self):
            dateWithPreviousMonthWeekdays = '2025-03-01'
            weekDaysInvolvingThePreviousMonth = ['Feb.23.2025', 'Feb.24.2025', 'Feb.25.2025', 'Feb.26.2025', 'Feb.27.2025', 'Feb.28.2025', 'Mar.01.2025']

            weekDaysStartingFromSunday = WeekNormalizer(dateWithPreviousMonthWeekdays).getWeekdays()

            self.assertEqual(weekDaysStartingFromSunday, weekDaysInvolvingThePreviousMonth)

        def testSameMonth(self):
            dateWithSameMonthWeekdays = '2025-03-27'
            weekDaysInvolvingOnlyTheSameMonth = ['Mar.23.2025', 'Mar.24.2025', 'Mar.25.2025', 'Mar.26.2025', 'Mar.27.2025', 'Mar.28.2025', 'Mar.29.2025']

            weekDaysStartingFromSunday = WeekNormalizer(dateWithSameMonthWeekdays).getWeekdays()

            self.assertEqual(weekDaysStartingFromSunday, weekDaysInvolvingOnlyTheSameMonth)

        def testSucceedingMonth(self):
            dateWithSuceedingMonthWeekdays = '2025-04-05'
            weekDaysInvolvingTheSucceedingMonth = ['Mar.30.2025', 'Mar.31.2025', 'Apr.01.2025', 'Apr.02.2025', 'Apr.03.2025', 'Apr.04.2025', 'Apr.05.2025']

            weekDaysStartingFromSunday = WeekNormalizer(dateWithSuceedingMonthWeekdays).getWeekdays()

            self.assertEqual(weekDaysStartingFromSunday,weekDaysInvolvingTheSucceedingMonth)


class SpreadsheetFileSystemTest(unittest.TestCase):

    currentDate = '2025-03-20'

    def testShouldCreateFolderRepresentingMonthWhenDateIsGiven(self):

        class FakeDirectoryCreator(DirectoryCreator):
            def __init__(self, parentDirectory):
                self.parentDirectory = parentDirectory

            def makeDirectoryOnFileSystem(self, monthName):
                return monthName

        parentDirectory = ""
        directoryCreator = FakeDirectoryCreator(parentDirectory)
        monthDirectory = MonthDirectory(directoryCreator, self.currentDate)

        fullPath = monthDirectory.create()

        self.assertEqual(fullPath, "March/")


    def testShouldCreateSpreadsheetFileRepresentingTheWeekNumberInMonthGivenCurrentDate(self):

        class FakeSpreadsheetFileCreator(SpreadsheetFileCreator):
            def __init__(self, fileCreator, currentDate):
                self.fileCreator = fileCreator
                self.currentDate = currentDate

            def getWorkbook(self, spreadsheetFilePath):
                return spreadsheetFilePath

        class FakeFileCreator(FileCreator):
            def __init__(self, parentDirectory):
                self.parentDirectory = parentDirectory

            def createSpreadsheetFile(self, filePath):
                return filePath

        def get_week_in_month(iso_date: str) -> int:
            date = pendulum.parse(iso_date)
            return date.week_of_month

        parentDirectory = ""
        fileCreator = FakeFileCreator(parentDirectory)
        weekWithinMonth = get_week_in_month(self.currentDate)

        spreadsheet = FakeSpreadsheetFileCreator(fileCreator, self.currentDate).create()

        self.assertEqual(spreadsheet['FilePath'], f"{parentDirectory}Week {weekWithinMonth}.xlsx")


class SpreadsheetWriterTest(unittest.TestCase):

    def testShouldPlaceExtractedDataInCorrectDateWorksheetWhenSpreadsheetIsAlreadyPopulatedWithDateWorksheets(self) -> None:

        def dataInSpreadsheet(spreadsheet):
            dummyList = []
            for row in spreadsheet.iter_rows(min_row=1, max_col=spreadsheet.max_column, max_row=spreadsheet.max_row, values_only=True):
                rowCells = list()
                for cell in row:
                    rowCells.append(cell)
                dummyList.append(rowCells)
            return dummyList

        class FakeWorkBook:
            def __init__(self, currentDate):
                self.currentDate = currentDate

            def workbookWithWeekDays(self) -> openpyxl.Workbook:
                workbook = openpyxl.Workbook()
                currentDate = pendulum.parse(self.currentDate)
                startOfWeek = currentDate.start_of('week')
                daysWithinWeek = [startOfWeek.add(days=i).format("YYYY-MM-DD") for i in range(7)]
                defaultSheet: openpyxl.worksheet.worksheet.Worksheet = workbook.active
                workbook.remove(defaultSheet)
                for day in daysWithinWeek:
                    workbook.create_sheet(day)
                return workbook

        data = {'Items': ['Candy', 'Orange', 'Chips'], 'Gross Price': [ 1, 1.50, 1.99 ], 'Final Price': [ 1.13, 1.76, 2.13 ], 'Taxes Paid': [ 0.13, 0.25, 0.35 ]}
        dataFrame: DataFrame = DataFrame(data)
        dataList = [['Items', 'Gross Price', 'Final Price', 'Taxes Paid'], ['Candy', 1.0, 1.13, 0.13], ['Orange', 1.5, 1.76, 0.25], ['Chips', 1.99, 2.13, 0.35]]
        currentDate = '2025-03-20'
        workbook: openpyxl.Workbook = FakeWorkBook(currentDate).workbookWithWeekDays()

        spreadsheetWithPopulatedCurrentDate = SpreadsheetDataPopulator(currentDate, dataFrame).populate(workbook)

        dateWorksheet = spreadsheetWithPopulatedCurrentDate[currentDate]
        spreadsheetData = dataInSpreadsheet(dateWorksheet)

        self.assertEqual(spreadsheetData, dataList)


unittest.main(testRunner=ColourTextTestRunner())
