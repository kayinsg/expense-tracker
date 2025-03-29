from pandas import DataFrame

def consolidateSeriesAndDataFrame(dataFrame: pandas.DataFrame, series: pandas.Series):
    result = [ ]

    dataFrameColumns =  [ ]
    for column in dataFrame.columns.tolist():
        dataFrameColumns.append(column)
    result.append(dataFrameColumns)

    for dataStructure in dataFrame.iterrows():
        result.append(dataStructure[1].tolist())

    seriesHeaders = [ ]
    for index in series.index.tolist():
        seriesHeaders.append(index)
    result.append(seriesHeaders)

    seriesData = [ ]
    for header in seriesHeaders:
        seriesData.append(series.loc[header].tolist())

    result.append(seriesData)

    return result
