import pendulum


class DateTranslator:
    def __init__(self, date):
        # Check if the date is already in ISO format (YYYY-MM-DD)
        try:
            parsed = pendulum.parse(date, strict=False)
            if parsed.format('YYYY-MM-DD') == date:
                self.date = date
                self.is_iso = True
            else:
                self.date = date
                self.is_iso = False
        except:
            self.date = date
            self.is_iso = False

    def translateDate(self, targetFormat):
        if targetFormat == 'spreadsheet':
            if self.is_iso:
                return pendulum.parse(self.date).format('MMM.DD.YYYY')
            return self.convertDateToSpreadsheetFormat(self.date)
        elif targetFormat == 'iso':
            if self.is_iso:
                return self.date
            return self.convertDateToPendulumFormat(self.date)
        raise ValueError("Unknown target format")

    def convertDateToSpreadsheetFormat(self, date):
        return pendulum.parse(date, strict=False).format('MMM.DD.YYYY')

    def convertDateToPendulumFormat(self, date):
        return pendulum.from_format(date, 'MMM.DD.YYYY').format('YYYY-MM-DD')
