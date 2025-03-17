from abc import ABC, abstractmethod
from pandas import DataFrame
from pandas import Index

from ExtractBudgetData.dataTypes import categorizedDataTuples
from ExtractBudgetData.SupportInterfaces.TypeChecker import TypeChecker


class TableCreator:
    def __init__(self, itemPricePairs: categorizedDataTuples):
        self.itemPricePairs = itemPricePairs

    def getDollarColumnsFromTable(self) -> list[dict]:
        table = RawTableBuilder(self.itemPricePairs).constructTable()
        return BeautifiedTableBuilder(self.itemPricePairs).getDollarColumns(table)

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

    def constructTable(self) -> DataFrame:
        itemPricePairsSortedByPrice = self.sortItemsByPrice(self.itemPricePairs)
        itemPriceTable              = self.putDataIntoTable(itemPricePairsSortedByPrice)
        return itemPriceTable

    def sortItemsByPrice(self, itemPricePairs):
        return sorted(
            itemPricePairs,
            key=lambda categorizedDataTuple: categorizedDataTuple[1],
            reverse=True
        )

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
        dollarColumns: list[dict] = self.getDollarColumns(self.table)
        beautifiedTable = self._padDollarColumnValues(
            self.table,
            dollarColumns
        )
        return beautifiedTable

    def getDollarColumns(self, table) -> list[dict]:
        totalColumns: list[str] = table.columns.tolist()
        dollarColumns = list()
        for column in totalColumns:
            columnValues = table[column].tolist()
            if TypeChecker(columnValues).dataType == "Decimal":
                dollarColumns.append(
                    {
                        'Name': column,
                        'Values': columnValues,
                    }
                )
            else:
                pass
        return dollarColumns

    def _padDollarColumnValues(
        self,
        dataFrame,
        dollarColumns: list[dict[str, list[int]]],
    ):
        for column in dollarColumns:
            paddedValues = list()
            for value in column['Values']:
                paddedDecimal = f"$ {value:05.2f}"
                paddedValues.append(paddedDecimal)
            dataFrame[column['Name']] = paddedValues
        return dataFrame
