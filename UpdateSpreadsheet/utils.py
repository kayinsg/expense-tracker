import pendulum

class DateTranslator:
    def __init__(self, date):
        self.date = date

    def translateDate(self, targetFormat):
        if targetFormat == 'spreadsheet':
            return self.convertDateToSpreadsheetFormat(self.date)
        elif targetFormat == 'iso':
            return self.convertDateToPendulumFormat(self.date)
        raise ValueError("Unknown target format")

    def convertDateToSpreadsheetFormat(self, date):
        return pendulum.parse(date).format('MMM.DD.YYYY')

    def convertDateToPendulumFormat(self, date):
        return pendulum.from_format(date, 'MMM.DD.YYYY').format('YYYY-MM-DD')
