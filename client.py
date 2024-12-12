from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re
from main import *
import mysql.connector

#color utiliser
color_bag = '#481B6B'
color_button = '#8b3dff'
color_activebtn = '#D2B3EF'


class Afficher_Client():
    def __init__(self, window, show_video_callback):
        self.show_video_callback = show_video_callback
        self.frame = Frame(window, bg=color_bag)
        self.label_title = Label(self.frame, text='Liste des Clients', bg=color_bag, fg='white', width=90, height=2, font=('Arial', 16))
        self.label_title.pack()
        self.label_options = Label(self.frame, text='Options:', background=color_bag, fg='white', font=('arial', 14))
        self.label_options.place(x=49, y=65)
        self.btn_chercher = Button(self.frame, text='Chercher', command=self.search_client)
        self.btn_chercher.place(x=690, y=67)

        self.combox_options = ttk.Combobox(self.frame, values=('Nom', 'Email', 'Téléphone'), state='readonly')
        self.combox_options.place(x=160, y=68)
        self.label_rechercher = Label(self.frame, text='Rechercher:', background=color_bag, fg='white', font=('arial', 14))
        self.label_rechercher.place(x=385, y=65)
        self.input_rechercher = Entry(self.frame, justify='center', fg='black', bg='white', font=('arial', 14),highlightthickness=1, highlightbackground=color_activebtn, relief='solid', width=15)
        self.input_rechercher.place(x=510, y=65)
        self.treeview_client = ttk.Treeview(self.frame, columns=("client_id", "name", "phone", "email"), show="headings")
        self.treeview_client.heading("client_id", text='Client ID')
        self.treeview_client.column("client_id", width=100, anchor=CENTER)
        self.treeview_client.heading("name", text='Nom de Client')
        self.treeview_client.column("name", anchor=CENTER)
        self.treeview_client.heading("phone", text='Telephone de Client')
        self.treeview_client.column("phone", anchor=CENTER)
        self.treeview_client.heading("email", text='Email de Clients')
        self.treeview_client.column("email", anchor=CENTER)
        self.treeview_client.place(x=49, y=100)
        self.btn_update = Button(self.frame, text='Update', bg='white', fg='BLACK', font=('Arial', 13), activebackground=color_activebtn, width=16, command=self.update_client)
        self.btn_update.place(x=330, y=350)
        self.btn_delete = Button(self.frame, text='Delete', bg='white', fg='BLACK', font=('Arial', 13), activebackground=color_activebtn, width=16, command=self.delete_client)
        self.btn_delete.place(x=595, y=350)
        self.btn_fermer = Button(self.frame, text='Fermer', bg='white', fg='BLACK', font=('Arial', 13), activebackground=color_activebtn, width=16, command=self.fermer)
        self.btn_fermer.place(x=49, y=350)

        self.fill_tv()
        self.frame.pack(fill=BOTH, expand=True)

    def fill_tv(self):
        con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
        cur = con.cursor()
        cur.execute('SELECT client_id, name_client, phone, email FROM client')
        data = cur.fetchall()
        con.close()
        if data:
            self.treeview_client.delete(*self.treeview_client.get_children())
            for row in data:
                self.treeview_client.insert(parent='', index=END, values=row)



    def delete_client(self):
        selected_item = self.treeview_client.selection()
        if not selected_item:
            messagebox.showwarning("Erreur de sélection", "Veuillez sélectionner un client à supprimer.")
            return

        client_name = self.treeview_client.item(selected_item)['values'][1]

        try:
            con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
            cur = con.cursor()

            cur.execute("DELETE FROM vente WHERE name_client = %s", (client_name,))
            cur.execute("DELETE FROM client WHERE name_client = %s", (client_name,))
            con.commit()
            con.close()

            self.treeview_client.delete(selected_item)
            messagebox.showinfo("Succès", "Client supprimé avec succès !")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def search_client(self):
        search_option = self.combox_options.get()
        search_value = self.input_rechercher.get()

        if not search_option or not search_value:
            messagebox.showerror("Erreur de validation", "Veuillez sélectionner une option et entrer une valeur de recherche.")
            return

        column_map = {
            'Nom': 'name_client',
            'Email': 'email',
            'Téléphone': 'phone'

        }

        column_name = column_map[search_option]

        try:
            con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
            cur = con.cursor()
            query = f"SELECT client_id, name_client, phone, email FROM client WHERE {column_name} LIKE %s"
            cur.execute(query, ('%' + search_value + '%',))
            data = cur.fetchall()
            con.close()

            self.treeview_client.delete(*self.treeview_client.get_children())
            for row in data:
                self.treeview_client.insert('', 'end', values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def fermer(self):
        self.frame.destroy()
        self.show_video_callback()

    def update_client(self):
        selected_item = self.treeview_client.selection()
        if not selected_item:
            messagebox.showwarning("Erreur de sélection", "Veuillez sélectionner un client à mettre à jour.")
            return

        client_data = self.treeview_client.item(selected_item)['values']
        Update_Client(self.frame, client_data, self.fill_tv)

class Update_Client():
    def __init__(self, parent, client_data, refresh_callback):
        self.refresh_callback = refresh_callback
        self.client_id = client_data[0]
        self.frame = Toplevel(parent)
        self.frame.geometry("800x400")
        self.frame.geometry("800x400")
        # Screen width and height
        self.screen_width = self.frame.winfo_screenwidth()
        self.screen_height = self.frame.winfo_screenheight()
        self.x = (self.screen_width // 2) - (800 // 2)
        self.y = (self.screen_height // 2) - (400 // 2)
        self.frame.geometry(f'800x400+{self.x}+{self.y}')
        self.frame.title("Shop Lead")
        self.frame.configure(bg=color_bag)

        self.label_title = Label(self.frame, text='Modifier Client', bg=color_bag, fg='white', width=90, height=2,
                                font=('Arial', 16))
        self.label_title.pack()

        self.btn_name = Label(self.frame, text="Nom du Client :", bg=color_bag, fg='white', font=('Arial', 14))
        self.btn_name.place(x=20, y=85)
        self.name = StringVar(value=client_data[1])
        self.input_name = Entry(self.frame, textvariable=self.name, justify='center', fg='black', bg='white',
                             font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn,
                             relief='solid', width=40)
        self.input_name.place(x=240, y=85)

        self.label_phone = Label(self.frame, text="Téléphone :", bg=color_bag, fg='white', font=('Arial', 14))
        self.label_phone.place(x=20, y=165)
        self.phone = StringVar(value=client_data[2])
        self.input_phone = Entry(self.frame, textvariable=self.phone, justify='center', fg='black', bg='white',
                              font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn,
                              relief='solid', width=40)
        self.input_phone.place(x=240, y=165)

        self.label_email = Label(self.frame, text='Email:', bg=color_bag, fg='white', font=('Arial', 14))
        self.label_email.place(x=20, y=245)
        self.email = StringVar(value=client_data[3])
        self.input_email = Entry(self.frame, textvariable=self.email, justify='center', fg='black', bg='white',
                              font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn,
                              relief='solid', width=40)
        self.input_email.place(x=240, y=245)

        self.btn_fermer = Button(self.frame, text='FERMER', bg='white', fg='BLACK', font=('Arial', 13), width=16,
                                  activebackground=color_activebtn, command=lambda: self.frame.destroy())
        self.btn_fermer.place(x=60, y=350)
        self.btn_conf = Button(self.frame, text='CONFIRMER', bg='white', fg='BLACK', font=('Arial', 13), width=16,
                                   activebackground=color_activebtn, command=self.confirmer)
        self.btn_conf.place(x=550, y=350)

    def validation(self):
        name = self.name.get().strip()
        phone = self.phone.get().strip()
        email = self.email.get().strip()

        # Check if any field is empty
        if not (name and phone and email):
            messagebox.showerror("Erreur de validation", "Tous les champs sont obligatoires.")
            return False

        # Validate phone number
        if not re.match(r'^\+?[0-9\s-]+$', phone):
            messagebox.showerror("Erreur de validation", "Format de numéro de téléphone invalide. Veuillez entrer un numéro de téléphone valide.")
            return False

        # Validate email format
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messagebox.showerror("Erreur de validation", "Format d'email invalide. Veuillez entrer une adresse email valide.")
            return False

        return True

    def confirmer(self):
        if not self.validation():
            return

        name = self.name.get().strip()
        phone = self.phone.get().strip()
        email = self.email.get().strip()

        try:
            con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
            cur = con.cursor()
            cur.execute("""
                UPDATE client
                SET name_client = %s, phone = %s, email = %s
                WHERE client_id = %s
            """, (name, phone, email, self.client_id))
            con.commit()
            con.close()
            messagebox.showinfo("Succès", "Client mis à jour avec succès !")
            self.frame.destroy()
            self.refresh_callback()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


class Ajouter_Client():
    def __init__(self, window, show_video_callback):
        self.show_video_callback = show_video_callback
        self.frame = Frame(window, bg=color_bag)
        self.frame.pack(fill=BOTH, expand=True)
        self.label_title = Label(self.frame, text='Ajouter des Clients', bg=color_bag, fg='white', width=90, height=2, font=('Arial', 16))
        self.label_title.pack()
        self.label_nom = Label(self.frame, text="Nom de Client :", bg=color_bag, fg='white', font=('Arial', 14))
        self.label_nom.place(x=20, y=85)
        self.valnomclient = StringVar()
        self.input_nom = Entry(self.frame, textvariable=self.valnomclient, justify='center', fg='black', bg='white', font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn, relief='solid', width=40)
        self.input_nom.place(x=240, y=85)
        self.label_email = Label(self.frame, text="Email de Client :", bg=color_bag, fg='white', font=('Arial', 14))
        self.label_email.place(x=20, y=165)
        self.vlemailclient = StringVar()
        self.input_email = Entry(self.frame, justify='center', textvariable=self.vlemailclient, fg='black', bg='white', font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn, relief='solid', width=40)
        self.input_email.place(x=240, y=165)
        self.label_tele = Label(self.frame, text="Telephone de Client :", bg=color_bag, fg='white', font=('Arial', 14))
        self.label_tele.place(x=20, y=245)
        self.vlteleclient = StringVar()
        self.input_tele = Entry(self.frame, justify='center', textvariable=self.vlteleclient, fg='black', bg='white', font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn, relief='solid', width=40)
        self.input_tele.place(x=240, y=245)
        self.btn_fermer = Button(self.frame, text='Fermer', bg='white', fg='BLACK', font=('Arial', 13), activebackground=color_activebtn, width=16, command=self.fermer)
        self.btn_fermer.place(x=50, y=350)
        self.btn_conf = Button(self.frame, text='Ajoute', bg='white', fg='BLACK', font=('Arial', 13), activebackground=color_activebtn, width=16, command=self.validation)
        self.btn_conf.place(x=590, y=350)

    def validation(self):
        nom_client = self.valnomclient.get()
        email_client = self.vlemailclient.get()
        telephone_client = self.vlteleclient.get()

        if not (nom_client and email_client and telephone_client):
            messagebox.showerror("Erreur de validation", "Veuillez remplir tous les champs.")
            return False
        elif not re.match(r"^[a-zA-Z\s]+$", nom_client):
            messagebox.showerror("Erreur de validation", "Le nom ne doit contenir que des lettres et des espaces.")
            return False
        elif not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email_client):
            messagebox.showerror("Erreur de validation", "Veuillez entrer une adresse email professionnelle valide.")
            return False
        elif not telephone_client.isdigit() or len(telephone_client) != 10:
            messagebox.showerror("Erreur de validation", "Veuillez entrer un numéro de téléphone valide avec 10 chiffres.")
            return False
        else:
            self.add_to_database(nom_client, email_client, telephone_client)
            return True

    def add_to_database(self, nom_client, email_client, telephone_client):
        try:
            con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
            cur = con.cursor()

            cur.execute("""
                INSERT INTO client (name_client, phone, email)
                VALUES (%s, %s, %s)
            """, (nom_client, telephone_client, email_client))

            con.commit()
            con.close()

            messagebox.showinfo("Succès", "Félicitations, le client a été ajouté avec succès !")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    def fermer(self):
        self.frame.destroy()
        self.show_video_callback()




