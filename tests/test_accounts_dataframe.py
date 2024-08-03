# test_accounts_dataframe.py
import unittest
import pandas as pd

from io                      import StringIO
from unittest.mock           import patch, mock_open
from data.accounts_dataframe import AccountsDataFrame


class TestAccountsDataFrame(unittest.TestCase):

    @patch('os.path.exists', return_value=True)
    @patch('pandas.read_csv')
    def setUp(self, mock_read_csv, mock_exists):
        self.mock_df = pd.DataFrame({
            'Numero de Cuenta': ['123', '456'],
            'Nombre': ['Alice', 'Bob']
        })
        mock_read_csv.return_value = self.mock_df
        self.accounts_df = AccountsDataFrame()

    @patch('os.path.exists', return_value=False)
    def test_init_file_not_found(self, mock_exists):
        with self.assertRaises(FileNotFoundError):
            AccountsDataFrame()

    def test_add_account(self):
        new_account = {'Numero de Cuenta': '789', 'Nombre': 'Charlie'}
        self.accounts_df.add(new_account)
        self.assertIn('789', self.accounts_df._df['Numero de Cuenta'].values)

    def test_add_duplicate_account(self):
        duplicate_account = {'Numero de Cuenta': '123', 'Nombre': 'Alice'}
        with self.assertRaises(ValueError):
            self.accounts_df.add(duplicate_account)

    def test_get_account(self):
        account = self.accounts_df.get('123')
        self.assertEqual(account['Nombre'], 'Alice')

    def test_get_nonexistent_account(self):
        with self.assertRaises(ValueError):
            self.accounts_df.get('999')

    def test_remove_account(self):
        self.accounts_df.remove('123')
        self.assertNotIn('123', self.accounts_df._df['Numero de Cuenta'].values)

    def test_remove_nonexistent_account(self):
        with self.assertRaises(ValueError):
            self.accounts_df.remove('999')

    def test_edit_account(self):
        new_data = {'Numero de Cuenta': '123', 'Nombre': 'Alice Updated'}
        self.accounts_df.edit('123', new_data)
        self.assertEqual(self.accounts_df.get('123')['Nombre'], 'Alice Updated')

    def test_edit_nonexistent_account(self):
        new_data = {'Numero de Cuenta': '999', 'Nombre': 'Nonexistent'}
        with self.assertRaises(ValueError):
            self.accounts_df.edit('999', new_data)

    def test_search(self):
        results = self.accounts_df.search('Alice')
        self.assertEqual(len(results), 1)
        self.assertEqual(results.iloc[0]['Nombre'], 'Alice')

    @patch('pandas.DataFrame.to_csv')
    def test_export_to_csv(self, mock_to_csv):
        self.accounts_df.export_to_csv('export.csv')
        mock_to_csv.assert_called_once_with('export.csv', index=False)

    def test_columns_property(self):
        self.assertEqual(self.accounts_df.columns, ['Numero de Cuenta', 'Nombre'])

    def test_rows_property(self):
        rows = list(self.accounts_df.rows)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['Nombre'], 'Alice')

if __name__ == '__main__':
    unittest.main()
    