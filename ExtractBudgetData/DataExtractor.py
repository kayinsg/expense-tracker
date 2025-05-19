class TextFile:
    def __init__(self, content):
        self.content = content

    def extractData(self):
        fileIdentifier = TextFileIdentifier(self.content)
        return TextFileExtractor(fileIdentifier, self.content).transform()


class TextFileIdentifier:
    def __init__(self, content):
        self.content = content

    def getFileType(self):
        if self.fileIsCSV():
            return 'csv'
        if self.fileContainsNewlineDelimiters():
            return 'newline'
        return 'unknown'

    def fileIsCSV(self):
        for char in self.content:
            if char == ',':
                return True
        return False

    def fileContainsNewlineDelimiters(self):
        for char in self.content:
            if char == '\n':
                return True
        return False


class TextFileExtractor:
    def __init__(self, fileIdentifier, content):
        self.fileIdentifier = fileIdentifier
        self.content = content

    def transform(self):
        typeOfFile = self.fileIdentifier.getFileType()
        if typeOfFile == 'csv':
            return self.transformCSVFile()
        elif typeOfFile == 'newline':
            return self.transformNewlineFile()
        else:
            raise ValueError("Unsupported file type")

    def transformCSVFile(self):
        items = self.content.split(',')
        items = list(map(str.strip, items))
        items = list(filter(None, items))
        return self.pairItems(items)

    def transformNewlineFile(self):
        items = self.content.split('\n')
        items = list(filter(None, items))
        return self.pairItems(items)

    def pairItems(self, items):
        pairedData = []
        for i in range(0, len(items), 2):
            if i + 1 < len(items):
                pairedData.append([items[i], items[i + 1]])
        return pairedData


class Cost:
    def __init__(self, items):
        self.items = items

    def createPriceTable(self, typeOfTable):
        priceComputer = self.computePriceDetails
        return CostTable(self.items).createTable(priceComputer, typeOfTable)

    def computePriceDetails(self, item):
        basePriceNumber = int(item[1])
        taxMultiplier = 1.13
        priceAfterTax = basePriceNumber * taxMultiplier
        taxesPaid = priceAfterTax - basePriceNumber
        return [item[0], basePriceNumber, priceAfterTax, taxesPaid]


class CostTable:
    def __init__(self, items):
        self.items = items
        self.table = [['Item', 'Gross Price', 'Price After Tax', 'Taxes Paid']]

    def createTable(self, priceComputer, formatType):
        itemPriceDetails = list(map(priceComputer, self.items))
        if formatType == 'raw':
            self.getRawTable(itemPriceDetails)
        elif formatType == 'formatted':
            self.getFormattedTable(itemPriceDetails)
        return self.table

    def getRawTable(self, itemPriceDetails):
        self.table.extend(itemPriceDetails)

    def getFormattedTable(self, itemPriceDetails):
        formattedRows = self.standardizePrices(itemPriceDetails)
        self.table.extend(formattedRows)

    def standardizePrices(self, priceDetails):
        formattedRows = []
        for item in priceDetails:
            formattedRows.append([
                item[0],
                '{0:.2f}'.format(item[1]),
                '{0:.2f}'.format(item[2]),
                '{0:.2f}'.format(item[3])
            ])
        return formattedRows


class CostSummary:
    def __init__(self, costTable):
        self.costTable = costTable

    def compute(self, summaryType):
        if summaryType == 'raw':
            return self.createRawCostSummary()
        elif summaryType == 'formatted':
            return self.createFormattedCostSummary()
        raise ValueError("Unsupported summary type")

    def createRawCostSummary(self):
        return CostSummaryRaw(self.costTable).get()

    def createFormattedCostSummary(self):
        return CostSummaryFormatted(self.costTable).get()


class CostSummaryRaw:
    def __init__(self, costTable):
        self.costTable = costTable

    def get(self):
        headers = self.costTable[0]
        dataRows = self.costTable[1:]

        summaryHeaders = self.transformHeaders(headers)
        totals = self.createSummaryFromTable(dataRows, headers)
        roundedTotals = self.standardizeValuesToTwoDecimalPlaces(totals)

        return self.getFinalSummary(summaryHeaders, len(dataRows), roundedTotals)

    def transformHeaders(self, headers):
        return ["Number of Items"] + [f"Total {h}" for h in headers[1:]]

    def createSummaryFromTable(self, dataRows, headers):
        totals = [0.0] * (len(headers) - 1)
        for row in dataRows:
            for i in range(1, len(row)):
                totals[i-1] += row[i]
        return totals

    def standardizeValuesToTwoDecimalPlaces(self, totals):
        return [round(x, 2) for x in totals]

    def getFinalSummary(self, summaryHeaders, numItems, roundedTotals):
        summaryData = [numItems] + roundedTotals
        return [summaryHeaders, summaryData]


class CostSummaryFormatted:
    def __init__(self, costTable):
        self.costTable = costTable

    def get(self):
        headers = self.costTable[0]
        dataRows = self.costTable[1:]

        summaryHeaders = self.transformHeaders(headers)
        totals = self.createSummaryFromTable(dataRows, headers)
        formattedValues = self.standardizeValues(totals, len(dataRows))

        return self.getFinalSummary(summaryHeaders, formattedValues)

    def transformHeaders(self, headers):
        return ["Number of Items" if header == "Item" else f"Total {header}"
                for header in headers]

    def createSummaryFromTable(self, dataRows, headers):
        totals = [0.0] * (len(headers) - 1)
        for row in dataRows:
            for i in range(1, len(row)):
                totals[i-1] += float(row[i])
        return totals

    def standardizeValues(self, totals, itemCount):
        return [str(itemCount)] + ["{:.2f}".format(total) for total in totals]

    def getFinalSummary(self, summaryHeaders, formattedValues):
        return [summaryHeaders, formattedValues]
