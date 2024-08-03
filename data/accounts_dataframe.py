import os
import pandas as pd
import threading
from typing import Dict, List, Generator

class AccountsDataFrame:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(AccountsDataFrame, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._filepath = 'data/accounts.csv'
            if not os.path.exists(self._filepath):
                raise FileNotFoundError(f"Archivo no encontrado en el directorio: {self._filepath}\n")
            self._df = pd.read_csv(self._filepath)
            self._initialized = True

    def add(self, account_data: Dict[str, str]) -> None:
        with self._lock:
            if not all(key in account_data for key in self._df.columns):
                raise ValueError("Datos de cuenta incompletos")
            if account_data['Numero de Cuenta'] in self._df['Numero de Cuenta'].astype(str).values:
                raise ValueError(f"Numero de Cuenta: {account_data['Numero de Cuenta']} ya existe en la base de datos\n")
            self._df.loc[len(self._df)] = pd.Series(account_data)
            self._save_to_csv()
    
    def get(self, account_number: str) -> pd.Series:
        with self._lock:
            self._df['Numero de Cuenta'] = self._df['Numero de Cuenta'].astype(str)
            if account_number not in self._df['Numero de Cuenta'].values:
                raise ValueError(f"Numero de Cuenta: {account_number} no existe en la base de datos\n")
            return self._df[self._df['Numero de Cuenta'] == account_number].iloc[0]

    def remove(self, account_number: str) -> None:
        with self._lock:
            self._df['Numero de Cuenta'] = self._df['Numero de Cuenta'].astype(str)
            if account_number not in self._df['Numero de Cuenta'].values:
                raise ValueError(f"Numero de Cuenta: {account_number} no existe en la base de datos\n")
            self._df = self._df[self._df['Numero de Cuenta'] != account_number]
            self._save_to_csv()
            if account_number in self._df['Numero de Cuenta'].values:
                raise RuntimeError(f"Error al eliminar el Numero de Cuenta: {account_number}")

    def _save_to_csv(self) -> None:
        with self._lock:
            self._df.to_csv(self._filepath, index=False)
    
    def export_to_csv(self, filepath: str) -> None:
        with self._lock:
            self._df.to_csv(filepath, index=False)

    def search(self, search_term: str) -> pd.DataFrame:
        with self._lock:
            search_results = self._df[self._df.apply(lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(), axis=1)]
            return search_results
    
    @property
    def columns(self) -> List[str]:
        with self._lock:
            return list(self._df.columns)
    
    @property
    def rows(self) -> Generator[pd.Series, None, None]:
        with self._lock:
            return (row for _, row in self._df.iterrows())
