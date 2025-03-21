import unittest
from FileSystem import MonthDirectory

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

unittest.main()
