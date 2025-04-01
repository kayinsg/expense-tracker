import pendulum


class WorkbookPopulator:
    def __init__(self, currentDate):
        self.currentDate = currentDate

    def populate(self, workbook):
        cleanedWorkbook = self.removeDefaultWorksheet(workbook)
        daysWithinWeek = self.getDaysWithinTheWeekOfCurrentDate(self.currentDate)
        workbookWithDateWorksheets = self.insertDateWorksheetsInWorkbook(cleanedWorkbook, daysWithinWeek)
        return workbookWithDateWorksheets

    def removeDefaultWorksheet(self, workbook):
        return DefaultWorksheetEraser(workbook).getCleanWorkbook()

    def getDaysWithinTheWeekOfCurrentDate(self, currentDate):
        return WeekNormalizer(currentDate).getWeekdays()

    def insertDateWorksheetsInWorkbook(self, workbook, daysWithinWeek):
        for day in daysWithinWeek:
            workbook.create_sheet(day)
        return workbook


class DefaultWorksheetEraser:
    def __init__(self, workbook):
        self.workbook = workbook

    def getCleanWorkbook(self):
        defaultWorksheet = self.getDefaultWorksheet(self.workbook)
        self.removeDefaultWorksheet(defaultWorksheet)
        return self.workbook

    def getDefaultWorksheet(self, workbook):
        defaultWorksheet = workbook.active
        return defaultWorksheet

    def removeDefaultWorksheet(self, defaultWorksheet):
        self.workbook.remove(defaultWorksheet)


class WeekNormalizer:
    def __init__(self, currentDate):
        self.currentDate = currentDate

    def getWeekdays(self):
        currentDate = self.encodeCurrentDate(self.currentDate)
        startOfWeek = self.standardizeWeekToSunday(currentDate)
        return self.convertDateTimeObjectsToString(self.getListOfDatesForTheWeek(startOfWeek))

    def encodeCurrentDate(self, currentDate):
        return pendulum.parse(currentDate)

    def standardizeWeekToSunday(self, currentDate):
        dayOfWeek = currentDate.day_of_week
        if dayOfWeek == 6:
            startOfWeek = currentDate
        else:
            startOfWeek = currentDate.subtract(days=dayOfWeek + 1)
        return startOfWeek

    def getListOfDatesForTheWeek(self, startOfWeek):
        getDates = lambda dayNumber: startOfWeek.add(days=dayNumber)
        return list(map(getDates, range(7)))

    def convertDateTimeObjectsToString(self, dateTimeObjects):
        convert = lambda dateTime: dateTime.format('MMM.DD.YYYY')
        return list(map(convert, dateTimeObjects))
