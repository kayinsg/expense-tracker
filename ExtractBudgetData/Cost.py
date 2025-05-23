class Cost:
    def __init__(self, items):
        self.items = items

    def createPriceTable(self, typeOfTable):
        return CostTable(self.items).createTable(typeOfTable)


class CostTable:
    def __init__(self, items):
        self.items = items
        self.table = [['Item', 'Gross Price', 'Price After Tax', 'Taxes Paid']]

    def createTable(self, formatType):
        itemPriceDetails = list(map(self.computePriceDetails, self.items))
        if formatType == 'raw':
            self.table.extend(itemPriceDetails)
        elif formatType == 'formatted':
            formattedItemPriceDetails = self.standardize(itemPriceDetails)
            self.table.extend(formattedItemPriceDetails)
        return self.table

    def computePriceDetails(self, item):
        basePriceNumber = int(item[1])
        taxMultiplier = 1.13
        priceAfterTax = basePriceNumber * taxMultiplier
        taxesPaid = priceAfterTax - basePriceNumber
        return [item[0], basePriceNumber, priceAfterTax, taxesPaid]

    def standardize(self, priceDetails):
        def standardizePrice(item):
            return [
                item[0],
                '{0:.2f}'.format(item[1]),
                '{0:.2f}'.format(item[2]),
                '{0:.2f}'.format(item[3])
            ]
        return list(map(standardizePrice, priceDetails))


class TypeOfTable:
    def __init__(self, costTable):
        self.costTable = costTable

    def getTableType(self):
        if self.hasRawData():
            return 'raw'
        return 'formatted'

    def hasRawData(self):
        for row in self.costTable[1:]:
            for cell in row[1:]:
                if not self.isFormattedCell(cell):
                    return True
        return False

    def isFormattedCell(self, cell):
        if not isinstance(cell, str):
            return False
        try:
            float(cell)
            return '.' in cell and len(cell.split('.')[1]) == 2
        except ValueError:
            return False


class CostSummary:
    def __init__(self, costTable):
        self.costTable = costTable

    def compute(self):
        typeOfTable = self.typeOfCostTable()
        if typeOfTable == 'raw':
            return self.createRawCostSummary()
        elif typeOfTable == 'formatted':
            return self.createFormattedCostSummary()
        raise ValueError("Unsupported summary type")

    def typeOfCostTable(self):
        return TypeOfTable(self.costTable).getTableType()

    def createRawCostSummary(self):
        return CostSummaryRaw(self.costTable).get()

    def createFormattedCostSummary(self):
        valueStandardizer = ValueStandardizer()
        return CostSummaryFormatted(self.costTable, valueStandardizer).get()


class CostSummaryInterface:
    def __init__(self, costTable):
        self.costTable = costTable
        self.headers = self.costTable[0]
        self.items = self.costTable[1:]

    def transformHeaders(self, headers):
        return ["Number of Items"] + [f"Total {h}" for h in headers[1:]]


class CostSummaryRaw(CostSummaryInterface):
    def __init__(self, costTable):
        super().__init__(costTable)

    def get(self):
        summaryHeaders = self.transformHeaders(self.headers)
        totals = self.createSummaryFromTable(self.items, self.headers)
        roundedTotals = self.standardizeValuesToTwoDecimalPlaces(totals)

        return self.getFinalSummary(summaryHeaders, len(self.items), roundedTotals)

    def createSummaryFromTable(self, items, headers):
        totals = [0.0] * (len(headers) - 1)
        for row in items:
            for i in range(1, len(row)):
                totals[i-1] += row[i]
        return totals

    def standardizeValuesToTwoDecimalPlaces(self, totals):
        return [round(x, 2) for x in totals]

    def getFinalSummary(self, summaryHeaders, numItems, roundedTotals):
        summaryData = [numItems] + roundedTotals
        return [summaryHeaders, summaryData]


class CostSummaryFormatted(CostSummaryInterface):
    def __init__(self, costTable, valueStandardizer):
        super().__init__(costTable)
        self.valueStandardizer = valueStandardizer

    def get(self):
        summaryHeaders = self.transformHeaders(self.headers)
        totals = self.createSummaryFromTable(self.items, self.headers)
        formattedValues = self.valueStandardizer.standardize(len(self.items), totals)
        return [summaryHeaders, formattedValues]

    def createSummaryFromTable(self, items, headers):
        totals = [0.0] * (len(headers) - 1)
        for row in items:
            for i in range(1, len(row)):
                totals[i-1] += float(row[i])
        return totals


class ValueStandardizer:
    def standardize(self, itemCount, totals):
        standardizedCount = self.standardizeCount(itemCount)
        standardizedTotals = self.standardizeTotals(totals)
        return [ standardizedCount ] + standardizedTotals

    def standardizeCount(self, itemCount):
        return str(itemCount)

    def standardizeTotals(self, totals):
        standardized = []
        for total in totals:
            standardized.append("{:.2f}".format(total))
        return standardized
