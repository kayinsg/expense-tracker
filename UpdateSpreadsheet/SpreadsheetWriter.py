class WorksheetDataDepositor:
    def __init__(self, workbook, worksheetName):
        self.workbook = workbook
        self.worksheetName = worksheetName

    def insert(self, dataFrame, series):
        nestedList = self.getNestedList(dataFrame, series)
        dateWorksheet = self.ensureWorksheetExists(self.workbook)
        return self.insertNestedListInWorkbook(dateWorksheet, nestedList)

    def getNestedList(self, dataFrame, series):
        return DataConsolidator(dataFrame).consolidate(series)

    def ensureWorksheetExists(self, workbook):
        try:
            return workbook[self.worksheetName]
        except:
            return self.workbook.create_sheet(self.worksheetName)

    def insertNestedListInWorkbook(self, dateWorksheet, nestedList):
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
        return NestedListNormalizer(nestedListComponents).getFinalizeNestedList()


class NestedListNormalizer:
    def __init__(self, nestedListComponents: dict):
        self.nestedListComponents = nestedListComponents
        self.finalNestedList: list[list] = [ ]

    def getFinalizeNestedList(self):
        for key in self.nestedListComponents:
            rowValues = self.nestedListComponents[key]
            self.addToFinalNestedList(rowValues)
        return self.finalNestedList

    def addToFinalNestedList(self, rowValues):
        if self.typeOfList(rowValues) == 'Single List':
            self.finalNestedList.append(rowValues)
        else:
            self.finalNestedList.extend(rowValues)

    def typeOfList(self, inputList):
        if isinstance(inputList[0], list):
            return 'List of Lists'
        return 'Single List'
