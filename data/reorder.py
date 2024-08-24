import pandas as pd

df = pd.read_csv('data/accounts.csv')
df = df[['Nombres', 'Apellido Paterno', 'Apellido Materno', 'Numero de Cuenta']]
df.to_csv('data/accounts.csv', index=False)
