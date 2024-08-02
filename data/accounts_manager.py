from typing                   import List
from dataclasses              import dataclass
from data.accounts_dataframe  import AccountsDataFrame

@dataclass
class Customer:
    apellido_paterno: str
    apellido_materno: str
    nombres: str
    numero_de_cuenta: str

class AccountsManager:

    def __init__(self) -> None:
        self._accounts = AccountsDataFrame()

    def add(self, customer: Customer) -> None:
        account_data = {
            'Apellido Paterno': customer.apellido_paterno,
            'Apellido Materno': customer.apellido_materno,
            'Nombres': customer.nombres,
            'Numero de Cuenta': customer.numero_de_cuenta
        }
        self._accounts.add(account_data)
    
    def get(self):
        pass

    def get_all(self) -> List[Customer]:
        return [Customer(row['Apellido Paterno'], row['Apellido Materno'], row['Nombres'], row['Numero de Cuenta']) for _, row in self._accounts.rows]

    def remove(self, account_number: str) -> None:
        self._accounts.remove(account_number)

    @property
    def columns(self) -> List[str]:
        return self._accounts.columns

    def search(self, search_term: str) -> List[Customer]:
        search_results = self._accounts.search(search_term)
        return [Customer(row['Apellido Paterno'], row['Apellido Materno'], row['Nombres'], row['Numero de Cuenta']) for _, row in search_results.iterrows()]
