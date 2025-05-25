import unittest
from Cost import Cost, CostSummary
from TextFile import TextFile, TextFileIdentifier
from colour_runner.runner import ColourTextTestRunner


class NewlineFileDataExtractorTests(unittest.TestCase):

    class FakeNewlineTextFile(TextFile):
        def __init__(self,filePath):
            self.filePath = filePath

        def getDataFromFile(self):
            return 'A Shoes From New York\n40\nMug\n2\nSweater\n40'

    def testShouldIdentifyFlatTextFileWithNewlines(self):
        # GIVEN the following preconditions corresponding to the system under test:
        filePath = None
        textFile = self.FakeNewlineTextFile(filePath).getDataFromFile()
        textFileModule = TextFileIdentifier(textFile)
        expectedExtractedData = [['A Shoes From New York', '40'], ['Mug', '2'], ['Sweater', '40']]
        # WHEN the following module is executed:
        fileType = textFileModule.getFileType()
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(fileType, 'newline')

    def testShouldExtractTextFromFlatTextFileWithNewlines(self):
        # GIVEN the following preconditions corresponding to the system under test:
        textFile = "A Shoes From New York\n40\nMug\n2\nSweater\n40"
        textFileModule = self.FakeNewlineTextFile(textFile)
        expectedExtractedData = [['A Shoes From New York', '40'], ['Mug', '2'], ['Sweater', '40']]
        # WHEN the following module is executed:
        extractedData = textFileModule.extractData()
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(extractedData, expectedExtractedData)


class CSVFileDataExtractorTests(unittest.TestCase):

    class FakeCSVTextFile(TextFile):
        def __init__(self,filePath):
            self.filePath = filePath

        def getDataFromFile(self):
            return 'Laptop, 400, Desk, 220, Headphones, 120'

    def setUp(self):
        self.maxDiff = None

    def testShouldIdentifyCSVFile(self):
        # GIVEN the following preconditions corresponding to the system under test:
        textFile = 'Laptop, 400, Desk, 220, Headphones, 120'
        textFileModule = TextFileIdentifier(textFile)
        # WHEN the following module is executed:
        fileType = textFileModule.getFileType()
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(fileType, 'csv')

    def testShouldExtractTextFromCSVFlatTextFile(self):
        # GIVEN the following preconditions corresponding to the system under test:
        textFile = "Laptop, 400, Desk, 220, Headphones, 120"
        expectedExtractedData = [['Laptop', '400'], ['Desk', '220'], ['Headphones', '120']]
        textFileModule = self.FakeCSVTextFile(textFile)
        # WHEN the following module is executed:
        extractedData = textFileModule.extractData()
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(extractedData, expectedExtractedData)


class CostTableTests(unittest.TestCase):

    def testShouldCreateRawPriceTable(self):
        # GIVEN the following preconditions corresponding to the system under test:
        items = [['Boots', '180',], ['Coat', '220'], ['Shirt', '25']]
        cost = Cost(items)
        expectedPriceTable = [
            ['Item', 'Gross Price', 'Price After Tax', 'Taxes Paid'],
            ['Boots', 180, 203.39999999999998, 23.399999999999977],
            ['Coat', 220, 248.59999999999997, 28.599999999999966],
            ['Shirt', 25, 28.249999999999996, 3.2499999999999964],
        ]
        # WHEN the following module is executed:
        priceTable = cost.createPriceTable('raw')
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(expectedPriceTable, priceTable)

    def testShouldCreateBeautifiedPriceTable(self):
        # GIVEN the following preconditions corresponding to the system under test:
        items = [['Boots', '180',], ['Coat', '220'], ['Shirt', '25']]
        cost = Cost(items)
        expectedResult = [
            ['Item', 'Gross Price', 'Price After Tax', 'Taxes Paid'],
            ['Boots', '$180.00', '$203.40', '$23.40'],
            ['Coat', '$220.00', '$248.60', '$28.60'],
            ['Shirt', '$25.00', '$28.25', '$3.25'],
        ]
        # WHEN the following module is executed:
        priceTable = cost.createPriceTable('formatted')
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(priceTable, expectedResult)


class CostSummaryTests(unittest.TestCase):

    def testShouldCreateRawCostSummary(self):
        # GIVEN the following preconditions corresponding to the system under test:
        costTable = [
            ['Item', 'Gross Price', 'Price After Tax', 'Taxes Paid'],
            ['Boots', 180, 203.39999999999998, 23.399999999999977],
            ['Coat', 220, 248.59999999999997, 28.599999999999966],
            ['Shirt', 25, 28.249999999999996, 3.2499999999999964],
        ]
        expectedCostSummary = [
            ["Number of Items", "Total Gross Price", "Total Price After Tax", "Total Taxes Paid"],
            [3, 425, 480.25, 55.25]
        ]
        # WHEN the following module is executed:
        costSummary = Cost("").createPriceSummary(costTable)
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(costSummary, expectedCostSummary)


    def testShouldCreateFormattedCostSummary(self):
        # GIVEN the following preconditions corresponding to the system under test:
        costTable = [
            ['Item', 'Gross Price', 'Price After Tax', 'Taxes Paid'],
            ['Boots', '$180.00', '$203.40', '$23.40'],
            ['Coat', '$220.00', '$248.60', '$28.60'],
            ['Shirt', '$25.00', '$28.25', '$3.25'],
        ]
        expectedCostSummary = [
            ['Number of Items', 'Total Gross Price', 'Total Price After Tax', 'Total Taxes Paid'],
            ['3', '$425.00', '$480.25', '$55.25']
        ]
        # WHEN the following module is executed:
        costSummary = Cost("").createPriceSummary(costTable)
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(costSummary, expectedCostSummary)


    def testShouldIdentifyFormattedTableForCostSummary(self):
        # GIVEN the following preconditions corresponding to the system under test:
        costTable = [
            ['Item', 'Gross Price', 'Price After Tax', 'Taxes Paid'],
            ['Boots', '$180.00', '$203.40', '$23.40'],
            ['Coat', '$220.00', '$248.60', '$28.60'],
            ['Shirt', '$25.00', '$28.25', '$3.25'],
        ]
        costSummary = CostSummary(costTable)
        # WHEN the following module is executed:
        typeOfTable = costSummary.typeOfCostTable()
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(typeOfTable, 'formatted')

    def testShouldIdentifyRawTableForCostSummary(self):
        # GIVEN the following preconditions corresponding to the system under test:
        costTable = [
            ['Item', 'Gross Price', 'Price After Tax', 'Taxes Paid'],
            ['Boots', 180, 203.39999999999998, 23.399999999999977],
            ['Coat', 220, 248.59999999999997, 28.599999999999966],
            ['Shirt', 25, 28.249999999999996, 3.2499999999999964],
        ]
        costSummary = CostSummary(costTable)
        # WHEN the following module is executed:
        typeOfTable = costSummary.typeOfCostTable()
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(typeOfTable, 'raw')


if __name__ == '__main__':
    unittest.main(testRunner=ColourTextTestRunner(verbosity=2))
