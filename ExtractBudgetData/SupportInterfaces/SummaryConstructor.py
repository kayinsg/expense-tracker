from ExtractBudgetData.SupportInterfaces.TableConstructor import TableCreator
from pandas import Index
from abc import ABC, abstractmethod
from pandas import Series
from ExtractBudgetData.dataTypes import categorizedDataTuples


class Summary:
    def __init__(self, itemPricePairs: categorizedDataTuples):
        self.itemPricePairs = itemPricePairs

    def getRawSummary(self) -> Series:
        return RawSummary(self.itemPricePairs).getSummary()

    def getFormattedSummary(self) -> Series:
        seriesData = RawSummary(self.itemPricePairs).getSummary()
        return FormattedSummary(seriesData).getSummary()


class SummaryInterface(ABC):
    @abstractmethod
    def getSummary(self):
        pass


class RawSummary(SummaryInterface):
    def __init__(self, itemPairs):
        self.itemPricePairs = itemPairs
        self.table = TableCreator(self.itemPricePairs)

    def getSummary(self) -> Series:
        totalSummaryOfColumns: list = self.aggregateColumnSummaries()
        indexNames = Index([
            'Number of Entries',
            'Total Gross Price',
            'Total Final Price',
            'Total Taxes Paid'
        ])
        summaryTable = Series(
            totalSummaryOfColumns,
            index=indexNames
        )
        return summaryTable

    def aggregateColumnSummaries(self) -> list[str]:
        numberOfItems = list(
            self._getTotalAmountItems(
                self.table
            )
        )
        totalsForDollarColumns = list(
            self._getTotalsForEachDollarColumn(
                self.table
            )
        )
        totalSummaryColumns = (
            numberOfItems + totalsForDollarColumns
        )
        return totalSummaryColumns

    def _getTotalAmountItems(self, table):
        table = table.makeTable("view")
        yield len(table['Items'])

    def _getTotalsForEachDollarColumn(self, table):
        dollarColumns = table.getDollarColumnsFromTable()
        for column in dollarColumns:
            totalForColumn = sum(column['Values'])
            yield totalForColumn


class FormattedSummary(SummaryInterface):
    def __init__(self, summary: Series):
        self.summary = summary

    def getSummary(self) -> Series:
        primitiveSummary = dict()
        items = list(self.summary.items())
        for label, value in items:
            if label == "Number of Entries":
                originalValue = value
                formattedValue = str(int(originalValue))
                primitiveSummary[label] = formattedValue
            else:
                originalValue = value
                formattedValue = f"$ {originalValue:05.2f}"
                primitiveSummary[label] = formattedValue

        return Series(primitiveSummary)
