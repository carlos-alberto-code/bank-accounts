import os
import pandas as pd
from unidecode import unidecode
from typing import Dict, List, Generator

class AccountsDataFrame:
    _instance = None

    def __new__(cls, *args, **kwargs):
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
        if not all(key in account_data for key in self._df.columns):
            raise ValueError("Datos de cuenta incompletos")
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
        if account_number in self._df['Numero de Cuenta'].values:
            raise RuntimeError(f"Error al eliminar el Numero de Cuenta: {account_number}")

    def edit(self, account_number: str, new_data: Dict[str, str]) -> None:
        self._df['Numero de Cuenta'] = self._df['Numero de Cuenta'].astype(str)
        if account_number not in self._df['Numero de Cuenta'].values:
            raise ValueError(f"Numero de Cuenta: {account_number} no existe en la base de datos\n")
        index = self._df.index[self._df['Numero de Cuenta'] == account_number].tolist()[0]
        if not all(key in new_data for key in self._df.columns):
            raise ValueError("Datos de cuenta incompletos")
        self._df.loc[index] = pd.Series(new_data)
        self._save_to_csv()
    
    def _save_to_csv(self) -> None:
        try:
            self._df.to_csv(self._filepath, index=False)
        except Exception as e:
            print(f"Error al guardar en CSV: {e}")

    def export_to_csv(self, filepath: str) -> None:
        self._df.to_csv(filepath, index=False)

    def search(self, search_term: str) -> pd.DataFrame:
        def normalize_text(text: str) -> str:
            return unidecode(text).lower()
        
        normalized_search_term = normalize_text(search_term)
        search_results = self._df[self._df.apply(
            lambda row: row.astype(str).apply(normalize_text).str.contains(normalized_search_term, na=False).any(),
            axis=1
        )]
        return search_results
    
    @property
    def columns(self) -> List[str]:
        return list(self._df.columns)
    
    @property
    def rows(self) -> Generator[pd.Series, None, None]:
        return (row for _, row in self._df.iterrows())
