import csv
import unittest
import os

from archiver import save_to_csv
from test_data.sample_transactions_1 import test_transactions

class TestWriteCSV(unittest.TestCase):
    def setUp(self):
        self.test_filename = "test_transactions/user_token/transfers/transactions-22563621-22563713.csv"

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_write_to_csv(self):
        save_to_csv(self.test_filename, test_transactions)
        assert os.path.exists(self.test_filename)

    # Extra tests (ran out of time?):
    # -Check content integrity
    # -Check encoding errors are handled gracefully
    # -Check overwrite behavior works as expected
    # -Handle aioetherscan client errors gracefully
