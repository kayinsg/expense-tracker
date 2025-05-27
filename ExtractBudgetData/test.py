import unittest
from Cost import Cost, CostSummary
from TextFile import TextFile, TextFileIdentifier
from colour_runner.runner import ColourTextTestRunner


class FileDataExtractorTests(unittest.TestCase):

    class FakeCSVTextFile(TextFile):
        def __init__(self, filePath):
            self.filePath = filePath

        def getDataFromFile(self):
            return 'Laptop, 400, Desk, 220, Headphones, 120'

    class FakeNewlineTextFile(TextFile):
        def __init__(self,filePath):
            self.filePath = filePath

        def getDataFromFile(self):
            return 'A Shoes From New York\n40\nMug\n2\nSweater\n40'

    def testShouldExtractTextFromCSVFlatTextFile(self):
        # GIVEN the following preconditions corresponding to the system under test:
        csvFile = self.FakeCSVTextFile("")
        expected = [['Laptop', '400'], ['Desk', '220'], ['Headphones', '120']]
        # WHEN the following module is executed:
        actual = csvFile.extractData()
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(actual, expected)

    def testShouldExtractTextFromFlatTextFileWithNewlines(self):
        # GIVEN the following preconditions corresponding to the system under test:
        newlineFile = self.FakeNewlineTextFile("")
        expected = [['A Shoes From New York', '40'], ['Mug', '2'], ['Sweater', '40']]
        # WHEN the following module is executed:
        actual = newlineFile.extractData()
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(expected, actual)


class FileIdentifierTests(unittest.TestCase):

    def getTextFileData(self, type):
        if type == 'csv':
            return 'Laptop, 400, Desk, 220, Headphones, 120'
        if type == 'newline':
            return 'A Shoes From New York\n40\nMug\n2\nSweater\n40'

    def testShouldIdentifyFlatTextFileWithNewlines(self):
        # GIVEN the following preconditions corresponding to the system under test:
        textFileData = self.getTextFileData('newline')
        textFileIdentifier = TextFileIdentifier(textFileData)
        # WHEN the following module is executed:
        result = textFileIdentifier.getFileType()
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(result, 'newline')

    def testShouldIdentifyCSVFile(self):
        # GIVEN the following preconditions corresponding to the system under test:
        textFileData = self.getTextFileData('csv')
        textFileModule = TextFileIdentifier(textFileData)
        # WHEN the following module is executed:
        result = textFileModule.getFileType()
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(result, 'csv')


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


class SummaryTableConsolidatorTests(unittest.TestCase):

    def testShouldConsolidateCostDetailsGivenTableAndSummary(self):
        # GIVEN the following preconditions corresponding to the system under test:
        costTable = [
            ['Item', 'Gross Price', 'Price After Tax', 'Taxes Paid'],
            ['Boots', '$180.00', '$203.40', '$23.40'],
            ['Coat', '$220.00', '$248.60', '$28.60'],
            ['Shirt', '$25.00', '$28.25', '$3.25'],
        ]
        costSummary = [
            ['Number of Items', 'Total Gross Price', 'Total Price After Tax', 'Total Taxes Paid'],
            ['3', '$425.00', '$480.25', '$55.25']
        ]
        cost = Cost("")
        expectedResult = [
            ['Item', 'Gross Price', 'Price After Tax', 'Taxes Paid'],
            ['Boots', '$180.00', '$203.40', '$23.40'],
            ['Coat', '$220.00', '$248.60', '$28.60'],
            ['Shirt', '$25.00', '$28.25', '$3.25'],
            ['Number of Items', 'Total Gross Price', 'Total Price After Tax', 'Total Taxes Paid'],
            ['3', '$425.00', '$480.25', '$55.25']
        ]
        # WHEN the following module is executed:
        actualResult = cost.consolidatePriceInfo(costTable, costSummary)
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(actualResult, expectedResult)

        

if __name__ == '__main__':
    unittest.main(testRunner=ColourTextTestRunner(verbosity=2))
