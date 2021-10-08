import re # Regex expressions
from abc import ABC # Abstract for polymorphism and inheritance

class cronArgument(ABC):
# class cronArgument:
    """
    Base form of cron argument. Shares common structure.
    """

    # Define the possible types of cron types
    cronTypes = ("INVALID", "WILDCARD", "SINGLE", "VALUES", "RANGE", "INTERVAL")

    # Define the given cron argument type and validity
    cronType:str = str
    isValid:bool = bool

    # Process valid types
    value:list[int] = list[int]
    printableValue:str = str

    def __init__(self, arg:str):
        """
        Constructor. Defines type of cron argument.
        """

        printableValue = self.cronTypes[0]
        cronType = self.cronTypes[0]
        value = []
        isValid = False

        # Match cron type
        self.cronType = self.matchCronArgument(arg)

        # Set cron isValid attribute
        if ( self.cronType == self.cronTypes[0] ) or ( self.value is None ) :
            self.setInvalid()

    def matchCronArgument(self, arg:str) -> cronType:
        """
        Match the type of cron argument to one from the tuple defined in class.
        :return:
        Returns the detected CronType for further checkups
        """
        # Wildcard detected
        if self.verifyWildcard(arg):
            self.value = '*'
            return self.cronTypes[1]

        # Single detected
        elif self.verifySingle(arg):
            self.value = self.breakdownSingle(arg)
            return self.cronTypes[2]

        # Separated Values detected
        elif self.verifyValues(arg):
            self.value = self.breakdownValues(arg)
            return self.cronTypes[3]

        # Range detected
        elif self.verifyRange(arg):
            self.value = self.breakdownRange(arg)
            return self.cronTypes[4]

        # Interval detected
        elif self.verifyInterval(arg):
            self.value = self.breakdownInterval(arg)
            return self.cronTypes[5]

        # Invalid type of cron argument, none detected
        else:
            return self.cronTypes[0]

    def getCronType(self) -> cronType:
        """
        Get method for exporting cron type outside of class
        :return:
        The type of cronType detected
        """
        return self.cronType

    def getIsValid(self) -> bool:
        """
        Get method for exporting the is_valid variable.
        Detects weather or not an argument is a cron argument.
        :return:
        True if detected argument is a valid cron argument
        False if detected an invalid cron argument.
        """
        return self.isValid

    def getPrintableValue(self) -> str:
        """
        Get printable value
        :return:
        Printable value as string
        """

        return self.printableValue

    def setInvalid(self):
        """
        Sets cron command to invalid
        :return:
        None
        """

        self.cronType = self.cronTypes[0]
        self.isValid = False
        self.printableValue = self.cronType

    def verifyWildcard(self, arg:str) -> bool:
        """
        Checks if given cron argument is of type wildcard - *
        """
        if arg == '*':
            return True
        return False

    def verifySingle(self, arg:str) -> bool:
        """
        Checks if given cron argument is of type single.
        A given number in range.
        """

        # Regex
        # if re.search("(?:^[0-5][0-9]$|^[0-9]$)", arg):
        #     return True
        # return False

        # Check that value is a natural number
        if type(arg) is str:
            if arg.isdigit():
                return True
        if type(arg) is not int:
            if str(arg).isdigit():
                return True

            # raise ValueError("Please input a string")
        return False

    def verifyValues(self, arg:str) -> bool:
        """
        Checks if given cron argument is of type separated values.
        A given set of natural numbers separated by a comma (,).
        """

        regex = "^(\d[,]\d?){1,}[^,]$"
        try:
            if re.match(regex, arg) is None:
                return False
        except TypeError:
            return True

    def verifyRange(self, arg:str) -> bool:
        """
        Checks if given cron argument is of type range.
        Two numbers separated by a '-'
        """

        # Check if matches natural number - natural number via regex
        regex = "(?:^[0-9]{1,2}[-][0-9]{1,2}$)"
        if re.match(regex, arg) is None:
            return False
        return True

    def verifyInterval(self, arg:str) -> bool:
        """
        Checks if given cron argument is of type interval.
        Wildcard (*) followed by a slash (/) and then a number.
        """

        regex = "(?:^[*][/][0-9]{1,2}$)"
        # Match structure of */NUMBER with regex
        if re.match(regex, arg) is None:
            return False
        return True

    def breakdownSingle(self, arg:str) -> int:
        """
        Casts a single cron argument to an integer
        :param arg:
        Cron arguments
        :return:
        Integer of cron argument.
        None if casting failed.
        """

        if type(arg) in [int, float]:
            return int(arg)
        else:
            return None
            raise ValueError("Expected integer")

    def breakdownValues(self, arg:str) -> list[int]:
        """
        Breaks down a values argument.
        :param arg:
        Cron values argument
        :return:
        List with objects without separators.
        Returns None if casting failed.
        """

        # List of values to return
        values:int = []
        if arg is str:
            for value in arg.split(','):
                try:
                    values.append(int(value))
                except ValueError:
                    return None
        else:
            return None

        return values

        # Check that input is an odd number, even number indicates an error
        # if ( len(arg) % 2 ) == 0:
        #     return False
        # # Check for natural numbers in odd places
        # for i in arg[0::2]:
        #     if self.verifySingle(i) is False:
        #         return False
        # # Check for commas in even places
        # for i in arg[1::2]:
        #     if i != ',':
        #         return False
        # return True

    def breakdownRange(self, arg:str) -> list[int]:
        """
        Breaks down a given range.
        :param arg:
        Values as cron arguments
        :return:
        Returns a list of length = 2
        First argument (before -)
        Second argument (after -)
        Returns None if casting failed
        """

        values:int = []

        for value in arg.split('-'):
            try:
                values.append(int(value))
            except ValueError:
                return None

        return values

        # Check if separator by -
        # if arg.find('-') == -1:
        #         return False
        #
        # # Split by -
        # separated_str = arg.split('-')
        #
        # # Check first number is natural number
        # if self.verifySingle(separated_str[0]) is False:
        #     return False
        # # Check second number is natural number
        # if self.verifySingle(separated_str[2]) is False:
        #     return False
        # return True

    def breakdownInterval(self, arg:str) -> int:
        """
        Breaks down the interval cron argument.
        Interval is always of type */natural.
        :param arg:
        Cron arguments
        :return:
        Returns an int with the interval (after */).
        Returns None if out of index.
        """

        value:int
        try:
            value = arg[arg.rindex('/')+1:]
            return int(value)
        except IndexError:
            raise IndexError("Out of bounds")
        except ValueError:
            raise ValueError("Value isn't an integer")
            return None

