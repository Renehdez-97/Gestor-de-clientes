import database as db
import helpers
from tkinter import*
from tkinter import ttk #widgets extendidos

from tkinter.messagebox import askokcancel, WARNING

class CenterWidgetMixin:
    def center (self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int(ws/2 - w/2)
        y = int(hs/2 - h/2)
        self.geometry(f"{w}x{h}+{x}+{y}") #ESTAS SON LAS ALTURAS QUE MODIFICARE WIDTHxHEIGHT+OFFSET_X+OFFSET_Y

class CreateClientWindow(Toplevel, CenterWidgetMixin): #widget que maneja las subventanas
    def __init__(self, parent): #el parametro parent es el padre de la subventana
        super().__init__(parent)
        self.title("Crear Cliente")
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set() #este impedira que interaccionemos con la ventana principal, en conjunto con transient 

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)
        Label(frame, text='DNI(1 upper chars y 3 ints)').grid(row=0, column=0)
        Label(frame, text='Nombre(2-30 chars)').grid(row=0, column=1)
        Label(frame, text='Apellido(2-30 chars)').grid(row=0, column=2)

        dni = Entry(frame) #el widjet es Entry y lo creamos en el frame
        dni.grid(row=1, column=0)
        dni.bind("<KeyRelease>", lambda event: self.validate(event, 0))
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 1))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 2))

        frame = Frame(self)
        frame.pack(pady=10)

        crear = Button(frame, text="Crear", command=self.create_client)
        crear.configure(state=DISABLED)
        crear.grid(row=0, column=0)
        Button(frame, text='Cancelar', command=self.close).grid(row=0,column=1)

        self.validaciones = [0, 0, 0] #se crea una lista para cada campo inicialmente, para el boton de crear clientes
        self.crear = crear #aqui exportamos el boton de crear a nivel de instancia para reutilizarlo
        self.dni = dni            #este
        self.nombre = nombre      #este
        self.apellido = apellido  #y este son los 3 campos que se exportaron

    def create_client(self):
        self.master.treeview.insert( #master es el padre de la subventana, la ventana principal
                parent='', index='end', iid=self.dni.get(), #utilizamos su metodo .get() se pone al final, para recuperar el texto, porque son campos de texto, son entrys
                values=(self.dni.get(), self.nombre.get(), self.apellido.get())  
            )
                #^anteriormenre todo lo de self, estaba con un cliente. dni, cliente.nombre, etc, y fue sustituido por un self, porque se han asignado, se han exportado los 3 campos de texto.
        db.Clientes.crear(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close() #llamamos al metodo close para destruir la subventana y agregar antes la informacion

    def close(self):
        self.destroy() #destruimos ua ventana
        self.update() #para actualizar la informacion interna

    def validate(self, event, index):
        valor = event.widget.get() #utilizo el metodo get() para recuperar su contenido y con esto el texto que hay dentro
        #if index==0:
        #    valido = helpers.validar_dni(valor, db.Clientes.lista)
        #    if valido:
        #        event.widget.configure({"bg":"Green"})
        #    else:
        #        event.widget.configure({"bg":"Red"})

        #if index==1:
        #    valido = valor.isalpha() and len(valor) >= 2 and len(valor)<=30
        #    if valido:
        #        event.widget.configure({"bg":"Green"})
        #    else:
        #        event.widget.configure({"bg":"Red"})

        #if index==2:
        #    valido = valor.isalpha() and len(valor) >= 2 and len(valor)<=30
        #    if valido:
        #        event.widget.configure({"bg":"Green"})
        #    else:
        #        event.widget.configure({"bg":"Red"})
        #TODO LO ANTERIOR PUEDE SER SUSTITUIDO POR:

        valido = helpers.validar_dni(valor, db.Clientes.lista) if index==0 else (valor.isalpha() and len(valor) >= 2 and len(valor)<=30) 
        event.widget.configure({"bg":"Green" if valido else "Red"})

        #Cambiar el estado del boton en base a las validaciones
        self.validaciones[index] = valido
        self.crear.config(state=NORMAL if self.validaciones==[1,1,1] else DISABLED) #operador ternario, el estado será activado(NORMAL), si todas las validaciones son verdaderas (1,1,1), en caso contrario cambiara a DISABLED.

class EditClientWindow(Toplevel, CenterWidgetMixin): #widget que maneja las subventanas
    def __init__(self, parent): #el parametro parent es el padre de la subventana
        super().__init__(parent)
        self.title("Actualizar Cliente")
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set() #este impedira que interaccionemos con la ventana principal, en conjunto con transient 

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)
        Label(frame, text='DNI(no editable)').grid(row=0, column=0)
        Label(frame, text='Nombre(2-30 chars)').grid(row=0, column=1)
        Label(frame, text='Apellido(2-30 chars)').grid(row=0, column=2)

        dni = Entry(frame) #el widjet es Entry y lo creamos en el frame
        dni.grid(row=1, column=0)
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 0))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 1))

        #despues de crar los campos, vamos a recuperar el cliente y los campos seleccionado en el treeview
        cliente = self.master.treeview.focus()
        campos = self.master.treeview.item(cliente, "values") #le pasaremos los clientes y que extraiga los values
        dni.insert(0, campos[0])
        dni.config(state=DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])

        frame = Frame(self)
        frame.pack(pady=10)

        actualizar = Button(frame, text="Actualizar", command=self.edit_client)
        
        actualizar.grid(row=0, column=0)
        Button(frame, text='Cancelar', command=self.close).grid(row=0,column=1)

        self.validaciones = [1, 1,] #solo se valida el nombre y apellido y por defecto van a ser TRUE [1,1], porque si estamos cargando un registro que ya existe, inicialmente es que estara validado 
        self.actualizar = actualizar #aqui exportamos el boton de crear a nivel de instancia para reutilizarlo
        self.dni = dni            #este
        self.nombre = nombre      #este
        self.apellido = apellido  #y este son los 3 campos que se exportaron

    def edit_client(self):
        cliente= self.master.treeview.focus()
        self.master.treeview.item(cliente, values=(self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.modificar(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close() #llamamos al metodo close para destruir la subventana y agregar antes la informacion

    def close(self):
        self.destroy() #destruimos ua ventana
        self.update() #para actualizar la informacion interna

    def validate(self, event, index):
        valor = event.widget.get() 

        valido = (valor.isalpha() and len(valor) >= 2 and len(valor)<=30) 
        event.widget.configure({"bg":"Green" if valido else "Red"})

        #Cambiar el estado del boton en base a las validaciones
        self.validaciones[index] = valido
        self.actualizar.config(state=NORMAL if self.validaciones==[1,1] else DISABLED)

class MainWindow (Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title ("Gestor de Clientes")
        self.build()
        self.center()

    def build (self):
        frame = Frame(self)
        frame.pack()
        
        #vamos a cargar unos widgets extendidos desde la libreria de tkinter

        treeview = ttk.Treeview(frame)
        treeview['columns'] = ['DNI', 'Nombre', 'Apellido']

        treeview.column("#0", width=0, stretch=NO)
        treeview.column("DNI", anchor=CENTER)
        treeview.column("Nombre", anchor=CENTER)
        treeview.column("Apellido", anchor=CENTER)

        treeview.heading("DNI", text='DNI', anchor=CENTER)
        treeview.heading("Nombre", text='Nombre', anchor=CENTER)
        treeview.heading("Apellido", text='Apellido', anchor=CENTER)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y) #con fill relleno verticalmente la barra poniendo Y)
        #Ahora tengo que decirle a treeview que utilice el scrollbar
       
        treeview['yscrollcommand'] = scrollbar.set

        for cliente in db.Clientes.lista:
            treeview.insert(
                parent='', index='end', iid=cliente.dni, 
                values=(cliente.dni, cliente.nombre, cliente.apellido)  
            )

        treeview.pack()

        frame = Frame(self)
        frame.pack(pady=20,)
        Button(frame, text='Crear', command=self.create).grid(row=0, column=0)
        Button(frame, text='Modificar', command=self.edit).grid(row=0, column=1)
        Button(frame, text='Borrar', command=self.delete).grid(row=0, column=2)

        #Vamos a estar accediendo a este treeview en estos metodos, por lo cual hay que exportarlo como un atributo de instancia, al poner un self, ya tenemos acceso a ese widget en los demas metodos
        self.treeview = treeview

    def delete(self):
        cliente = self.treeview.focus()
        if cliente:
            campos = self.treeview.item(cliente, 'values') #values extraera los valores del registro 'clientes' seleccionado en el treeview, dni, nombre, apellido
            confirmar = askokcancel (title='Confirmar borrado', 
                                     message=f'borrar {campos[1]} {campos[2]}?', 
                                     icon = WARNING)
            if confirmar:
                self.treeview.delete(cliente)
                db.Clientes.borrar(campos[0]) #para que se actualice y aparezca en mi archivo de clientes en la base de datos

    def create (self):
        CreateClientWindow(self)

    def edit (self):
        if self.treeview.focus():
            EditClientWindow(self)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
