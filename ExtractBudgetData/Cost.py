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
        valueStandardizer = ValueStandardizer()
        return CostSummaryFormatted(valueStandardizer, self.costTable).get()


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
    def __init__(self, valueStandardizer, costTable):
        self.valueStandardizer = valueStandardizer
        self.costTable = costTable

    def get(self):
        headers = self.costTable[0]
        dataRows = self.costTable[1:]

        summaryHeaders = self.transformHeaders(headers)
        totals = self.createSummaryFromTable(dataRows, headers)
        formattedValues = self.valueStandardizer.standardize(len(dataRows), totals)
        return [summaryHeaders, formattedValues]

    def transformHeaders(self, headers):
        return ["Number of Items" if header == "Item" else f"Total {header}"
                for header in headers]

    def createSummaryFromTable(self, dataRows, headers):
        totals = [0.0] * (len(headers) - 1)
        for row in dataRows:
            for i in range(1, len(row)):
                totals[i-1] += float(row[i])
        return totals


class ValueStandardizer:
    def standardize(self, itemCount, totals):
        standardizedCount = self.standardizeCount(itemCount)
        standardizedTotals = self.standardizeTotals(totals)
        return [standardizedCount] + standardizedTotals

    def standardizeCount(self, itemCount):
        return str(itemCount)

    def standardizeTotals(self, totals):
        standardized = []
        for total in totals:
            standardized.append("{:.2f}".format(total))
        return standardized
