import sys #este nos permitira comprobar los argumentos que enviamos al script al ejecutarlo

DATABASE_PATH = "clientes.csv" 
if "pytest" in sys.argv[0]:
    DATABASE_PATH = "tests/clientes_test.csv" 