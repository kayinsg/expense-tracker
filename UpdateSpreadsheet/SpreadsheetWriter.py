

class DataConsolidator:
    def __init__(self, dataFrame):
        self.dataFrame = dataFrame

    def consolidate(self, series):
        dataFrameColumns = self.getDataFrameColumns(self.dataFrame)
        dataFrameValues = self.getDataFrameRowValues(self.dataFrame)
        seriesHeaders = self.getSeriesHeaders(series)
        seriesData = self.getSeriesData(series, seriesHeaders)
        nestedListComponents = {'Data Frame Columns': dataFrameColumns, 'Data Frame Values': dataFrameValues, 'Series Headers': seriesHeaders, 'Series Data': seriesData}
        return self.finalizeNestedList(nestedListComponents)

    def getDataFrameColumns(self, dataFrame):
        return list(map(lambda x: x, dataFrame.columns.tolist()))

    def getDataFrameRowValues(self, dataFrame):
        return list(map(lambda dataStructure: dataStructure[1].tolist(),  dataFrame.iterrows()))

    def getSeriesHeaders(self, series):
        return list(map(lambda x: x, series.index.tolist()))

    def getSeriesData(self, series, seriesHeaders):
        return list(map(lambda header: series.loc[header].tolist(), seriesHeaders))

    def finalizeNestedList(self, nestedListComponents):
        finalNestedList = [ ]

        addToNestedList = lambda rowValues: finalNestedList.append(rowValues)
        flattenListThenAddToNestedList = lambda rowValues: finalNestedList.extend(rowValues)

        for key in nestedListComponents:
            rowValues = nestedListComponents[key]
            if self.isAListOfLists(rowValues):
                flattenListThenAddToNestedList(rowValues)
            else:
                addToNestedList(rowValues)

        return finalNestedList

    def isAListOfLists(self, inputList):
        if not isinstance(inputList, list):
            return False
        
        for element in inputList:
            if not isinstance(element, list):
                return False
        return True