class minuteCronArgument(cronArgument):

    printableValue = ""

    def __init__(self, arg):
        """Constructor. Defines type of cron argument."""
        super().__init__(arg)

        # Wildcard type
        if self.cronType == self.cronTypes[1]:
            self.printableValue = self.parseWildcard()

        # Single type
        if self.cronType == self.cronTypes[2]:
            self.printableValue = self.parseSingle()

        # Values type
        if self.cronType == self.cronTypes[3]:
            self.printableValue = self.parseValues()

        # Range type
        if self.cronType == self.cronTypes[4]:
            self.printableValue = self.parseRange()

        # Interval type
        if self.cronType == self.cronTypes[5]:
            self.printableValue = self.parseInterval()

        # Invalid type
        if self.cronType == self.cronTypes[0]:
            self.isValid = False
            self.printableValue = self.cronTypes[0]

    def parseWildcard(self) -> str:
        """
        Parses a wildcard for the minute cron argument
        :return:
        A string with all the numbers representing a minute within the hour: 1-59
        """

        values:str = ""

        for i in range(1,60):
            values += str(i) + ' '

        return values

    def parseSingle(self) -> str:
        """
        Converts cron single minute argument to a string of active minutes
        :param arg:
        :return:
        String with length=1 OR 2 of minute in which cron will take place
        """

        value:str = ""

        if 0 <= self.value < 60:
            value = str(self.value)
        else:
            self.setInvalid()

        return value

    def parseValues(self) -> str:
        """
        Returns a list with values given via cron argument.
        Please note that there may be duplicated values, this is acceptable by crontab guru - https://crontab.guru/#3,4,1,3_0_*_8_*.
        :param arg:
        :return:
        String with range of values given.
        """

        values:str = ""

        for value in self.value:
            # Check that it is in range
            if 0 <= value < 60:
                # Check that numbers only exist once
                if values.find(str(value)) == -1:
                    values += str(value) + ' '
            else:
                self.setInvalid()

        return values

    def parseRange(self) -> str:
        """
        Parses a range or given values
        :param arg:
        :return:
        String of cron arguments seperated by spaces.
        Returns none if this is an invalid cron argument.
        """

        values:str = ""
        rangeStart = self.value[0]
        rangeEnd = self.value[1]

        # Check beginning of range is smaller than ending and range is correct
        if (rangeStart < rangeEnd) and (0 <= rangeStart < 60) and (0 <= rangeEnd < 60):
            for value in range(rangeStart, rangeEnd+1):
                values += str(value) + " "
            return values

        self.setInvalid()
        return None

    def parseInterval(self) -> str:
        """
        Parses a cron minute interval given
        :param arg:
        :return:
        String with the minutes in which a cron command will run.
        If this is not a valid cron argument, returns None.
        """

        # Values allowed by cron minute and second arguments. They are dividable by 60
        allowedIntervals = [2, 3, 4, 5, 6, 10, 12, 15, 20, 30]
        cronRange = ""

        if self.value in allowedIntervals:
            # return str(self.value)
            for i in range(0,60, self.value):
                cronRange += str(i) + ' '
            return cronRange

        self.setInvalid()
        return None

