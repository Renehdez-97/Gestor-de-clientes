## Gestor de Clientes con Tkinter

Este proyecto ofrece una interfaz gráfica en Tkinter para gestionar clientes de manera sencilla. Permite agregar, modificar y eliminar clientes con validaciones en tiempo real para los campos de DNI, nombre y apellido. Los datos se almacenan en un archivo CSV, y se utilizan pruebas unitarias con pytest para garantizar que todas las funciones de la interfaz gráfica trabajen correctamente. Ideal para usuarios que prefieren una aplicación de escritorio simple para gestionar información de clientes.


## Instalar las dependencias

_Nota: Sólo incluye pytest para realizar pruebas unitarias._

```bash
pip install -r requirements.txt
```

## Para probar el programa en modo gráfico

```bash
python run.py
```

## Para probar el programa en modo terminal

```bash
python run.py -t
```

## Para ejecutar las pruebas unitarias

```bash
pytest -v
```
