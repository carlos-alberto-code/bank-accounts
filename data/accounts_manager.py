from typing                   import List
from dataclasses              import dataclass
from data.accounts_dataframe  import AccountsDataFrame

@dataclass
class Customer:
    paternal_surname: str
    maternal_surname: str
    names: str
    account_number: str

class AccountsManager:

    def __init__(self) -> None:
        self._accounts = AccountsDataFrame()

    def add(self, customer: Customer) -> None:
        account_data = {
            'Apellido Paterno': customer.paternal_surname,
            'Apellido Materno': customer.maternal_surname,
            'Nombres': customer.names,
            'Numero de Cuenta': customer.account_number
        }
        self._accounts.add(account_data)

    def remove(self, account_number: str) -> None:
        self._accounts.remove(account_number)

    @property
    def columns(self) -> List[str]:
        return self._accounts.columns

    def search(self, search_term: str) -> List[Customer]:
        search_results = self._accounts.search(search_term)
        return [Customer(row['Apellido Paterno'], row['Apellido Materno'], row['Nombres'], row['Numero de Cuenta']) for _, row in search_results.iterrows()]