class hourCronArgument(cronArgument):

    def __init__(self, arg):
        """
        Constructor. Defines type of cron argument.
        """
        super().__init__(arg)

        # Wildcard type
        if self.cronType == self.cronTypes[1]:
            self.printableValue = self.parseWildcard()

        # Single type
        if self.cronType == self.cronTypes[2]:
            self.printableValue = self.parseSingle()

        # Values type
        if self.cronType == self.cronTypes[3]:
            self.printableValue = self.parseValues()

        # Range type
        if self.cronType == self.cronTypes[4]:
            self.printableValue = self.parseRange()

        # Invalid type (such as interval for hour)
        if self.cronType == self.cronTypes[0] or self.cronType == self.cronTypes[5]:
            self.setInvalid()

    def parseWildcard(self) -> str:
        """
        Parses a wildcard for the minute cron argument
        :return:
        A string with all the numbers representing a minute within the hour: 1-59
        """

        values:str = ""

        for i in range(0,24):
            values += str(i) + ' '

        return values

    def parseSingle(self) -> str:
        """
        Converts cron single minute argument to a string of active minutes
        :return:
        String with length=1 OR 2 of minute in which cron will take place
        """

        value:str = ""

        if 0 <= self.value < 24:
            value = str(self.value)
            return value

        self.setInvalid()
        # return value

    def parseValues(self) -> str:
        """
        Returns a list with values given via cron argument.
        Please note that there may be duplicated values, this is acceptable by crontab guru - https://crontab.guru/#3,4,1,3_0_*_8_*.
        :return:
        String with range of values given.
        """

        values:str = ""

        for value in self.value:
            # Check that it is in range
            if 0 <= value < 24:
                # Check that numbers only exist once
                if values.find(str(value)) == -1:
                    values += str(value) + ' '
            else:
                self.setInvalid()

        return values

    def parseRange(self) -> str:
        """
        Parses a range or given values
        :param arg:
        :return:
        String of cron arguments seperated by spaces.
        Returns none if this is an invalid cron argument.
        """

        values:str = ""
        rangeStart = self.value[0]
        rangeEnd = self.value[1]

        # Check beginning of range is smaller than ending and range is correct
        if (rangeStart < rangeEnd) and (0 <= rangeStart < 60) and (0 <= rangeEnd < 60):
            for value in range(rangeStart, rangeEnd+1):
                values += str(value) + " "
            return values

        self.setInvalid()
        return None

