from django.test import SimpleTestCase

from app.play_numbers import add_numbers, substract_numbers, multiplier_numbers


class CalcTests(SimpleTestCase):

    def test_add_number(self):
        res = add_numbers(3, 2)
        self.assertEqual(res, 5)

    def test_substract_number(self):
        res = substract_numbers(5, 2)
        self.assertEqual(res, 3)

    def test_multiplier_number(self):
        res = multiplier_numbers(2, 2)
        self.assertEqual(res, 4)
