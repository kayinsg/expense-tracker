
from pandas import DataFrame


from SupportInterfaces.TableConstructor import TableCreator
from SupportInterfaces.TypeChecker import TypeChecker
from SupportInterfaces.SummaryConstructor import Summary
from SupportInterfaces.dataTransferObjects import Data
from SupportInterfaces.utils import readLinesFromFile
from paths import flatTextFile, spreadsheetPath
from spreadsheet import Spreadsheet


class TableFacade:
    def __init__(self, flatTextPath: str):
        self.itemPricePairs = DataExtractor(
            readLinesFromFile(flatTextPath)
        ).categorizeData()

    def getRawTable(self) -> DataFrame:
        return TableCreator(self.itemPricePairs).makeTable("raw")

    def getFormattedTable(self) -> DataFrame:
        return TableCreator(self.itemPricePairs).makeTable("view")


class DataExtractor:
    def __init__(self, listOfLinesInFile: list[str]):
        self.listOfLinesInFile = listOfLinesInFile

    def categorizeData(self) ->  list[tuple[str, int | float, float, int]]:
        listOfLinesInFile = self.listOfLinesInFile

        items: list[str] = list(filter(
            self._lineComprisesStrings,
            listOfLinesInFile
        ))
        pricesRepresentedAsStrings = list(filter(
            self._lineComprisesNumbers,
            listOfLinesInFile
        ))
        numericPrices = list(map(
            self._convertPricesToNumericDataType,
            pricesRepresentedAsStrings
        ))
        afterTaxPrices = list(map(
            self._calculateAfterTaxPrices,
            numericPrices
        ))

        taxPaidPerItem = self._calculateTaxesPaidPerItem(
            numericPrices,
            afterTaxPrices
        )

        itemPriceInformation = list(zip(
            items,
            numericPrices,
            afterTaxPrices,
            taxPaidPerItem
        ))

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

    def _convertPricesToNumericDataType(self, price: str) -> int | float:
        dataTypeOfPrice = TypeChecker(price).dataType
        if dataTypeOfPrice == "Integer":
            return int(price)
        elif dataTypeOfPrice == "Decimal":
            return float(price)
        return 0

    def _calculateAfterTaxPrices(self, price: int | float):
        countryTaxRateInDecimal = 0.13
        taxMultiplier = 1 + countryTaxRateInDecimal
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


def getFormattedData():
    flatTextFileContent = readLinesFromFile(flatTextFile)
    itemPricePairs = DataExtractor(flatTextFileContent).categorizeData()
    summary = Summary(itemPricePairs)
    formattedSummary = summary.getFormattedSummary()
    
    table = TableFacade(flatTextFile)
    viewTable = table.getFormattedTable()
    
    return Data(viewTable, formattedSummary)

def getRawData():
    rawTable = TableFacade(flatTextFile).getRawTable()
    itemPricePairs = DataExtractor(readLinesFromFile(flatTextFile)).categorizeData()

    summary = Summary(itemPricePairs)
    rawSummary = summary.getRawSummary()

    return Data(rawTable, rawSummary)


data = getFormattedData()
Spreadsheet(spreadsheetPath).apply(data)
