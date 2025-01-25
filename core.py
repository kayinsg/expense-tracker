
from pandas import DataFrame

from SupportInterfaces.TableConstructor import TableCreator
from SupportInterfaces.TypeChecker import TypeChecker
from SupportInterfaces.SummaryConstructor import Summary
from SupportInterfaces.dataTransferObjects import Data
from paths import flatTextFile, spreadsheetPath
from spreadsheet import Spreadsheet


class DataFacade:
    def __init__(self):
        itemPricePairs = DataExtractor(flatTextFile).categorizeData()
        self.tableCreator = TableCreator(itemPricePairs)
        self.summaryCreator = Summary(itemPricePairs)

    def formattedData(self):
        viewTable = self.tableCreator.makeTable("view")
        formattedSummary = self.summaryCreator.getFormattedSummary()
        return Data(viewTable, formattedSummary)

    def rawData(self):
        rawTable = self.tableCreator.makeTable("raw")
        rawSummary = self.summaryCreator.getRawSummary()
        return Data(rawTable, rawSummary)


class DataExtractor:
    def __init__(self, filePath: str):
        with open(filePath, "r") as file:
            self.listOfLinesInFile = file.read().splitlines()

    def categorizeData(self) ->  list[tuple[str, int | float, float, int]]:
        listOfLinesInFile = self.listOfLinesInFile

        items: list[str] = list(
            filter(self._lineComprisesStrings, listOfLinesInFile)
        )
        pricesRepresentedAsStrings = list(
            filter(self._lineComprisesNumbers, listOfLinesInFile)
        )
        cost = Costs(pricesRepresentedAsStrings).get()
        itemPriceInformation = list(
            zip(
                items,
                cost['Prices'],
                cost['After-Tax Prices'],
                cost['Tax Per Item']
            )
        )

        return itemPriceInformation

    def _lineComprisesStrings(self, entry: str) -> bool:
        entryType = TypeChecker(entry).dataType
        if entryType == "String":
            return True
        return False

    def _lineComprisesNumbers(self, entry: str) -> bool:
        entryType = TypeChecker(entry).dataType
        if entryType == "Integer":
            return True
        elif entryType == "Decimal":
            return True
        return False


class Costs:
    def __init__(self, pricesRepresentedAsStrings):
        self.pricesRepresentedAsStrings = pricesRepresentedAsStrings
        self.taxRate = 0.13

    def get(self):
        numericPrices = list(
            map(
                self._convertPricesToNumericDataType,
                self.pricesRepresentedAsStrings
            )
        )
        afterTaxPrices = list(
            map(
                self._calculateAfterTaxPrices,
                numericPrices
            )
        )
        taxPaidPerItem = self._calculateTaxesPaidPerItem(numericPrices, afterTaxPrices) 

        return {
            'Prices': numericPrices,
            'After-Tax Prices': afterTaxPrices,
            'Tax Per Item': taxPaidPerItem,
        }

    def _convertPricesToNumericDataType(self, price: str) -> int | float:
        dataTypeOfPrice = TypeChecker(price).dataType
        if dataTypeOfPrice == "Integer":
            return int(price)
        elif dataTypeOfPrice == "Decimal":
            return float(price)
        return 0

    def _calculateAfterTaxPrices(self, price: int | float):
        taxMultiplier = 1 + self.taxRate
        afterTaxPrice = taxMultiplier * price
        return afterTaxPrice

    def _calculateTaxesPaidPerItem(
        self,
        grossPrices: list[int | float],
        afterTaxPrices: list[int | float],
    ) -> list[int] :

        pricePairs = list(zip(grossPrices, afterTaxPrices))

        taxesPaidPerItem = list()

        for grossPrice, afterTaxPrice in pricePairs:
            taxPaid = afterTaxPrice - grossPrice
            taxesPaidPerItem.append(taxPaid)

        return taxesPaidPerItem


data = DataFacade().formattedData()
Spreadsheet(spreadsheetPath).apply(data)
