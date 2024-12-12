from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def login():
    user = email.get()
    password = passworde.get()
    if user.lower() == 'admin' and password == "2025":
        messagebox.showinfo("valide", "La connexion a été réussie. Bienvenue dans l'application")
        rootlogin.destroy()
        from main import root

    else:
        messagebox.showerror("erreur", "Bonjour, le mot de passe et l'utilisateur ne sont pas corrects !!!")

rootlogin = Tk()
rootlogin.title('Shop Lead')
rootlogin.resizable(False, False)

rootlogin.iconbitmap("LOGO.ico")
rootlogin.geometry('800x400')

#Screen width and height
screen_width = rootlogin.winfo_screenwidth()
screen_height = rootlogin.winfo_screenheight()
x = (screen_width // 2) - (800 // 2)
y = (screen_height // 2) - (400 // 2)
rootlogin.geometry(f'800x400+{x}+{y}')

# Create login
img = PhotoImage(file='Login.png')
label_img = Label(rootlogin, bd=0, background='white', image=img)
label_img.pack()
login_label = Label(rootlogin, text='Login', background='#481B6B', fg='#D2B3EF', font=('arial', 24))
login_label.place(x=560, y=70)
login_user = Label(rootlogin, text='User:', background='#481B6B', fg='white', font=('arial', 14))
login_user.place(x=380, y=160)
email = StringVar()
input_user = Entry(rootlogin, justify='center', fg='black', bg='white', font=('arial', 14), highlightthickness=1, highlightbackground='#D2B3EF', relief='solid', textvariable=email)
input_user.place(x=490, y=160)
password_label = Label(rootlogin, text='Password:', background='#481B6B', fg='white', font=('arial', 14))
password_label.place(x=380, y=200)
passworde = StringVar()
input_password = Entry(rootlogin, justify='center', fg='black', bg='white', font=('arial', 14), show='*', highlightthickness=1, highlightbackground='#D2B3EF', relief='solid', textvariable=passworde)
input_password.place(x=490, y=200)
btn_login = Button(rootlogin, text='Conexion', bg='white', fg='BLACK', font=('Arial', 13), activebackground='#D2B3EF', width=16, command=login)
btn_login.place(x=530, y=250)

rootlogin.mainloop()
