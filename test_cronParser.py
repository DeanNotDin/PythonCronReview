import unittest
import cronParser as cp

# Checkup values
wildcard = '*'
arg = "* * * * * echo Hello World!"

class TestPCRMinute(unittest.TestCase):
    single = [[1], [5], [10], [15], [30], [60], [100], [-5], ['1'], ['five'], ['daily']]
    interval = '*/5'

    # def setUp(self) -> None:

    def test_wildcard_validity(self):
        self.assertTrue(cp.minuteCronArgument(wildcard))

    def test_wildcard_output(self):
        expectedOutput = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 "
        self.assertEqual(cp.minuteCronArgument('*').getPrintableValue(), expectedOutput)

    def test_single_validity(self):
        for value in self.single:
            self.assertTrue(cp.minuteCronArgument(self.single))

class TestPCRHour(unittest.TestCase):

    def test_wildcard_validity(self):
        self.assertTrue(cp.hourCronArgument(wildcard))

    def test_wildcard_output(self):
        expectedOutput = "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 "
        self.assertEqual(cp.hourCronArgument('*').getPrintableValue(), expectedOutput)

class TestPCRMonth(unittest.TestCase):
    def test_wildcard_validity(self):
        self.assertTrue(cp.monthCronArgument(wildcard))

    def test_wildcard_output(self):
        expectedOutput = "1 2 3 4 5 6 7 8 9 10 11 12 "
        self.assertEqual(cp.monthCronArgument('*').getPrintableValue(), expectedOutput)


class TestPCRDayOfWeek(unittest.TestCase):
    def test_wildcard_validity(self):
        self.assertTrue(cp.dayOfWeekCronArgument(wildcard))

    def test_wildcard_output(self):
        expectedOutput = "1 2 3 4 5 6 "
        self.assertEqual(cp.dayOfWeekCronArgument('*').getPrintableValue(), expectedOutput)

class TestPCRDayOfMonth(unittest.TestCase):
    def test_wildcard_validity2(self):
        self.assertTrue(cp.dayOfMonthCronArgument(wildcard))

    def test_wildcard_output(self):
        expectedOutput = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 "
        self.assertEqual(cp.dayOfMonthCronArgument('*').getPrintableValue(), expectedOutput)

if __name__ == '__main__':
    unittest.main()