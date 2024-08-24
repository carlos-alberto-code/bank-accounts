Desarrollé esta aplicación para un cliente que efectúa depósitos a diferentes cuentas bancarias. El propósito fue facilitar la búsqueda de las cuentas de un determinado cliente, y poder copiar y pegar rápidamente en un sitio web la cuenta a la que se efectuaría el depósito.
La aplicación está desarrollada en Python, y usa tecnologías como pandas para el acceso a un archivo, y flet para la interfaz gráfica.

# Arquitectura

Aunque es una aplicación liviana, separar en diferentes capas sigue siendo beneficioso. En esta aplicación la capa más baja se encarga de la interacción con el archivo csv por medio de pandas.
Una capa superior se encarga de comunicarse con la interfaz gráfica y con la clase que interactúa con pandas, todo esto en un pequeño controlador.
La capa gráfica es en esa aplicación la que más código necesito. Hay una clase que hereda de ``ft.DataTable`` y que maneja la presentación de los datos recibidos en el controlador por la capa de negocio.
En otros archivos se manejan los eventos y otros pequeños componentes.
