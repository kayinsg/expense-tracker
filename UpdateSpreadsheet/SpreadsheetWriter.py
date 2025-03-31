import openpyxl
import pandas

class WorksheetDataDepositor:
    def __init__(self, workbook: openpyxl.Workbook, worksheetName: str):
        self.workbook: openpyxl.Workbook = workbook
        self.worksheetName: str = worksheetName

    def insert(self, dataFrame: pandas.DataFrame, series: pandas.Series) -> list[list]:
        nestedList: list[list] = self._getPandasData(dataFrame, series)
        dateWorksheet = self._ensureWorksheetExistsInWorkbook(self.workbook)
        return self._insertConsolidatedPandasDataInWorksheet(dateWorksheet, nestedList)

    def _getPandasData(self, dataFrame: pandas.DataFrame, series: pandas.Series) -> list[list]:
        return DataConsolidator(dataFrame).consolidate(series)

    def _ensureWorksheetExistsInWorkbook(self, workbook: openpyxl.Workbook) -> openpyxl.worksheet.worksheet.Worksheet:
        try:
            return workbook[self.worksheetName]
        except:
            return self.workbook.create_sheet(self.worksheetName)

    def _insertConsolidatedPandasDataInWorksheet(self, dateWorksheet, nestedList: list[list]) -> openpyxl.Workbook:
        for row in nestedList:
            dateWorksheet.append(row)
        return self.workbook


class DataConsolidator:
    def __init__(self, dataFrame):
        self.dataFrame = dataFrame

    def consolidate(self, series):
        dataFrameColumns = self.getDataFrameColumns(self.dataFrame)
        dataFrameValues = self.getDataFrameRowValues(self.dataFrame)
        seriesHeaders = self.getSeriesHeaders(series)
        seriesData = self.getSeriesData(series, seriesHeaders)
        nestedListComponents = {
            'Data Frame Columns': dataFrameColumns,
            'Data Frame Values': dataFrameValues,
            'Series Headers': seriesHeaders,
            'Series Data': seriesData,
        }
        return self.normalizeNestedList(nestedListComponents)

    def getDataFrameColumns(self, dataFrame):
        return list(map(lambda x: x, dataFrame.columns.tolist()))

    def getDataFrameRowValues(self, dataFrame):
        return list(map(lambda dataStructure: dataStructure[1].tolist(),  dataFrame.iterrows()))

    def getSeriesHeaders(self, series):
        return list(map(lambda x: x, series.index.tolist()))

    def getSeriesData(self, series, seriesHeaders):
        return list(map(lambda header: series.loc[header].tolist(), seriesHeaders))

    def normalizeNestedList(self, nestedListComponents: dict) -> list[list]:
        return NestedListNormalizer(nestedListComponents).getFinalList()


class NestedListNormalizer:
    def __init__(self, nestedListComponents: dict):
        self.nestedListComponents = nestedListComponents
        self.finalNestedList: list[list] = [ ]

    def getFinalList(self):
        for key in self.nestedListComponents:
            rowValues = self.nestedListComponents[key]
            self._addRowValuesToFinalNestedList(rowValues)
        return self.finalNestedList

    def _addRowValuesToFinalNestedList(self, rowValues):
        if self._typeOfListForPandasRowValues(rowValues) == 'Single List':
            self.finalNestedList.append(rowValues)
        else:
            self.finalNestedList.extend(rowValues)

    def _typeOfListForPandasRowValues(self, inputList):
        if isinstance(inputList[0], list):
            return 'List of Lists'
        return 'Single List'
