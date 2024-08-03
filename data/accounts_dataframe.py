import os
import pandas as pd

class AccountsDataFrame:

    def __init__(self) -> None:
        self._filepath = 'data/accounts.csv'
        if not os.path.exists(self._filepath):
            raise FileNotFoundError(f"Archivo no encontrado en el directorio: {self._filepath}\n")
        self._df = pd.read_csv(self._filepath)

    def add(self, account_data: dict) -> None:
        if account_data['Numero de Cuenta'] in self._df['Numero de Cuenta'].astype(str).values:
            raise ValueError(f"Numero de Cuenta: {account_data['Numero de Cuenta']} ya existe en la base de datos\n")
        self._df.loc[len(self._df)] = pd.Series(account_data)
        self._save_to_csv()
    
    def get(self, account_number: str) -> pd.Series:
        self._df['Numero de Cuenta'] = self._df['Numero de Cuenta'].astype(str)
        if account_number not in self._df['Numero de Cuenta'].values:
            raise ValueError(f"Numero de Cuenta: {account_number} no existe en la base de datos\n")
        return self._df[self._df['Numero de Cuenta'] == account_number].iloc[0]

    def remove(self, account_number: str) -> None:
        self._df['Numero de Cuenta'] = self._df['Numero de Cuenta'].astype(str)
        if account_number not in self._df['Numero de Cuenta'].values:
            raise ValueError(f"Numero de Cuenta: {account_number} no existe en la base de datos\n")
        self._df = self._df[self._df['Numero de Cuenta'] != account_number]
        self._save_to_csv()

    def _save_to_csv(self) -> None:
        self._df.to_csv(self._filepath, index=False)
    
    def export_to_csv(self, filepath: str) -> None:
        self._df.to_csv(filepath, index=False)

    def search(self, search_term: str) -> pd.DataFrame:
        search_results = self._df[self._df.apply(lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(), axis=1)]
        return search_results
    
    @property
    def columns(self) -> list[str]:
        return list(self._df.columns)
    
    @property
    def rows(self):
        return self._df.iterrows()
