"""
Unit tests for the batch_rr_calcs library
"""

from calculations.math_util import *


class TestMathUtil:

    def test_make_speed_array(self):
        assert [5, 15, 25] == make_array(5, 25, 10)
        try:
            make_array(35, 25, 10)
            assert False
        except Exception as e:
            assert isinstance(e, ValueError)

    def test_cosd(self):
        assert math.isclose(1, cosd(0))
        assert math.isclose(0, cosd(90))
        assert math.isclose(-1, cosd(180))

