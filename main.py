from tkinter import *
from tkinter import ttk
from article import *
from client import *
from vente import *
from home import VideoPlayer
#color utiliser
color_bag = '#481B6B'
color_button = '#8b3dff'
color_activebtn = '#D2B3EF'
def Clear_window():
    for widget in root.winfo_children():
        if isinstance(widget, Frame):
            widget.destroy()

def frame_afficher_article():
    Clear_window()
    Afficher_Article(root, show_video_player)

def frame_ajouter_article():
    Clear_window()
    Ajouter_Article(root, show_video_player)

def frame_afficher_client():
    Clear_window()
    Afficher_Client(root, show_video_player)

def frame_ajoute_client():
    Clear_window()
    Ajouter_Client(root, show_video_player)

def frame_afficher_vente():
    Clear_window()
    Afficher_Ventes(root, show_video_player)

def frame_ajoute_vente():
    Clear_window()
    Ajouter_Ventes(root, show_video_player)

root = Tk()
root.title('Shop Lead')
root.config(background='#481B6B')
root.resizable(False, False)

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates to center the window
x = (screen_width // 2) - (800 // 2)
y = (screen_height // 2) - (400 // 2)

# Set the geometry to the calculated coordinates
root.geometry(f'800x400+{x}+{y}')
#Logo
img = PhotoImage(file="loginnn.png")
root.iconphoto(True, img)
# Create the menu bar
bare_menu = Menu(root)

# Menu Articles
Article_Menu = Menu(bare_menu, tearoff=False, background='#d9d9d9', foreground='black',
                    activebackground='#ececec', activeforeground='black', relief=RAISED)
bare_menu.add_cascade(label='Articles', menu=Article_Menu)
Article_Menu.add_command(label='Afficher Article', command=frame_afficher_article)
Article_Menu.add_command(label='Ajouter Article', command=frame_ajouter_article)

# Menu Clients
Client_Menu = Menu(bare_menu, tearoff=False)
bare_menu.add_cascade(label='Clients', menu=Client_Menu)
Client_Menu.add_command(label='Afficher les Clients', command=frame_afficher_client)
Client_Menu.add_command(label='Ajouter un Client', command=frame_ajoute_client)

# Menu Ventes
Ventes_Menu = Menu(bare_menu, tearoff=False)
bare_menu.add_cascade(label='Ventes', menu=Ventes_Menu)
Ventes_Menu.add_command(label='Afficher les Ventes', command=frame_afficher_vente)
Ventes_Menu.add_command(label='Ajouter une Vente', command=frame_ajoute_vente)

# Frame video
def show_video_player():
    framevideo = Frame(root, background=color_bag, width=800, height=400)
    framevideo.place(x=-2, y=-2)
    framevideo.pack_forget()
    video_player = VideoPlayer(framevideo)

root.config(menu=bare_menu)
show_video_player()

root.mainloop()