class dayOfMonthCronArgument(cronArgument):

    def __init__(self, arg):
        """
        Constructor. Defines type of cron argument.
        """
        super().__init__(arg)

        # Wildcard type
        if self.cronType == self.cronTypes[1]:
            self.printableValue = self.parseWildcard()

        # Single type
        if self.cronType == self.cronTypes[2]:
            self.printableValue = self.parseSingle()

        # Values type
        if self.cronType == self.cronTypes[3]:
            self.printableValue = self.parseValues()

        # Range type
        if self.cronType == self.cronTypes[4]:
            self.printableValue = self.parseRange()

        # Invalid type (such as interval for hour)
        if self.cronType == self.cronTypes[0] or self.cronType == self.cronTypes[5]:
            self.setInvalid()

    def parseWildcard(self) -> str:
        """
        Parses a wildcard for the minute cron argument
        :return:
        A string with all the numbers representing a minute within the hour: 1-59
        """

        values:str = ""

        for i in range(1,32):
            values += str(i) + ' '

        return values

    def parseSingle(self) -> str:
        """
        Converts cron single minute argument to a string of active minutes
        :return:
        String with length=1 OR 2 of minute in which cron will take place
        """

        value:str = ""

        if 0 < self.value < 32:
            value = str(self.value)
            return value

        self.setInvalid()
        # return value

    def parseValues(self) -> str:
        """
        Returns a list with values given via cron argument.
        Please note that there may be duplicated values, this is acceptable by crontab guru - https://crontab.guru/#3,4,1,3_0_*_8_*.
        :return:
        String with range of values given.
        """

        values:str = ""

        for value in self.value:
            # Check that it is in range
            if 0 < value < 32:
                # Check that numbers only exist once
                if values.find(str(value)) == -1:
                    values += str(value) + ' '
            else:
                self.setInvalid()

        return values

    def parseRange(self) -> str:
        """
        Parses a range or given values
        :param arg:
        :return:
        String of cron arguments seperated by spaces.
        Returns none if this is an invalid cron argument.
        """

        values:str = ""
        rangeStart = self.value[0]
        rangeEnd = self.value[1]

        # Check beginning of range is smaller than ending and range is correct
        if (rangeStart < rangeEnd) and (0 < rangeStart < 32) and (0 < rangeEnd < 32):
            for value in range(rangeStart, rangeEnd+1):
                values += str(value) + " "
            return values

        self.setInvalid()
        return None

