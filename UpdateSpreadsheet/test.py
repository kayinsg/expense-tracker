import unittest
from FileSystem import MonthDirectory, DirectoryCreator

class SpreadsheetTests(unittest.TestCase):

    currentDate = '2025-03-20'

    def testShouldCreateFolderRepresentingMonthWhenDateIsGiven(self):
        class FakeDirectoryCreator(DirectoryCreator):
            def __init__(self, parentDirectory):
                self.parentDirectory = parentDirectory

            def makeDirectoryOnFileSystem(self, monthName):
                return monthName

        parentDirectory = ""

        monthFolderPath = FileSystem(parentDirectory, self.currentDate).createSpreadsheetMonthFolder()

        self.assertEqual(monthFolderPath, "March/")

unittest.main()
