import sys
from cronParser import *

def processArgs() -> list[str]:
    """
    Process arguments given to the application
    :return:
    Commands entered as arguments
    """
    args = sys.argv[1:]
    cronCommand = args[0].split(" ")

    return cronCommand

def initCronParser(cronCommand) -> dict:
    """
    Initialize CronArgument objects to process cron commands using custom logic from cronParser.py
    :param cronCommand:
    Cron command given as argument to the application
    :return:
    Dictionary with the runtime description of cron command
    """

    # Concat shell command
    command = ""
    for item in cronCommand[5:]:
        command += item + ' '

    # Create dictionary
    cronValues = {
        'Minute': minuteCronArgument(cronCommand[0]).getPrintableValue(),
        'Hour': hourCronArgument(cronCommand[1]).getPrintableValue(),
        'DayOfMonth': dayOfMonthCronArgument(cronCommand[2]).getPrintableValue(),
        'Month': monthCronArgument(cronCommand[3]).getPrintableValue(),
        'DayOfWeek': dayOfWeekCronArgument(cronCommand[4]).getPrintableValue(),
        'Command': command
    }

    return cronValues

def composePrintString(cronValues) -> str:
    """
    Concat strings to a single string for easy printing to CLI
    :param cronValues:
    Parsed Cron values
    :return:
    String containing cron runtime information
    """
    output = ""
    output += 'minute\t' + cronValues['Minute'] + '\n'
    output += 'hour\t' + cronValues['Hour'] + '\n'
    output += 'day of month\t' + cronValues['DayOfMonth'] + '\n'
    output += 'month\t' + cronValues['Month'] + '\n'
    output += 'day of week\t' + cronValues['DayOfWeek'] + '\n'
    output += 'command\t' + cronValues['Command']

    return output

# Main function
if __name__ == '__main__':

    # Check that the correct number of arguments was given
    if len(sys.argv) >= 2:
        # Parse arguments into cron attributes
        commands = processArgs()
        # Parse cron extended runtime information to a dictionary
        cronData = initCronParser(commands)
        # Parse dictionary into string for easy CLI printing
        print(composePrintString(cronData))

    # Exit with error code
    else:
        print("Please input whole CRON argument, including a command.")
        raise RuntimeError("Please enter the correct number of arguments!")
        exit(1)