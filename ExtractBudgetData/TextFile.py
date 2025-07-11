class TextFile:
    def __init__(self, filePath):
        self.filePath = filePath

    def extractData(self):
        fileContent = self.getDataFromFile()
        return self.transformBudgetDataIntoPairStructure(fileContent)

    def getDataFromFile(self):
        try:
            with open(self.filePath, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {self.filePath} was not found")
        except Exception as e:
            raise IOError(f"An error occurred while reading the file: {str(e)}")

    def transformBudgetDataIntoPairStructure(self, fileContent):
        fileIdentifier = TextFileIdentifier(fileContent)
        return TextFileExtractor(fileIdentifier, fileContent).transform()


class TextFileIdentifier:
    def __init__(self, content):
        self.content = content

    def getFileType(self):
        if self.fileIsCSV():
            return 'csv'
        if self.fileContainsNewlineDelimiters():
            return 'newline'
        return 'unknown'

    def fileIsCSV(self):
        for char in self.content:
            if char == ',':
                return True
        return False

    def fileContainsNewlineDelimiters(self):
        for char in self.content:
            if char == '\n':
                return True
        return False


class TextFileExtractor:
    def __init__(self, fileIdentifier, content):
        self.fileIdentifier = fileIdentifier
        self.content = content

    def transform(self):
        typeOfFile = self.fileIdentifier.getFileType()
        if typeOfFile == 'csv':
            return self.transformCSVFile()
        elif typeOfFile == 'newline':
            return self.transformNewlineFile()
        else:
            raise ValueError("Unsupported file type")

    def transformCSVFile(self):
        items = self.content.split(',')
        items = list(map(str.strip, items))
        items = list(filter(None, items))
        return self.pairItems(items)

    def transformNewlineFile(self):
        items = self.content.split('\n')
        items = list(filter(None, items))
        return self.pairItems(items)

    def pairItems(self, items):
        pairedData = []
        for i in range(0, len(items), 2):
            if i + 1 < len(items):
                pairedData.append([items[i], items[i + 1]])
        return pairedData
