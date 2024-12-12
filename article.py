from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from main import *
import re
import mysql.connector

#color utiliser
color_bag = '#481B6B'
color_button = '#8b3dff'
color_activebtn = '#D2B3EF'
class Afficher_Article():
    def __init__(self, window, show_video_callback):
        self.show_video_callback = show_video_callback
        self.frame = Frame(window, bg=color_bag)
        self.label_title = Label(self.frame, text='Liste des Articles', bg=color_bag, fg='white', width=90, height=2,
                                font=('Arial', 16))
        self.label_title.pack()
        self.label_category = Label(self.frame, text='Categories:', background=color_bag, fg='white', font=('arial', 14))
        self.label_category.place(x=49, y=65)
        self.category = StringVar()
        self.category.set('All')
        self.cbox_category = ttk.Combobox(self.frame, textvariable=self.category, values=('All', 'Electronics', 'Apparel', 'Books', 'Home Appliances', 'Furniture'), state='readonly')
        self.cbox_category.place(x=190, y=68)
        self.label_rechercher = Label(self.frame, text='Rechercher:', background=color_bag, fg='white', font=('arial', 14))
        self.label_rechercher.place(x=385, y=65)
        self.input_rechercher = Entry(self.frame, justify='center', fg='black', bg='white', font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn, relief='solid', width=15)
        self.input_rechercher.place(x=510, y=65)
        self.btn_chercher = Button(self.frame, text='Chercher', command=self.search)
        self.btn_chercher.place(x=690, y=67)
        self.cbox_category.bind("<<ComboboxSelected>>", self.category_filter)
        self.treeview_article = ttk.Treeview(self.frame, columns=("id", "libille", "categorie", "prix"), show="headings")
        self.treeview_article.heading("id", text="ID D'article")
        self.treeview_article.column("id", width=100, anchor=CENTER)
        self.treeview_article.heading("libille", text="Libelle D'article")
        self.treeview_article.heading("categorie", text="Categorie D'article")
        self.treeview_article.heading("prix", text="Prix D'article")
        self.treeview_article.place(x=49, y=100)
        self.fill_tv()

        self.btn_fermer = Button(self.frame, text='Fermer', bg='white', fg='BLACK', font=('Arial', 13),
                             activebackground=color_activebtn, width=16, command=self.fermer)
        self.btn_fermer.place(x=49, y=350)

        self.btn_delete = Button(self.frame, text='Delete', bg='white', fg='BLACK', font=('Arial', 13),
                               activebackground=color_activebtn, width=16, command=self.delete_article)
        self.btn_delete.place(x=599, y=350)
        self.btn_update = Button(self.frame, text='Update', bg='white', fg='BLACK', font=('Arial', 13),
                               activebackground=color_activebtn, width=16, command=self.update_article)
        self.btn_update.place(x=324, y=350)

        self.frame.pack(fill=BOTH, expand=True)

    def fermer(self):
        self.frame.destroy()
        self.show_video_callback()




    def fill_tv(self):
        con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
        cur = con.cursor()
        cur.execute('SELECT * FROM article')
        data = cur.fetchall()
        con.close()
        if len(data) != 0:
            self.treeview_article.delete(*self.treeview_article.get_children())
            for row in data:
                self.treeview_article.insert(parent='', index=END, values=row)

    def category_filter(self, event):
        val_category = self.category.get()
        if val_category == "All":
            self.fill_tv()
            return
        con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
        cur = con.cursor()
        cur.execute(f"SELECT * FROM article WHERE category='{val_category}'")
        data = cur.fetchall()
        con.close()
        if len(data) != 0:
            self.treeview_article.delete(*self.treeview_article.get_children())
            for row in data:
                self.treeview_article.insert(parent='', index=END, values=row)


    def delete_article(self):
        selected_item = self.treeview_article.selection()
        if not selected_item:
            messagebox.showwarning("Erreur de sélection", "Veuillez sélectionner un article à supprimer.")
            return

        article_name = self.treeview_article.item(selected_item)['values'][1]

        try:
            # Connect to the database
            con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
            cur = con.cursor()

            # Check for dependent records in vente table
            cur.execute("SELECT * FROM vente WHERE name_article = %s", (article_name,))
            dependent_records = cur.fetchall()

            if dependent_records:
                # If dependent records exist, prompt the user
                confirm = messagebox.askyesno("Confirm Deletion",
                                              "This article has dependent records in the vente table. "
                                              "Do you want to delete these records as well?")
                if confirm:
                    # Delete dependent records in vente table
                    cur.execute("DELETE FROM vente WHERE name_article = %s", (article_name,))
                else:
                    messagebox.showinfo("Deletion Cancelled", "The article was not deleted due to dependent records.")
                    con.close()
                    return

            # Delete the article
            cur.execute("DELETE FROM article WHERE name_article = %s", (article_name,))
            con.commit()
            con.close()
            self.treeview_article.delete(selected_item)
            messagebox.showinfo("Succès", "Article supprimé avec succès !")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def search(self):
        search_val = self.input_rechercher.get()
        selected_category = self.category.get()

        try:
            con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
            cur = con.cursor()

            if selected_category == "All":
                cur.execute("SELECT * FROM article WHERE name_article LIKE %s", ('%' + search_val + '%',))
            else:
                cur.execute("SELECT * FROM article WHERE category = %s AND name_article LIKE %s",
                            (selected_category, '%' + search_val + '%'))

            data = cur.fetchall()
            con.close()

            if len(data) == 0:
                messagebox.showinfo("Résultat de la recherche", "Aucun article trouvé.")
                self.treeview_article.delete(*self.treeview_article.get_children())
                return
            self.treeview_article.delete(*self.treeview_article.get_children())
            for row in data:
                self.treeview_article.insert(parent='', index=END, values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def update_article(self):
        selected_item = self.treeview_article.selection()
        if not selected_item:
            messagebox.showwarning("Erreur de sélection", "Veuillez sélectionner un article à mettre à jour.")
            return
        article_data = self.treeview_article.item(selected_item)['values']
        Update_Article(self.frame, article_data, self.fill_tv)



class Update_Article():
    def __init__(self, parent, article_data, refresh_callback):
        self.refresh_callback = refresh_callback
        self.article_id = article_data[0]
        self.frame = Toplevel(parent)
        self.frame.iconbitmap("LOGO.ico")
        # Screen width and height
        self.screen_width = self.frame.winfo_screenwidth()
        self.screen_height = self.frame.winfo_screenheight()
        self.x = (self.screen_width // 2) - (800 // 2)
        self.y = (self.screen_height // 2) - (400 // 2)
        self.frame.geometry(f'800x400+{self.x}+{self.y}')
        self.frame.title("Shop Lead")
        self.frame.configure(bg=color_bag)
        self.label_title = Label(self.frame, text='Modifier Article', bg=color_bag, fg='white', width=90, height=2,
                                font=('Arial', 16))
        self.label_title.pack()
        self.label_name = Label(self.frame, text="Name D'article :", bg=color_bag, fg='white', font=('Arial', 14))
        self.label_name.place(x=20, y=85)
        self.nom = StringVar(value=article_data[1])
        self.input_name = Entry(self.frame, textvariable=self.nom, justify='center', fg='black', bg='white',
                           font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn,
                           relief='solid', width=40)
        self.input_name.place(x=240, y=85)
        self.label_prix = Label(self.frame, text="Prix D'article :", bg=color_bag, fg='white', font=('Arial', 14))
        self.label_prix.place(x=20, y=165)
        self.prix = StringVar(value=article_data[3])
        self.input_prix = Entry(self.frame, justify='center', textvariable=self.prix, fg='black', bg='white',
                            font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn,
                            relief='solid', width=40)
        self.input_prix.place(x=240, y=165)
        self.label_category = Label(self.frame, text='Categories:', background=color_bag, fg='white', font=('arial', 14))
        self.label_category.place(x=20, y=245)
        self.category = StringVar(value=article_data[2])
        self.cbox_category = ttk.Combobox(self.frame, textvariable=self.category,
                                       values=('Electronics', 'Apparel', 'Books'), state='readonly', width=70)
        self.cbox_category.place(x=240, y=245)
        self.btn_fermer = Button(self.frame, text='FERMER', bg='white', fg='BLACK', font=('Arial', 13), width=16,
                                  activebackground=color_activebtn, command=lambda: self.frame.destroy())
        self.btn_fermer.place(x=60, y=350)
        self.btn_conf = Button(self.frame, text='CONFIRMER', bg='white', fg='BLACK', font=('Arial', 13), width=16,
                                   activebackground=color_activebtn, command=self.confirmer)
        self.btn_conf.place(x=550, y=350)

    def validation(self):
        nom_articl = self.nom.get()
        prix_articl = self.prix.get()
        category = self.category.get()

        if not (nom_articl and prix_articl and category != 'All'):
            messagebox.showerror("Erreur de validation", "Veuillez remplir tous les champs et sélectionner une catégorie.")
            return False
        try:
            prix_articl = float(prix_articl)
            if prix_articl <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur de validation", "Veuillez saisir un prix valide.")
            return False
        return True

    def confirmer(self):
        if not self.validation():
            return

        nom_articl = self.nom.get()
        prix_articl = float(self.prix.get())
        category = self.category.get()

        try:
            con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
            cur = con.cursor()
            cur.execute("UPDATE article SET name_article = %s, category = %s, price = %s WHERE article_id = %s",
                        (nom_articl, category, prix_articl, self.article_id))
            con.commit()
            con.close()
            messagebox.showinfo("Succès", "Article mis à jour avec succès !")
            self.frame.destroy()
            self.refresh_callback()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


class Ajouter_Article():
    def __init__(self, window, show_video_callback):
        self.show_video_callback = show_video_callback
        self.frame = Frame(window, bg=color_bag)
        self.frame.pack(fill=BOTH, expand=True)
        self.label_title = Label(self.frame, text='Ajouter des Articles', bg=color_bag, fg='white', width=90, height=2,
                                font=('Arial', 16))
        self.label_title.pack()
        self.label_name = Label(self.frame, text="Name D'article :", bg=color_bag, fg='white', font=('Arial', 14))
        self.label_name.place(x=20, y=85)
        self.nom = StringVar()
        self.input_name = Entry(self.frame, textvariable=self.nom, justify='center', fg='black', bg='white',
                           font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn,
                           relief='solid', width=40)
        self.input_name.place(x=240, y=85)
        self.label_prix = Label(self.frame, text="Prix D'article :", bg=color_bag, fg='white', font=('Arial', 14))
        self.label_prix.place(x=20, y=165)
        self.prix = StringVar()
        self.input_prix = Entry(self.frame, justify='center', textvariable=self.prix, fg='black', bg='white',
                            font=('arial', 14), highlightthickness=1, highlightbackground=color_activebtn,
                            relief='solid', width=40)
        self.input_prix.place(x=240, y=165)
        self.label_category = Label(self.frame, text='Categories:', background=color_bag, fg='white', font=('arial', 14))
        self.label_category.place(x=20, y=245)
        self.category = StringVar()
        self.category.set('All')
        self.cbox_category = ttk.Combobox(self.frame, textvariable=self.category,
                                       values=('Electronics', 'Apparel', 'Books', 'Home Appliances', 'Furniture'), state='readonly', width=70)
        self.cbox_category.place(x=240, y=245)
        self.btn_fermer = Button(self.frame, text='FERMER', bg='white', fg='BLACK', font=('Arial', 13), width=16,
                                  activebackground=color_activebtn, command=self.fermer)
        self.btn_fermer.place(x=60, y=350)
        self.btn_conf = Button(self.frame, text='CONFIRMER', bg='white', fg='BLACK', font=('Arial', 13), width=16,
                                   activebackground=color_activebtn, command=self.confirmer)
        self.btn_conf.place(x=550, y=350)

    def validation(self):
        nom_articl = self.nom.get()
        prix_articl = self.prix.get()
        category = self.category.get()

        if not (nom_articl and prix_articl and category != 'All'):
            messagebox.showerror("Erreur de validation", "Veuillez remplir tous les champs et sélectionner une catégorie.")
            return False
        elif not re.match(r"^[a-zA-Z\s]+$", nom_articl):
            messagebox.showerror("Erreur de validation", "Le nom ne doit contenir que des lettres et des espaces.")
            return False
        try:
            prix_articl = float(prix_articl)
            if prix_articl <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur de validation", "Veuillez entrer un prix valide.")
            return False
        return True

    def confirmer(self):
        if not self.validation():
            return

        nom_articl = self.nom.get()
        prix_articl = float(self.prix.get())
        category = self.category.get()

        try:
            con = mysql.connector.connect(host='localhost', database='article', user='root', password='0000')
            cur = con.cursor()
            cur.execute("INSERT INTO article (name_article, category, price) VALUES (%s, %s, %s)",
                        (nom_articl, category, prix_articl))
            con.commit()
            con.close()
            messagebox.showinfo("Succès", "Article ajouté avec succès !")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


    def fermer(self):
        self.frame.destroy()
