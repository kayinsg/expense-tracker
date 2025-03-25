import unittest
from FileSystem import MonthDirectory, DirectoryCreator, SpreadsheetFileCreator, FileCreator
from WorkbookPopulator import WeekNormalizer
import pendulum
from colour_runner.runner import ColourTextTestRunner


class SpreadsheetWorkbookPopulationTest(unittest.TestCase):
        @staticmethod
        def convertDateTimeObjectsToString(dateTimeObjects):
            convert = lambda dateTime: dateTime.format('MMM.DD.YYYY')
            return list(map(convert, dateTimeObjects))

        @staticmethod
        def firstDayOfWeek(weekDays):
            return weekDays[0].format('dddd')

        @staticmethod
        def lastDayOfWeek(weekDays):
            return weekDays[-1].format('dddd')

        class FakeWeekNormalizer(WeekNormalizer): 
            def convertDateTimeObjectsToString(self, dateTimeObjects):
                return dateTimeObjects

        def testPreviousMonth(self):
            dateWithPreviousMonthWeekdays = '2025-03-01'
            weekDaysInvolvingThePreviousMonth = ['Feb.23.2025', 'Feb.24.2025', 'Feb.25.2025', 'Feb.26.2025', 'Feb.27.2025', 'Feb.28.2025', 'Mar.01.2025']

            weekDaysStartingFromSunday = self.FakeWeekNormalizer(dateWithPreviousMonthWeekdays).getWeekdays()

            self.assertEqual(self.firstDayOfWeek(weekDaysStartingFromSunday), "Sunday")
            self.assertEqual(self.lastDayOfWeek(weekDaysStartingFromSunday), "Saturday")
            self.assertEqual(self.convertDateTimeObjectsToString(weekDaysStartingFromSunday), weekDaysInvolvingThePreviousMonth)

        def testSameMonth(self):
            dateWithSameMonthWeekdays = '2025-03-27'
            weekDaysInvolvingOnlyTheSameMonth = ['Mar.23.2025', 'Mar.24.2025', 'Mar.25.2025', 'Mar.26.2025', 'Mar.27.2025', 'Mar.28.2025', 'Mar.29.2025']

            weekDaysStartingFromSunday = self.FakeWeekNormalizer(dateWithSameMonthWeekdays).getWeekdays()

            self.assertEqual(self.firstDayOfWeek(weekDaysStartingFromSunday), "Sunday")
            self.assertEqual(self.lastDayOfWeek(weekDaysStartingFromSunday), "Saturday")
            self.assertEqual(self.convertDateTimeObjectsToString(weekDaysStartingFromSunday), weekDaysInvolvingOnlyTheSameMonth)

        def testSucceedingMonth(self):
            dateWithSuceedingMonthWeekdays = '2025-04-05'
            weekDaysInvolvingTheSucceedingMonth = ['Mar.30.2025', 'Mar.31.2025', 'Apr.01.2025', 'Apr.02.2025', 'Apr.03.2025', 'Apr.04.2025', 'Apr.05.2025']

            weekDaysStartingFromSunday = self.FakeWeekNormalizer(dateWithSuceedingMonthWeekdays).getWeekdays()

            self.assertEqual(self.firstDayOfWeek(weekDaysStartingFromSunday), "Sunday")
            self.assertEqual(self.lastDayOfWeek(weekDaysStartingFromSunday), "Saturday")
            self.assertEqual(self.convertDateTimeObjectsToString(weekDaysStartingFromSunday),weekDaysInvolvingTheSucceedingMonth)

class SpreadsheetTests(unittest.TestCase):

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


unittest.main(testRunner=ColourTextTestRunner())
