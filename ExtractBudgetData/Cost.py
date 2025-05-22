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
            self.completeTable(itemPriceDetails)
        elif formatType == 'formatted':
            formattedRows = self.standardize(itemPriceDetails)
            self.completeTable(formattedRows)
        return self.table

    def computePriceDetails(self, item):
        basePriceNumber = int(item[1])
        taxMultiplier = 1.13
        priceAfterTax = basePriceNumber * taxMultiplier
        taxesPaid = priceAfterTax - basePriceNumber
        return [item[0], basePriceNumber, priceAfterTax, taxesPaid]

    def completeTable(self, itemPriceDetails):
        self.table.extend(itemPriceDetails)

    def standardize(self, priceDetails):
        def standardizePrice(item):
            return [
                item[0],
                '{0:.2f}'.format(item[1]),
                '{0:.2f}'.format(item[2]),
                '{0:.2f}'.format(item[3])
            ]
        return list(map(standardizePrice, priceDetails))


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
        return CostSummaryFormatted(valueStandardizer, self.costTable).get()


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


class CostSummaryRaw:
    def __init__(self, costTable):
        self.costTable = costTable

    def get(self):
        headers = self.costTable[0]
        items = self.costTable[1:]

        summaryHeaders = self.transformHeaders(headers)
        totals = self.createSummaryFromTable(items, headers)
        roundedTotals = self.standardizeValuesToTwoDecimalPlaces(totals)

        return self.getFinalSummary(summaryHeaders, len(items), roundedTotals)

    def transformHeaders(self, headers):
        return ["Number of Items"] + [f"Total {h}" for h in headers[1:]]

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


class CostSummaryFormatted:
    def __init__(self, valueStandardizer, costTable):
        self.valueStandardizer = valueStandardizer
        self.costTable = costTable

    def get(self):
        costTableDetails = self.extractTableDetails()
        summaryHeaders = self.transformHeaders(costTableDetails['headers'])
        totals = self.createSummaryFromTable(costTableDetails['items'], costTableDetails['headers'])
        formattedValues = self.valueStandardizer.standardize(len(costTableDetails['items']), totals)
        return [summaryHeaders, formattedValues]


    def extractTableDetails(self):
        return {
            'headers': self.costTable[0],
            'items':self.costTable[1:],
        }

    def transformHeaders(self, headers):
        return ["Number of Items" if header == "Item" else f"Total {header}"
                for header in headers]

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
