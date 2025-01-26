import re as regex
from ExtractBudgetData.SupportInterfaces.dataTypes import AtomicDataStructure, CompositeDataStructure

class TypeChecker:
    def __init__(self, dataToEvaluate: str | list | tuple):
        self.dataToEvaluate = dataToEvaluate
        self.dataType       = self.determineDataType()

    def determineDataType(self) -> str:
        category = self.createTypeCategory()
        dataType = category.checkDataType()
        return dataType

    def createTypeCategory(self):
        dataToEvaluate  = self.dataToEvaluate

        dataIsAtomic    = isinstance(dataToEvaluate, AtomicDataStructure)
        dataIsComposite = isinstance(dataToEvaluate, CompositeDataStructure)

        if dataIsAtomic:
            return AtomicTypeChecker(dataToEvaluate)

        elif dataIsComposite:
            return CompositeTypeChecker(dataToEvaluate)

        return AtomicTypeChecker(dataToEvaluate)


class TypeCheckerInterface:
    def checkDataType(self):
        raise NotImplementedError("This is an abstract class")


class AtomicTypeChecker(TypeCheckerInterface):
    def __init__(self, dataToEvaluate):
        self.dataToEvaluate = dataToEvaluate
        self.dataType = self.checkDataType()

    def checkDataType(self) -> str:
        dataToEvaluate = self.dataToEvaluate

        valueIsADecimalNumber = self.isADecimalNumber(dataToEvaluate)
        valueIsAWholeNumber   = self.isAnInteger(dataToEvaluate)
        valueIsNull           = dataToEvaluate is None

        if valueIsADecimalNumber:
            return "Decimal"
        elif valueIsAWholeNumber:
            return "Integer"
        elif valueIsNull:
            return "None"

        return "String"

    def isADecimalNumber(self, value) -> bool:
        decimalPattern = regex.compile(r"\d+\.\d+$")
        checkForDecimal = regex.match(decimalPattern, str(value))
        if checkForDecimal:
            return True
        else:
            return False

    def isAnInteger(self,value) -> bool:
        decimalPattern = regex.compile(r"\d+$")
        checkForInteger = regex.match(decimalPattern, str(value))
        if checkForInteger:
            return True
        else:
            return False


class CompositeTypeChecker(TypeCheckerInterface):
    def __init__(self, dataToEvaluate):
        self.dataToEvaluate = dataToEvaluate
        self.dataType       = self.checkDataType()

    def checkDataType(self) -> str:
        dataToEvaluate = self.dataToEvaluate
        iterableIsFloat = self.checkIterableForFloat(dataToEvaluate)
        iterableIsString = self.checkIterableForString(dataToEvaluate)
        if iterableIsFloat:
            return "Decimal"
        elif iterableIsString:
            return "String"
        else:
            return "None"

    def checkIterableForFloat(self, purportedFloatIterable) -> bool:
        checkedValues = list()

        for element in purportedFloatIterable:
            if AtomicTypeChecker(element).dataType == "Decimal":
                checkedValues.append(True)
            else:
                checkedValues.append(False)

        if all(checkedValues):
            return True

        return False

    def checkIterableForString(self, purportedStringIterable) -> bool:
        checkedValues = list()

        for element in purportedStringIterable:
            if AtomicTypeChecker(element).dataType == "String":
                checkedValues.append(True)
            else:
                checkedValues.append(False)

        if all(checkedValues):
            return True

        return False
