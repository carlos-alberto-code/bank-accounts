import threading
import re

from typing import List, Tuple
from dataclasses import dataclass
from data.accounts_dataframe import AccountsDataFrame

@dataclass
class Customer:
    apellido_paterno: str
    apellido_materno: str
    nombres: str
    numero_de_cuenta: str

    @property
    def full_name(self) -> str:
        return f"{self.nombres.capitalize()} {self.apellido_paterno.capitalize()} {self.apellido_materno.capitalize()}"

class AccountsManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(AccountsManager, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._accounts = AccountsDataFrame()
            self._initialized = True
    
    def add(self, customer: Customer) -> None:
        customer = self._normalize_customer(customer)
        valid, error_message = self._validate_customer(customer)
        if not valid:
            raise ValueError(f"Datos del cliente no válidos: {error_message}")

        account_data = {
            'Apellido Paterno': customer.apellido_paterno,
            'Apellido Materno': customer.apellido_materno,
            'Nombres': customer.nombres,
            'Numero de Cuenta': customer.numero_de_cuenta
        }
        try:
            self._accounts.add(account_data)
        except ValueError as e:
            raise ValueError(f"Error al agregar la cuenta: {str(e)}")

    def get(self, account_number: str) -> Customer:
        try:
            row = self._accounts.get(account_number)
            return Customer(row['Apellido Paterno'], row['Apellido Materno'], row['Nombres'], row['Numero de Cuenta'])
        except ValueError as e:
            raise ValueError(f"Error al obtener la cuenta: {str(e)}")

    def get_all(self) -> List[Customer]:
        return [
            Customer(row['Apellido Paterno'], row['Apellido Materno'], row['Nombres'], row['Numero de Cuenta'])
            for row in self._accounts.rows
        ]

    def remove(self, account_number: str) -> None:
        try:
            self._accounts.remove(account_number)
        except ValueError as e:
            raise ValueError(f"Error al eliminar la cuenta: {str(e)}")

    @property
    def columns(self) -> List[str]:
        return self._accounts.columns

    def search(self, search_term: str) -> List[Customer]:
        search_results = self._accounts.search(search_term)
        return [Customer(row['Apellido Paterno'], row['Apellido Materno'], row['Nombres'], row['Numero de Cuenta']) for _, row in search_results.iterrows()]

    def update(self, account_number: str, updated_customer: Customer) -> None:
        updated_customer = self._normalize_customer(updated_customer)
        valid, error_message = self._validate_customer(updated_customer)
        if not valid:
            raise ValueError(f"Datos del cliente no válidos: {error_message}")

        updated_data = {
            'Apellido Paterno': updated_customer.apellido_paterno,
            'Apellido Materno': updated_customer.apellido_materno,
            'Nombres': updated_customer.nombres,
            'Numero de Cuenta': updated_customer.numero_de_cuenta
        }
        try:
            self._accounts.edit(account_number, updated_data)
        except ValueError as e:
            raise ValueError(f"Error al actualizar la cuenta: {str(e)}")

    def _validate_customer(self, customer: Customer) -> Tuple[bool, str]:
        def is_valid_length(field: str, min_length: int, max_length: int) -> Tuple[bool, str]:
            if not (min_length <= len(field) <= max_length):
                return False, f"{field} debe tener entre {min_length} y {max_length} caracteres."
            return True, ""
        
        def is_alpha_space(field: str) -> Tuple[bool, str]:
            if not re.match(r'^[a-zA-Z\s]+$', field):
                return False, f"{field} solo puede contener letras y espacios."
            return True, ""
        
        def is_valid_account_number(account_number: str) -> Tuple[bool, str]:
            if not re.match(r'^\d{5,50}$', account_number):
                return False, "El número de cuenta debe tener entre 5 y 50 dígitos."
            return True, ""
    
        checks = [
            is_valid_account_number(customer.numero_de_cuenta),
            is_valid_length(customer.apellido_paterno, 2, 30),
            is_valid_length(customer.apellido_materno, 2, 30),
            is_valid_length(customer.nombres, 2, 30),
            is_alpha_space(customer.apellido_paterno),
            is_alpha_space(customer.apellido_materno),
            is_alpha_space(customer.nombres),
        ]

        for valid, error_message in checks:
            if not valid:
                return False, error_message
        return True, ""

    def _normalize_customer(self, customer: Customer) -> Customer:
        customer.apellido_paterno = self._capitalize_words(customer.apellido_paterno)
        customer.apellido_materno = self._capitalize_words(customer.apellido_materno)
        customer.nombres = self._capitalize_words(customer.nombres)
        return customer

    def _capitalize_words(self, text: str) -> str:
        return ' '.join(word.capitalize() for word in text.split())
