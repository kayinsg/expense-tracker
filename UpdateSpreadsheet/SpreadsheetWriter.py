

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
        nestedList = [ ]
        nestedList.append(nestedListComponents['Data Frame Columns'])
        nestedList.extend(nestedListComponents['Data Frame Values'])
        nestedList.append(nestedListComponents['Series Headers'])
        nestedList.append(nestedListComponents['Series Data'])
        return nestedList
