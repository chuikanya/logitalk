from customtkinter import *
import threading
from socket import *
from PIL import Image


class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('600x400')
        self.title("Logitalk")
        self.resizable(False, False)
        self.configure(fg_color='#8E1EA2')
        self.is_show_menu = False

        self.chat_field = CTkScrollableFrame(self, width=520, height=310, fg_color='#80426E', scrollbar_button_color="#462C7D", scrollbar_button_hover_color="#674BA5")
        self.chat_field.place(x=65, y=10)
        self.message_entry = CTkEntry(
            self,
            placeholder_text='Escribe un mensaje:',
            width=450,
            height=40,
            fg_color='#EA9D9D',
            text_color='#FFFFFF',
            border_color='#BD5579',
            placeholder_text_color='#FFFFFF'
        )
        self.message_entry.bind("<Return>", lambda event: self.send_message())
        self.message_entry.place(x=65, y=340)

        self.send_button = CTkButton(
            self,
            text='>',
            width=50,
            height=40,
            command=self.send_message,
            fg_color='#462C7D'
        )
        self.send_button.place(x=530, y=340)

        self.menu_frame = CTkFrame(self, width=50, height=400, fg_color='#8E1EA2')
        self.menu_frame.place(x=0, y=0)
        self.menu_frame.pack_propagate(False)

        self.btn = CTkButton(self.menu_frame, text='▶️', command=self.toggle_menu, width=35, fg_color='#462C7D')
        self.btn.place(x=7, y=10)

        self.menu_content = CTkFrame(self.menu_frame, width=180, height=330, fg_color="#802C62")

        CTkLabel(self.menu_content, text='Імʼя:').pack(pady=(5, 2))
        self.username_entry = CTkEntry(self.menu_content, width=160, fg_color='#9E7EB5', border_color='#5D1C6A')
        self.username_entry.pack(padx=10, pady=(0, 5))

        try:
            self.menu_bg = CTkImage(dark_image=Image.open("durin.jpg"), size=(180, 250))
            self.menu_bg_label = CTkLabel(self.menu_content, text="", image=self.menu_bg)
            self.menu_bg_label.pack(fill="both", expand=True, padx=0, pady=0)
        except Exception as e:
            print(f"Помилка завантаження фото: {e}")

        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('4.tcp.eu.ngrok.io', 22283))
            threading.Thread(target=self.recv_message, daemon=True).start()
        except Exception as e:
            self.add_message(f"Помилка підключення: {e}")

    def toggle_menu(self):
        if self.is_show_menu:
            self.menu_content.place_forget()
            self.menu_frame.configure(width=50)
            self.btn.configure(text='▶️')
            self.is_show_menu = False
        else:
            self.menu_frame.configure(width=200)
            self.menu_content.place(x=10, y=50)
            self.btn.configure(text='◀️')
            self.is_show_menu = True

    def add_message(self, text):
        def _update():
            msg_label = CTkLabel(
                self.chat_field,
                text=text,
                anchor='w',
                justify='left',
                text_color='#FFFFFF'
            )
            msg_label.pack(fill='x', padx=5, pady=3)
            self.chat_field._parent_canvas.yview_moveto(1.0)

        self.after(0, _update)

    def send_message(self):
        name = (self.username_entry.get().strip() or "User")
        message = (self.message_entry.get().strip())
        if message:
            full_text = f"{name}: {message}"
            self.add_message(f"Я: {message}")
            try:
                self.sock.send(full_text.encode())
            except:
                pass
            self.message_entry.delete(0, 'end')

    def recv_message(self):
        while True:
            try:
                message = self.sock.recv(1024).decode()
                if message:
                    self.add_message(message)
            except:
                break



win = MainWindow()
win.mainloop()