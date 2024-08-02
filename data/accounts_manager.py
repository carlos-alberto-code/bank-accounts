from typing         import List
from data.accounts_dataframe  import AccountsDataFrame
from dataclasses    import dataclass

@dataclass
class Customer:
    paternal_surname: str
    maternal_surname: str
    names: str
    account_number: str

class AccountsManager:

    def __init__(self) -> None:
        self.accounts = AccountsDataFrame()

    def add_customer(self, customer: Customer) -> None:
        account_data = {
            'Apellido Paterno': customer.paternal_surname,
            'Apellido Materno': customer.maternal_surname,
            'Nombres': customer.names,
            'Numero de Cuenta': customer.account_number
        }
        self.accounts.add(account_data)

    def remove_customer(self, account_number: str) -> None:
        self.accounts.remove(account_number)

    def get_total_customers(self) -> int:
        return self.accounts.total_accounts

    def get_column_names(self) -> List[str]:
        return self.accounts.column_names

    def search(self, search_term: str) -> List[Customer]:
        search_results = self.accounts.search(search_term)
        return [Customer(row['Apellido Paterno'], row['Apellido Materno'], row['Nombres'], row['Numero de Cuenta']) for _, row in search_results.iterrows()]
