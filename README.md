#<b>Python Cron Review (PCR)</b>
###About
This is a small python project that parses cron commands given as arguments and extends it to actual runtime information.
This is very useful for reviewing cron commands prior to using them on a server.

##Requirements
This script was written in Python 3.9 but should run without issue on all Python3 versions.

## Installation
1. Clone this repo using the following command:
`git clone https://github.com/deannotdin/PythonCronReview.git`
2. cd PythonCodeReview

## Usage
1. Run `./PCR "*/5 4-8 1,2,3 12 * echo hello world!"`
2. <b>Profit!</b>

## Known issues:

1. Days of the week can only be entered as a numerical value and not with short day name (such as SUN for sunday)
2. Does not accept year values (not supported in all cron implementations)
3. Weekdays are only accepted between 0-6. 7 isn't accepted, although it isn't accepted in all cron implementations.

## Nice to have features:
1. Sorting a given set of numbers separated by a comma.
2. Add written text support for verification of months and days. For example, accepting DEC as the 12th month.

## Remarks:
4. I did not use PEP8 convention. Instead, I used some of my best practices. I have to problem adapting to any convention.
5. OOP could have been better written given more time.
   1. One example for that would be avoiding calling self.setInvalid() in cronParser.py and change logics to return INVALID even after a positive regex match, but with values that are invalid.
   2. Another example would be 