class monthCronArgument(cronArgument):

    def __init__(self, arg):
        """
        Constructor. Defines type of cron argument.
        """
        super().__init__(arg)

        # Wildcard type
        if self.cronType == self.cronTypes[1]:
            self.printableValue = self.parseWildcard()

        # Single type
        if self.cronType == self.cronTypes[2]:
            self.printableValue = self.parseSingle()

        # Values type
        if self.cronType == self.cronTypes[3]:
            self.printableValue = self.parseValues()

        # Range type
        if self.cronType == self.cronTypes[4]:
            self.printableValue = self.parseRange()

        # Invalid type (such as interval for hour)
        if self.cronType == self.cronTypes[0] or self.cronType == self.cronTypes[5]:
            self.setInvalid()

    def parseWildcard(self) -> str:
        """
        Parses a wildcard for the minute cron argument
        :return:
        A string with all the numbers representing a minute within the hour: 1-59
        """

        values:str = ""

        for i in range(1,13):
            values += str(i) + ' '

        return values

    def parseSingle(self) -> str:
        """
        Converts cron single minute argument to a string of active minutes
        :return:
        String with length=1 OR 2 of minute in which cron will take place
        """

        value:str = ""

        if 0 < self.value < 13:
            value = str(self.value)
            return value

        self.setInvalid()
        # return value

    def parseValues(self) -> str:
        """
        Returns a list with values given via cron argument.
        Please note that there may be duplicated values, this is acceptable by crontab guru - https://crontab.guru/#3,4,1,3_0_*_8_*.
        :return:
        String with range of values given.
        """

        values:str = ""

        for value in self.value:
            # Check that it is in range
            if 0 < value < 13:
                # Check that numbers only exist once
                if values.find(str(value)) == -1:
                    values += str(value) + ' '
            else:
                self.setInvalid()

        return values

    def parseRange(self) -> str:
        """
        Parses a range or given values
        :param arg:
        :return:
        String of cron arguments seperated by spaces.
        Returns none if this is an invalid cron argument.
        """

        values:str = ""
        rangeStart = self.value[0]
        rangeEnd = self.value[1]

        # Check beginning of range is smaller than ending and range is correct
        if (rangeStart < rangeEnd) and (0 < rangeStart < 13) and (0 < rangeEnd < 13):
            for value in range(rangeStart, rangeEnd+1):
                values += str(value) + " "
            return values

        self.setInvalid()
        return None

class dayOfWeekCronArgument(cronArgument):

    def __init__(self, arg):
        """
        Constructor. Defines type of cron argument.
        """
        super().__init__(arg)

        # Wildcard type
        if self.cronType == self.cronTypes[1]:
            self.printableValue = self.parseWildcard()

        # Single type
        if self.cronType == self.cronTypes[2]:
            self.printableValue = self.parseSingle()

        # Values type
        if self.cronType == self.cronTypes[3]:
            self.printableValue = self.parseValues()

        # Range type
        if self.cronType == self.cronTypes[4]:
            self.printableValue = self.parseRange()

        # Invalid type (such as interval for hour)
        if self.cronType == self.cronTypes[0] or self.cronType == self.cronTypes[5]:
            self.setInvalid()

    def parseWildcard(self) -> str:
        """
        Parses a wildcard for the minute cron argument
        :return:
        A string with all the numbers representing a minute within the hour: 1-59
        """

        days = [1,2,3,4,5,6]
        values:str = ""

        for i in days:
            values += str(i) + ' '

        return values

    def parseSingle(self) -> str:
        """
        Converts cron single minute argument to a string of active minutes
        :return:
        String with length=1 OR 2 of minute in which cron will take place
        """

        value:str = ""

        if 0 <= self.value < 7:
            value = str(self.value)
            return value

        self.setInvalid()
        # return value

    def parseValues(self) -> str:
        """
        Returns a list with values given via cron argument.
        Please note that there may be duplicated values, this is acceptable by crontab guru - https://crontab.guru/#3,4,1,3_0_*_8_*.
        :return:
        String with range of values given.
        """

        values:str = ""

        for value in self.value:
            # Check that it is in range
            if 0 <= value < 7:
                # Check that numbers only exist once
                if values.find(str(value)) == -1:
                    values += str(value) + ' '
            else:
                self.setInvalid()

        return values

    def parseRange(self) -> str:
        """
        Parses a range or given values
        :return:
        String of cron arguments separated by spaces.
        Returns none if this is an invalid cron argument.
        """

        values:str = ""
        rangeStart = self.value[0]
        rangeEnd = self.value[1]

        # Check beginning of range is smaller than ending and range is correct
        if (rangeStart < rangeEnd) and (0 <= rangeStart < 7) and (0 <= rangeEnd < 7):
            for value in range(rangeStart, rangeEnd+1):
                values += str(value) + " "
            return values

        self.setInvalid()
        return None