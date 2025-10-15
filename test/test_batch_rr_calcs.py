"""
Unit tests for the batch_rr_calcs library
"""

from daamsim import batch_rr_calcs

class TestBatchRrCalcs:

    def test_batch_rr_calcs():
        assert [5, 15, 25] == batch_rr_calcs(5, 25, 10)