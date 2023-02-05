from main import Transaction
import unittest

class Testmain(unittest.TestCase):
    def setUp(self):
        self.transaction = Transaction("2019-08-26T10:50:58.294041", "Перевод организации", "Maestro 1596837868705199", "Счет 64686473678894779589", "31957.58", "руб.")

    def test_blur_from(self):
        self.assertEqual(self.transaction.blur_from(), 'Maestro 1596 83** **** 5199')

    def test_blur_to(self):
        self.assertEqual(self.transaction.blur_to(), 'Счет **** **** **** **** 9589')

    def test_get_date(self):
        self.assertEqual(self.transaction.get_date(), '2019-08-26')

    def test_info(self):
        self.assertEqual(self.transaction.info(), '2019-08-26 Перевод организации\nMaestro 1596 83** **** 5199 -> Счет **** **** **** **** 9589\n31957.58 руб.\n')







