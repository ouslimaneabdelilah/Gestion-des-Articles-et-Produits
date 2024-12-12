from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import re
from main import *
from datetime import datetime

#color utiliser
color_bag = '#481B6B'
color_button = '#8b3dff'
color_activebtn = '#D2B3EF'


class Afficher_Ventes():
    def __init__(self, window, show_video_callback):
        self.show_video_callback = show_video_callback
        self.frame = Frame(window, bg=color_bag)
        self.label_title = Label(self.frame, text='Liste des Ventes', bg=color_bag, fg='white', width=90, height=2, font=('Arial', 16))
        self.label_title.pack()
        self.label_options = Label(self.frame, text='Options:', background=color_bag, fg='white', font=('arial', 14))
        self.label_options.place(x=49, y=65)
        self.combox_options = ttk.Combobox(self.frame, values=('Article', 'Client'), state='readonly')
        self.combox_options.place(x=160, y=68)

        self.label_rechercher = Label(self.frame, text='Rechercher:', background=color_bag, fg='white', font=('arial', 14))
        self.label_rechercher.place(x=385, y=65)
        self.input_rechercher = Entry(self.frame, justify='center', fg='black', bg='white', font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn, relief='solid', width=15)
        self.input_rechercher.place(x=510, y=65)

        self.btn_chercher = Button(self.frame, text='Chercher', command=self.search_vente, activebackground=color_activebtn)
        self.btn_chercher.place(x=690, y=67)
        self.treeview_vente = ttk.Treeview(self.frame, columns=("vente_id", "name_article", "name_client", "quantity", "sale_date", "total_price"), show="headings")
        self.treeview_vente.heading("vente_id", text='Vente ID')
        self.treeview_vente.heading("name_article", text='Article')
        self.treeview_vente.heading("name_client", text='Client')
        self.treeview_vente.heading("quantity", text='Quantité')
        self.treeview_vente.heading("sale_date", text='Date de Vente')
        self.treeview_vente.heading("total_price", text='Prix Total')
        self.treeview_vente.column("vente_id", width=65, anchor=CENTER)
        self.treeview_vente.column("name_article", width=120, anchor=CENTER)
        self.treeview_vente.column("name_client", anchor=CENTER)
        self.treeview_vente.column("quantity", width=90, anchor=CENTER)
        self.treeview_vente.column("sale_date", width=100, anchor=CENTER)
        self.treeview_vente.column("total_price", width=120, anchor=CENTER)
        self.treeview_vente.place(x=49, y=100)

        self.btn_update = Button(self.frame, text='Update', bg='white', fg='BLACK', font=('Arial', 13), activebackground=color_activebtn, width=16, command=self.update_vente)
        self.btn_update.place(x=330, y=350)
        self.btn_delete = Button(self.frame, text='Delete', bg='white', fg='BLACK', font=('Arial', 13), activebackground=color_activebtn, width=16, command=self.delete_vente)
        self.btn_delete.place(x=595, y=350)
        self.btn_fermer = Button(self.frame, text='Fermer', bg='white', fg='BLACK', font=('Arial', 13), activebackground=color_activebtn, width=16, command=self.fermer)
        self.btn_fermer.place(x=49, y=350)

        self.fill_tv()
        self.frame.pack(fill=BOTH, expand=True)

    def fill_tv(self):
        con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
        cur = con.cursor()
        cur.execute('SELECT vente_id, name_article, name_client, quantity, sale_date, total_price FROM vente')
        data = cur.fetchall()
        con.close()
        if data:
            self.treeview_vente.delete(*self.treeview_vente.get_children())
            for row in data:
                self.treeview_vente.insert(parent='', index=END, values=row)

    def delete_vente(self):
        selected_item = self.treeview_vente.selection()
        if not selected_item:
            messagebox.showwarning("Erreur de sélection", "Veuillez sélectionner une vente à supprimer.")
            return

        vente_id = self.treeview_vente.item(selected_item)['values'][0]

        try:
            con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
            cur = con.cursor()

            cur.execute("DELETE FROM vente WHERE vente_id = %s", (vente_id,))
            con.commit()
            con.close()

            self.treeview_vente.delete(selected_item)
            messagebox.showinfo("Succès", "Vente supprimée avec succès !")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def search_vente(self):
        search_option = self.combox_options.get()
        search_value = self.input_rechercher.get()

        if not search_option or not search_value:
            messagebox.showerror("Erreur de validation", "Veuillez sélectionner une option et entrer une valeur de recherche.")
            return

        column_map = {
            'Article': 'name_article',
            'Client': 'name_client',
        }

        column_name = column_map[search_option]

        try:
            con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
            cur = con.cursor()
            query = f"""
                SELECT vente_id, name_article, name_client, quantity, sale_date, total_price 
                FROM vente 
                WHERE {column_name} LIKE %s
            """
            cur.execute(query, ('%' + search_value + '%',))
            data = cur.fetchall()
            con.close()

            self.treeview_vente.delete(*self.treeview_vente.get_children())
            for row in data:
                self.treeview_vente.insert('', 'end', values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def fermer(self):
        self.frame.destroy()
        self.show_video_callback()


    def update_vente(self):
        selected_item = self.treeview_vente.selection()
        if not selected_item:
            messagebox.showwarning("Erreur de sélection", "Veuillez sélectionner une vente à mettre à jour.")
            return

        vente_data = self.treeview_vente.item(selected_item)['values']
        Update_Vente(self.frame, vente_data, self.fill_tv)


class Update_Vente():
    def __init__(self, parent, vente_data, refresh_callback):
        self.refresh_callback = refresh_callback
        self.vente_id = vente_data[0]
        self.frame = Toplevel(parent)
        self.frame.title("Shop Lead")
        self.frame.configure(bg=color_bag)
        # Screen width and height
        self.screen_width = self.frame.winfo_screenwidth()
        self.screen_height = self.frame.winfo_screenheight()
        self.x = (self.screen_width // 2) - (800 // 2)
        self.y = (self.screen_height // 2) - (400 // 2)
        self.frame.geometry(f'800x400+{self.x}+{self.y}')
        self.label_title = Label(self.frame, text='Modifier Vente', bg=color_bag, fg='white', width=90, height=2,
                                 font=('Arial', 16))
        self.label_title.pack()

        self.label_article = Label(self.frame, text='Article:', bg=color_bag, fg='white', font=('Arial', 14))
        self.label_article.place(x=20, y=85)

        self.article = StringVar(value=vente_data[1])
        self.article_list = self.get_article_names()
        self.input_article = ttk.Combobox(self.frame, textvariable=self.article, values=self.article_list,
                                       state='readonly', font=('arial', 14), width=38)
        self.input_article.place(x=240, y=85)
        self.input_article.current(self.article_list.index(vente_data[1]))  # Set the selected article

        self.label_client = Label(self.frame, text='Client:', bg=color_bag, fg='white', font=('Arial', 14))
        self.label_client.place(x=20, y=135)
        self.client = StringVar(value=vente_data[2])
        self.input_client = Entry(self.frame, textvariable=self.client, justify='center', fg='black', bg='white',
                               font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn,
                               relief='solid', width=40, state='readonly')
        self.input_client.place(x=240, y=135)

        self.label_quantity = Label(self.frame, text='Quantité:', bg=color_bag, fg='white', font=('Arial', 14))
        self.label_quantity.place(x=20, y=185)
        self.quantity = StringVar(value=vente_data[3])
        self.input_quantity = Entry(self.frame, textvariable=self.quantity, justify='center', fg='black', bg='white',
                                 font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn,
                                 relief='solid', width=40)
        self.input_quantity.place(x=240, y=185)

        self.label_date = Label(self.frame, text='Date de Vente:', bg=color_bag, fg='white', font=('Arial', 14))
        self.label_date.place(x=20, y=235)
        self.sale_date = StringVar(value=vente_data[4])
        self.input_date = Entry(self.frame, textvariable=self.sale_date, justify='center', fg='black', bg='white',
                             font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn,
                             relief='solid', width=40)
        self.input_date.place(x=240, y=235)

        self.lb_total_prix = Label(self.frame, text='Prix Total:', bg=color_bag, fg='white', font=('Arial', 14))
        self.lb_total_prix.place(x=20, y=285)
        self.total_price = StringVar(value=vente_data[5])
        self.inp_total_prix = Entry(self.frame, textvariable=self.total_price, justify='center', fg='black', bg='white',
                                    font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn,
                                    relief='solid', width=40, state='readonly')
        self.inp_total_prix.place(x=240, y=285)

        self.btn_fermer = Button(self.frame, text='FERMER', bg='white', fg='BLACK', font=('Arial', 13), width=16,
                                  activebackground=color_activebtn, command=lambda: self.frame.destroy())
        self.btn_fermer.place(x=50, y=335)
        self.btn_conf = Button(self.frame, text='CONFIRMER', bg='white', fg='BLACK', font=('Arial', 13), width=16,
                                   activebackground=color_activebtn, command=self.confirmer)
        self.btn_conf.place(x=590, y=335)

    def get_article_names(self):
        try:
            con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
            cur = con.cursor()
            cur.execute("SELECT name_article FROM article")
            articles = cur.fetchall()
            con.close()
            return [article[0] for article in articles]
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching articles: {err}")
            return []
################# khtad khtad
    def validation(self):
        article = self.article.get().strip()
        client = self.client.get().strip()
        quantity = self.quantity.get().strip()
        sale_date = self.sale_date.get().strip()

        # Check if any field is empty
        if not (article and client and quantity and sale_date):
            messagebox.showerror("Erreur de validation", "Tous les champs sont obligatoires.")
            return False

        # Validate quantity: it should be a positive integer
        if not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showerror("Erreur de validation", "La quantité doit être un nombre entier positif.")
            return False

        # Validate date format (YYYY-MM-DD)
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, sale_date):
            messagebox.showerror("Erreur de validation", "Le format de la date doit être AAAA-MM-JJ.")
            return False

        try:
            # Parse the date
            sale_date_obj = datetime.strptime(sale_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erreur de validation", "Date invalide. La date doit être au format AAAA-MM-JJ.")
            return False

        # Check if the year is negative
        if sale_date_obj.year < 0:
            messagebox.showerror("Erreur de validation", "L'année doit être un nombre positif.")
            return False

        # Validate month and day limits
        if sale_date_obj.month < 1 or sale_date_obj.month > 12:
            messagebox.showerror("Erreur de validation", "Le mois doit être compris entre 1 et 12.")
            return False

        if sale_date_obj.day < 1 or sale_date_obj.day > 31:
            messagebox.showerror("Erreur de validation", "Le jour doit être compris entre 1 et 31.")
            return False

        # Check February's day limits
        if sale_date_obj.month == 2:  # February
            if (sale_date_obj.year % 4 == 0 and sale_date_obj.year % 100 != 0) or (sale_date_obj.year % 400 == 0):
                if sale_date_obj.day > 29:
                    messagebox.showerror("Erreur de validation",
                                         "Février en année bissextile doit avoir un jour inférieur ou égal à 29.")
                    return False
            else:
                if sale_date_obj.day > 28:
                    messagebox.showerror("Erreur de validation", "Février doit avoir un jour inférieur ou égal à 28.")
                    return False

        # Check months with 30 days
        elif sale_date_obj.month in [4, 6, 9, 11]:  # Months with 30 days
            if sale_date_obj.day > 30:
                messagebox.showerror("Erreur de validation", f"{sale_date_obj.strftime('%B')} a seulement 30 jours.")
                return False

        return True
    def confirmer(self):
        if not self.validation():
            return

        article = self.article.get().strip()
        client = self.client.get().strip()
        quantity = self.quantity.get().strip()
        sale_date = self.sale_date.get().strip()

        try:
            # Connect to the database
            con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
            cur = con.cursor()

            # Fetch the price of the selected article
            cur.execute("SELECT price FROM article WHERE name_article = %s", (article,))
            article_price = cur.fetchone()

            if article_price:
                article_price = article_price[0]
                total_price = round(article_price * int(quantity), 2)

                # Update the vente record with the new values and total price
                cur.execute("""
                    UPDATE vente
                    SET name_article = %s, name_client = %s, quantity = %s, sale_date = %s, total_price = %s
                    WHERE vente_id = %s
                """, (article, client, quantity, sale_date, total_price, self.vente_id))
                con.commit()
                con.close()
                messagebox.showinfo("Succès", "Vente mise à jour avec succès !")
                self.frame.destroy()
                self.refresh_callback()
            else:
                messagebox.showerror("Erreur", "Article non trouvé dans la base de données.")
                con.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


class Ajouter_Ventes():
    def __init__(self, window, show_video_callback):
        self.show_video_callback = show_video_callback
        self.frame = Frame(window, bg=color_bag)  # Adjust the background color to color_bag or your preferred color
        self.frame.pack(fill=BOTH, expand=True)

        self.lbajoute = Label(self.frame, text='Ajouter des Ventes', bg=color_bag, fg='white', width=90, height=2,
                              font=('Arial', 16))
        self.lbajoute.pack()

        # Fetch article names from the database
        self.article_list = self.get_article_names()

        self.label_article = Label(self.frame, text="Article :", bg=color_bag, fg='white', font=('Arial', 14))
        self.label_article.place(x=20, y=85)
        self.valarticle = StringVar()
        self.input_article = ttk.Combobox(self.frame, textvariable=self.valarticle, values=self.article_list,
                                      state='readonly', font=('arial', 14), width=38)
        self.input_article.place(x=240, y=85)
        self.input_article.current(0)  # Set the default selection, if needed

        # Fetch client names from the database
        self.client_list = self.get_client_names()

        self.label_client = Label(self.frame, text="Client :", bg=color_bag, fg='white', font=('Arial', 14))
        self.label_client.place(x=20, y=145)
        self.valclient = StringVar()
        self.label_client = ttk.Combobox(self.frame, textvariable=self.valclient, values=self.client_list, state='readonly',
                                     font=('arial', 14), width=38)
        self.label_client.place(x=240, y=145)
        self.label_client.current(0)  # Set the default selection, if needed

        self.label_quantity = Label(self.frame, text="Quantité :", bg=color_bag, fg='white', font=('Arial', 14))
        self.label_quantity.place(x=20, y=205)
        self.valquantity = StringVar()
        self.input_quantity = Entry(self.frame, justify='center', textvariable=self.valquantity, fg='black', bg='white',
                                font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn, relief='solid',
                                width=40)
        self.input_quantity.place(x=240, y=205)

        self.label_date = Label(self.frame, text="Date de Vente :", bg=color_bag, fg='white', font=('Arial', 14))
        self.label_date.place(x=20, y=265)
        self.valdate = StringVar()
        self.input_date = Entry(self.frame, justify='center', textvariable=self.valdate, fg='black', bg='white',
                            font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn, relief='solid',
                            width=40)
        self.input_date.place(x=240, y=265)

        self.btn_fermer = Button(self.frame, text='Fermer', bg='white', fg='BLACK', font=('Arial', 13),
                             activebackground=color_activebtn, width=16, command=self.fermer)
        self.btn_fermer.place(x=50, y=335)
        self.btn_vente = Button(self.frame, text='Ajouter', bg='white', fg='BLACK', font=('Arial', 13),
                                 activebackground=color_activebtn, width=16, command=self.validation)
        self.btn_vente.place(x=590, y=335)

    def get_article_names(self):
        try:
            con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
            cur = con.cursor()
            cur.execute("SELECT name_article FROM article")
            articles = cur.fetchall()
            con.close()
            return [article[0] for article in articles]
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching articles: {err}")
            return []

    def get_client_names(self):
        try:
            con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
            cur = con.cursor()
            cur.execute("SELECT name_client FROM client")
            clients = cur.fetchall()
            con.close()
            return [client[0] for client in clients]
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching clients: {err}")
            return []

    def validation(self):
        name_article = self.valarticle.get()
        name_client = self.valclient.get()
        quantity = self.valquantity.get()
        sale_date = self.valdate.get()

        if not (name_article and name_client and quantity and sale_date):
            messagebox.showerror("Erreur de validation", "Veuillez remplir tous les champs.")
            return False
        elif not quantity.isdigit():
            messagebox.showerror("Erreur de validation", "La quantité doit être numérique.")
            return False
        else:
            self.add_to_database(name_article, name_client, quantity, sale_date)
            return True

    def add_to_database(self, name_article, name_client, quantity, sale_date):
        try:
            con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
            cur = con.cursor()

            # Check if the article exists
            cur.execute("SELECT price FROM article WHERE name_article = %s", (name_article,))
            price_result = cur.fetchone()
            if price_result:
                price = price_result[0]
                total_price = float(price) * int(quantity)
            else:
                messagebox.showerror("Erreur", "Article non trouvé.")
                return

            # Check if the client exists
            cur.execute("SELECT client_id FROM client WHERE name_client = %s", (name_client,))
            client_result = cur.fetchone()
            if not client_result:
                messagebox.showerror("Erreur", "Client non trouvé.")
                return

            cur.execute("""
                INSERT INTO vente (name_article, name_client, quantity, sale_date, total_price)
                VALUES (%s, %s, %s, %s, %s)
            """, (name_article, name_client, quantity, sale_date, total_price))

            con.commit()
            con.close()

            messagebox.showinfo("Succès", "Vente ajoutée avec succès.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    def fermer(self):
        self.frame.destroy()
        self.show_video_callback()

