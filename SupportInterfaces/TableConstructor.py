from abc import ABC, abstractmethod
from pandas import DataFrame
from pandas import Index

from .utils import getDollarColumns
from .dataTransferObjects import ColumnDetails


class TableCreator:
    def __init__(self, itemPricePairs: list):
        self.itemPricePairs = itemPricePairs

    def getDollarColumnsFromTable(self):
        rawTable = RawTableBuilder(self.itemPricePairs).constructTable()
        return getDollarColumns(rawTable)

    def makeTable(self, typeOfTable) -> DataFrame:
        tableType = self._determineTypeOfTable(typeOfTable)
        return tableType.constructTable()

    def _determineTypeOfTable(self, typeOfTable):
        if typeOfTable == "raw":
            return RawTableBuilder(self.itemPricePairs)
        elif typeOfTable == "view":
            return BeautifiedTableBuilder(self.itemPricePairs)
        return RawTableBuilder(self.itemPricePairs)


class TableInterface(ABC):
    @abstractmethod
    def constructTable(self):
        raise NotImplementedError("This is an abstract class.")


class RawTableBuilder(TableInterface):
    def __init__(self, itemPricePairs):
        self.itemPricePairs = itemPricePairs

    def constructTable(self):
        itemPricePairsSortedByPrice =  set(self.sortPricesHighToLow())
        itemPriceTable              =  self.putDataIntoTable(itemPricePairsSortedByPrice)
        return itemPriceTable

    def sortPricesHighToLow(self):
        itemPricePairs = self.itemPricePairs
        grossPrices = list()
        for item in itemPricePairs:
            grossPrices.append(item[1])
        sortedGrossPrices = sorted(grossPrices, reverse=True)
        for grossPrice in sortedGrossPrices:
            for item in itemPricePairs:
                if grossPrice == item[1]:
                    yield item

    def putDataIntoTable(self, itemPricePairs) -> DataFrame:
        columnNames = Index(
            ["Items", "Prices", "Final Prices", "Taxes Paid"]
        )
        itemsPricesTable = DataFrame(
            itemPricePairs,
            columns=columnNames
        )
        return itemsPricesTable


class BeautifiedTableBuilder(TableInterface):
    def __init__(self, itemPricePairs):
        self.table = RawTableBuilder(itemPricePairs).constructTable()

    def constructTable(self) -> DataFrame:
        table = self.table
        dollarColumns = getDollarColumns(table)
        beautifiedTable = self._padDollarColumnValues(
            table,
            dollarColumns
        )
        return beautifiedTable

    def _padDollarColumnValues(
        self,
        dataFrame,
        dollarColumns: list[ColumnDetails],
    ):
        for column in dollarColumns:
            paddedValues = list()
            for value in column.values:
                paddedDecimal = f"$ {value:05.2f}"
                paddedValues.append(paddedDecimal)
            dataFrame[column.name] = paddedValues
        return dataFrame
