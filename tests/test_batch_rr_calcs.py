"""
Unit tests for the batch_rr_calcs library
"""

from calculations.batch_rr_calcs import make_speed_array


class TestBatchRrCalcs:

    def test_make_speed_array(self):
        assert [5, 15, 25] == make_speed_array(5, 25, 10)
        try:
            make_speed_array(35, 25, 10)
            assert False
        except Exception as e:
            assert isinstance(e, ValueError)

