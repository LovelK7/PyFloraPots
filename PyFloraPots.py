import customtkinter as ctk
ctk.set_appearance_mode('light')
ctk.set_default_color_theme('green')
from tkinter import messagebox
import datetime
import time
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from user import User 
from database import DBHandler
from meteo import Meteo
from sensors import Sensor
from plots import PyF_plots
from measurements import Meas
from file_manager import FileMngr

#-----------------------MAIN GUI--------------------------------

class PyF_login(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.user = User()
        self.authentication = False

        #Login screen initialization
        self.login = ctk.CTk()
        self.login.title('PyFlora - Login')
        self.login.state('zoomed')

        self.header_frame = ctk.CTkFrame(master=self.login)
        self.header_frame.pack(padx=60, pady=20, fill='both', expand=True)
        self.header = ctk.CTkLabel(master=self.header_frame, text ='PyFloraPots', font=('Roboto', 18))
        self.header.pack(padx=10, pady=12)

        self.root_title = ctk.CTkLabel(master=self.login, text ='Login', font=('Roboto', 20))
        self.root_title.pack(padx=10, pady=12)

        self.input_username = ctk.CTkEntry(master=self.login, placeholder_text='username')
        self.input_username.pack(padx=10, pady=12)

        self.input_password = ctk.CTkEntry(master=self.login, placeholder_text='password', show = '*')
        self.input_password.pack(padx=10, pady=12)

        self.prijava = ctk.CTkButton(master=self.login, text='Login', command=self.login_event)
        self.prijava.pack(padx=10, pady=12)

        #login is possible with Enter key
        self.login.bind('<Return>', lambda event: self.login_event())
        #Quit with ESC key
        self.login.bind('<Escape>', lambda quit: self.quit())

    def login_event(self):
        input_name = self.input_username.get()
        input_password = self.input_password.get()
        if self.user.check_user(input_name, input_password):
            print('Successful login!')
            self.login.quit()
            self.login.destroy()
            self.authentication = True
        else:
            messagebox.showerror('PyFloraPots - Error', 'The username does not exist or the password is wrong, try again!')
    
    def run(self):
        self.login.mainloop()

class PyF_main_menu(ctk.CTk):
    def __init__(self, user):
        super().__init__()
        global pots_location
        self.user = user
        self.db = DBHandler()
        self.sensors = Sensor()
        self.plots = PyF_plots()
        self.meas = Meas()
        self.filemngr = FileMngr()
        self.meteo_app = Meteo()

        #Main screen initialization
        self.root = ctk.CTkToplevel()
        self.root.title('PyFloraApp')
        self.root.geometry("1200x750")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.bind('<Escape>', lambda quit: self.quit_event)
        self.root.protocol("WM_DELETE_WINDOW", self.quit_event) # X button event
        
        self.navigation_frm()

        self.welcome_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.welcome_frame.grid(row=0, column=1, sticky="nsew")
        self.welcome_frame.grid_columnconfigure(0, weight=1)
        self.welcome_frame_label = ctk.CTkLabel(self.welcome_frame, text="Welcome to PyFloraPots!", font=('Roboto', 28))
        self.welcome_frame_label.grid(row=1, column=0, padx=20, pady=20, sticky='s', columnspan=4)
        self.welcome_frame.grid_rowconfigure(1, weight=2)
        foto_path = 'PyFloraPots/foto/!plant-pot.jpeg'
        self.welcome_img = ctk.CTkImage(Image.open(foto_path), size=(200,200))
        self.welcome_img = ctk.CTkLabel(self.welcome_frame, text='', image=self.welcome_img)
        self.welcome_img.grid(row=2, column=0, padx=20, pady=10, sticky='n', columnspan=4)
        self.welcome_frame.grid_rowconfigure(2, weight=2)

        #Initialize frames
        self.profile_frm()
        self.pot_frm()
        self.plant_frm()
        self.meas_frm()
        
    def quit_event(self): #EXIT THE PROGRAM
        if messagebox.askokcancel("PyFloraPots - Exit", "Exit PyFloraPots?"):
            plt.close('all')
            quit()

    def navigation_frm(self): #NAVIGATION FRAME
        def foto_path(img):
            return f'PyFloraPots/foto/{img}.jpeg'

        self.navigation_frame = ctk.CTkFrame(self.root, corner_radius=0, border_color='gray10')
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="PyFloraPots \n Menu", 
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.pot_img = ctk.CTkImage(Image.open(foto_path('!pot')), size=(20,20))
        self.pots_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Pots",
                                                      fg_color="transparent", text_color="gray10", hover_color="gray70",
                                                       anchor="w", font=('Calibri',20), compound="left", image=self.pot_img, 
                                                       command=lambda: self.select_frame('pots'))
        self.pots_button.grid(row=1, column=0, sticky="ew")

        self.plant_img = ctk.CTkImage(Image.open(foto_path('!plant')), size=(20,20))
        self.plants_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Plants",
                                                      fg_color="transparent", text_color="gray10", hover_color="gray70",
                                                       anchor="w", font=('Calibri',20), compound="left", image=self.plant_img,
                                                       command=lambda: self.select_frame('plants'))
        self.plants_button.grid(row=2, column=0, sticky="ew")

        self.meas_img = ctk.CTkImage(Image.open(foto_path('!graph')), size=(20,20))
        self.meas_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Logging",
                                                      fg_color="transparent", text_color="gray10", hover_color="gray70",
                                                       anchor="w", font=('Calibri',20), compound="left", image=self.meas_img,
                                                       command=lambda: self.select_frame('measurements'))
        self.meas_button.grid(row=3, column=0, sticky="ew")

        self.profile_img = ctk.CTkImage(Image.open(foto_path('!profile')), size=(20,20))
        self.profile_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="My profile",
                                                      fg_color="transparent", text_color="gray10", hover_color="gray70",
                                                       anchor="w", font=('Calibri',20), compound="left", image=self.profile_img,
                                                       command=lambda: self.select_frame('profile'))
        self.profile_button.grid(row=4, column=0, sticky="ew")

        self.quit_img = ctk.CTkImage(Image.open(foto_path('!quit')), size=(20,20))
        self.quit_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Exit",
                                                      fg_color="transparent", text_color="gray10", hover_color="gray70",
                                                       anchor="w", font=('Calibri',20), compound="left", image=self.quit_img,
                                                       command=self.quit_event)
        self.quit_button.grid(row=5, column=0, sticky="ew")

        self.quit_window = None
    
    def select_frame(self, name): #SELECT TAB
        if self.welcome_frame.winfo_exists:
            self.welcome_frame.destroy()

        self.pots_button.configure(fg_color="gray75" if name == "pots" else "transparent")
        self.plants_button.configure(fg_color="gray75" if name == "plants" else "transparent")
        self.profile_button.configure(fg_color="gray75" if name == "profile" else "transparent")
        self.meas_button.configure(fg_color="gray75" if name == "measurements" else "transparent")

        if name == "pots":
            self.pots_frame.grid(row=0, column=1, sticky="nsew")
        else:
            plt.close('all')
            self.pots_frame.grid_forget()
        if name == "plants":
            self.plants_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.plants_frame.grid_forget()
        if name == "profile":
            self.profile_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.profile_frame.grid_forget()  
        if name == "measurements":
            self.meas_frame.grid(row=0, column=1, sticky="nsew")
        else:
            plt.close('all')
            self.meas_frame.grid_forget()

    def refresh(self): #REFRESH FRAMES
        self.pot_frm()
        self.plant_frm()
        self.meas_frm()
        self.profile_frm()

    def sensor_reading_event(self): #SYNC ALL POTS
        self.db.store_sync_data_all()
        self.refresh()
        self.select_frame('pots')

    def manage_pot(self, id_number): #open window for manageing pot
        pot_root = ctk.CTkToplevel()
        pot_root.title('PyFloraApp - Manage pot')
        pot_root.geometry("950x750")
        pot_root.grab_set()

        global new_foto_path
        pot = self.db.read_pot(id_number)
        pot_label_text = pot.location # type: ignore
        plant = self.db.read_plant(pot.plant_id) # type: ignore
        plant_tbl = self.db.read_plant_tbl()
        plant_names = [plant_name.name for plant_name in plant_tbl]
        new_foto_path = None

        def exit_pot():
            plt.close('all')
            pot_root.grab_release()
            time.sleep(0.2)
            pot_root.destroy()
            self.refresh()
            self.select_frame('pots')
        
        def change_foto():
            change_foto_frame = ctk.CTkToplevel()
            change_foto_frame.title('PyFloraApp - Manage pot')
            change_foto_frame.geometry("500x160")
            change_foto_frame.grab_set()

            current_foto_path_lbl = ctk.CTkLabel(change_foto_frame, text="Current path: ", font=('Roboto', 14))
            current_foto_path_lbl.grid(row=0, column=0, padx=10, pady=5, sticky='e')
            current_foto_path = ctk.CTkTextbox(change_foto_frame, width=300, height=20, font=('Roboto', 12), fg_color="gray80", text_color="gray20", activate_scrollbars=False)
            current_foto_path.grid(row=0, column=1, padx=10, pady=5, sticky='w')

            if plant:
                current_foto_path.insert('0.0', pot.plant.foto) # type: ignore
            else:
                current_foto_path.insert('0.0', 'Path is incorrect or does not exist!')
            current_foto_path.configure(state='disabled')

            new_foto_path_lbl = ctk.CTkLabel(change_foto_frame, text="New path: ", font=('Roboto', 14))
            new_foto_path_lbl.grid(row=1, column=0, padx=10, pady=5, sticky='e')
            new_foto_path_input = ctk.CTkTextbox(change_foto_frame, width=300, height=20, font=('Roboto', 12), activate_scrollbars=False)
            new_foto_path_input.grid(row=1, column=1, padx=10, pady=5, sticky='w')
            
            def accept():
                new_foto_path = new_foto_path_input.get('0.0','end-1c')
                try:
                    image = ctk.CTkImage(Image.open(new_foto_path), size=(160,200))
                    if plant:
                        self.db.update_foto_path(pot.id_number,new_foto_path) # type: ignore
                    cancel()
                except:
                    print('The photo cannot be opened or the path is wrong!')
                
            def cancel():
                change_foto_frame.grab_release()
                time.sleep(0.2)
                change_foto_frame.destroy()
            
            accept_foto_path_btn = ctk.CTkButton(change_foto_frame, text="Accept", command=accept)
            accept_foto_path_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
            cancel_foto_path_btn = ctk.CTkButton(change_foto_frame, text="Cancel", command=cancel)
            cancel_foto_path_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=5)  

        #TITLE BAR
        'undefined location' if pot_label_text is None else pot_label_text
        pot_label = ctk.CTkLabel(pot_root, text=f"{pot_label_text}", font=('Roboto', 20))
        pot_label.pack(padx=10, pady=10)
        pot_exit = ctk.CTkButton(pot_root, width=75, height=25, text="Close", command=exit_pot)
        pot_exit.pack(padx=10, pady=0, anchor='e')

        #CONTENT FRAME
        content_frame = ctk.CTkFrame(pot_root)
        content_frame.pack(padx=5, pady=10, anchor='n', side='left', fill='both')
        try:
            foto_path = pot.plant.foto # type: ignore
            image = ctk.CTkImage(Image.open(foto_path), size=(160,200))
        except:
            foto_path = 'PyFloraPots/foto/question_mark.jpeg'
            image = ctk.CTkImage(Image.open(foto_path), size=(160,200)) 
        foto = ctk.CTkButton(content_frame, width=180, height=220, text='', image=image, command=change_foto)
        foto.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='n')
        foto.configure(state='disabled')

        pot_id_label = ctk.CTkLabel(content_frame, text="Pot ID: ", font=('Roboto', 14))
        pot_id_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')
        pot_id = ctk.CTkTextbox(content_frame, width=50, height=20, font=('Roboto', 12), fg_color="gray80", text_color="gray20", activate_scrollbars=False)
        pot_id.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        pot_id.insert('0.0', pot.id_number) # type: ignore
        pot_id.configure(state='disabled')

        pot_location_label = ctk.CTkLabel(content_frame, text="Pot location: ", font=('Roboto', 14))
        pot_location_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
        pot_location = ctk.CTkTextbox(content_frame, width=150, height=20, font=('Roboto', 12), fg_color="gray80", text_color="gray20", activate_scrollbars=False)
        pot_location.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        if pot.location is None: # type: ignore
            pot_location.insert('0.0', 'undefined')
        else:
            pot_location.insert('0.0', pot.location) # type: ignore
        pot_location.configure(state='disabled')

        pot_plant_id_name_label = ctk.CTkLabel(content_frame, text="Plant name: ", font=('Roboto', 14))
        pot_plant_id_name_label.grid(row=3, column=0, padx=10, pady=5, sticky='e')
        pot_plant_id_name = ctk.CTkComboBox(content_frame, values=plant_names, width=150, height=20, font=('Roboto', 12), fg_color="gray80", text_color="gray20") # type: ignore
        pot_plant_id_name.grid(row=3, column=1, padx=10, pady=5, sticky='w')
        if pot.plant_id is None: # type: ignore
            pot_plant_id_name.set('empty pot')
        else:
            pot_plant_id_name.set(plant.name) # type: ignore
        pot_plant_id_name.configure(state='disabled')

        def change():
            pot_change_btn.configure(state='disabled')
            foto.configure(state='normal')
            pot_location.configure(fg_color="white", state='normal')
            pot_plant_id_name.configure(fg_color="white", state='normal')
            pot_accept_btn.configure(state='normal')
            pot_cancel_btn.configure(state='normal')

        def accept():
            location = pot_location.get('0.0','end-1c')
            plant_name = pot_plant_id_name.get()        
            if location == '':
                location = 'undefined location' 
            if plant_name == 'empty pot':
                plant_name = None
            else:
                plant_to_save_id = self.db.find_plant_id_by_name(plant_name)
                if plant_to_save_id is not None:
                    self.db.update_pot(id_number, plant_to_save_id[0], location)

                    pot_status = self.db.read_status_row(id_number)
                    datetimestamp = datetime.datetime.now()
                    file_path = f"PyFloraPots/pot_data_id_{id_number}.csv"
                    file_writer = FileMngr.openFileForWriting(self.filemngr, file_path)
                    file_writer.write(f"datetime,vwc,ph,sal,lux\n") # type: ignore
                    file_writer.write(f"{datetimestamp},{pot_status.vwc},{pot_status.ph},{pot_status.sal},{pot_status.lux}\n") # type: ignore
                    file_writer.close() # type: ignore

                    if new_foto_path is not None:
                        self.db.update_foto_path(id_number, new_foto_path)
                        new_image = ctk.CTkImage(Image.open(new_foto_path), size=(160,200))
                        foto.configure(state='disabled', image=new_image)
                    else:
                        try:
                            foto_path = pot.plant.foto # type: ignore
                            foto.configure(state='disabled')
                        except:
                            foto_path = 'PyFloraPots/foto/question_mark.jpeg'
                            new_image = ctk.CTkImage(Image.open(foto_path), size=(160,200))
                            foto.configure(state='disabled', image=new_image)
                refresh_status_frame()
                print('Changes recorded successfully!')
                #PyFloraPots/foto/test_foto.jpeg
            time.sleep(0.2)
            pot_id.configure(fg_color="gray80", text_color="gray20", state='disabled')
            pot_location.configure(fg_color="gray80", text_color="gray20", state='disabled')
            pot_plant_id_name.configure(fg_color="gray80", text_color="gray20", state='disabled')
            pot_change_btn.configure(state='normal')
            pot_accept_btn.configure(state='disabled') 
            pot_cancel_btn.configure(state='disabled')

        def cancel():
            pot_location.delete('0.0','end')
            pot = self.db.read_pot(id_number)
            plant = self.db.read_plant(pot.plant_id) # type: ignore
            try:
                pot_location.insert('0.0', pot.location) # type: ignore
                pot_plant_id_name.set(plant.name) # type: ignore
            except:
                pot_location.delete('0.0','end')
                pot_location.insert('0.0', 'undefined location')
                pot_plant_id_name.set('empty pot')
                
            pot_id.configure(fg_color="gray80", text_color="gray20", state='disabled')
            pot_location.configure(fg_color="gray80", text_color="gray20", state='disabled')
            pot_plant_id_name.configure(fg_color="gray80", text_color="gray20", state='disabled')
            pot_change_btn.configure(state='normal')
            pot_accept_btn.configure(state='disabled')
            pot_cancel_btn.configure(state='disabled')
            foto.configure(state='disabled')
            print('Cancelled!')

        def empty_pot():
            if messagebox.askokcancel("PyFloraPots - Pot emptying", "Emptying the pot will erase the measurements. Continue?"):
                pot_plant_id_name.set('empty pot')
                self.db.empty_pot(id_number)
                foto_path = 'PyFloraPots/foto/question_mark.jpeg'
                image = ctk.CTkImage(Image.open(foto_path), size=(160,200))
                foto = ctk.CTkButton(content_frame, width=180, height=220, text='', image=image)
                foto.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='n')
                refresh_status_frame('empty_pot')
                file_path = f"PyFloraPots/pot_data_id_{id_number}.csv"
                self.filemngr.deleteCSVFile(file_path)
                exit_pot()
            
        def delete_pot():
            if messagebox.askokcancel("PyFloraPots - Pot deleting", "You are about to delete the pot. Continue?"):
                self.db.delete_pot(id_number)
                exit_pot()

        pot_change_btn = ctk.CTkButton(content_frame, text="Change", command=change)
        pot_accept_btn = ctk.CTkButton(content_frame, text="Accept", command=accept)
        pot_cancel_btn = ctk.CTkButton(content_frame, text="Cancel", command=cancel)
        pot_empty_btn = ctk.CTkButton(content_frame, text="Empty pot", command=empty_pot)
        pot_delete_btn = ctk.CTkButton(content_frame, text="Delete pot", command=delete_pot)
        row=6
        pot_change_btn.grid(row=row, column=0, columnspan=2, padx=10, pady=5)
        pot_accept_btn.grid(row=row+1, column=0, columnspan=2, padx=10, pady=5)
        pot_cancel_btn.grid(row=row+2, column=0, columnspan=2, padx=10, pady=5)
        pot_empty_btn.grid(row=row+3, column=0, columnspan=2, padx=10, pady=5)
        pot_delete_btn.grid(row=row+4, column=0, columnspan=2, padx=10, pady=5)
        pot_accept_btn.configure(state='disabled')
        pot_cancel_btn.configure(state='disabled')
        if pot.plant_id is None: # type: ignore
            pot_empty_btn.configure(state='disabled')

        #STATUS FRAME
        status_frame = ctk.CTkFrame(pot_root)
        status_frame.pack(padx=5, pady=10, anchor='n', side='left', fill='both', expand=True)

        def sync():
            plt.close('all')
            self.db.store_sync_data(id_number)
            refresh_status_frame('default')  

        status_main_label = ctk.CTkLabel(status_frame, text="Status:", font=('Roboto', 16))
        status_main_label.grid(row=0, column=0, padx=10, pady=5, sticky='ew')

        sync_btn = ctk.CTkButton(status_frame, width=75, height=25, text="Sync", command=sync)
        sync_btn.grid(row=0, column=1, padx=10, pady=5, sticky='e')

        status_labels = ['VWC: ','pH: ','Salinity: ','Light: ']
        status_units = ['%','',' mS/cm',' lux']

        def refresh_status_frame(action='default'):
            if action == 'default':
                status_val_tuple = self.db.read_status_values(id_number)
            elif action == 'empty_pot':
                status_val_tuple = None
            row, col = 1, 0
            for i in range(4):
                plot_frame = ctk.CTkFrame(status_frame)
                plot_frame.grid(row=row, column=col, padx=5, pady=5)
                status_lbl = ctk.CTkLabel(plot_frame, text=f"{status_labels[i]}", font=('Roboto', 14))
                status_lbl.grid(row=0, column=0, padx=10, pady=5, sticky='e')
                status_val = ctk.CTkTextbox(plot_frame, width=75, height=20, font=('Roboto', 12), fg_color="gray70", text_color="gray10", activate_scrollbars=False)
                status_val.grid(row=0, column=1, padx=10, pady=5, sticky='w')
                if status_val_tuple:
                    status_val.insert('0.0', f'{status_val_tuple[i]}{status_units[i]}')
                    status_list = self.db.plant_care_status(status_val_tuple[0],status_val_tuple[1],status_val_tuple[2],status_val_tuple[3])
                    status_text = f'{status_list[i]}'
                    df = self.meas.read_csv(id_number)
                    fig = self.plots.line_plt(df)[i]
                    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
                    canvas.draw()
                    canvas.get_tk_widget().grid(row=2, column=0, ipadx=30, ipady=30, padx=10, pady=10, columnspan=2, sticky='nsew')
                else:
                    status_val.insert('0.0', '')
                    status_text = ''
                status_val.configure(state='disabled')
                status_notif = ctk.CTkLabel(plot_frame, text=status_text, font=('Roboto', 12))
                status_notif.grid(row=1, column=0, padx=10, pady=5, columnspan=2, sticky='w')
                col += 1
                if col % 2 == 0:
                    row += 1
                    col = 0
        
        refresh_status_frame()

    class Pot_box(ctk.CTkFrame): #SHOW POT BOXES
        def __init__(self, master, id_number):
            super().__init__(master)
            self.db = DBHandler()
            id_number = id_number
            pot = self.db.read_pot(id_number)
            location = pot.location  # type: ignore
            if location is None:
                location = 'Undefined location'
            
            self.location_lbl = ctk.CTkLabel(self, text=f'{location}', font=('Roboto', 16))
            self.location_lbl.pack(padx=10, pady=5)

            try:
                plant_name = pot.plant.name  # type: ignore
                vwc,ph,sal,lux = self.db.read_status_values(id_number)
                status_list = self.db.plant_care_status(vwc,ph,sal,lux)
            except:
                plant_name = 'empty pot'
                status_list = ''

            try:
                foto_path = pot.plant.foto  # type: ignore
                image = ctk.CTkImage(Image.open(foto_path), size=(80,100))
            except:
                foto_path = 'PyFloraPots/foto/question_mark.jpeg'
                image = ctk.CTkImage(Image.open(foto_path), size=(80,100))

            self.foto = ctk.CTkButton(self, width=80, height=100, text='', image=image)
            self.foto.pack(padx=10, pady=10, side='left', anchor='n')
            self.foto.bind("<Button-1>", lambda event, id_number=id_number, foto_path=foto_path: main_menu_app.manage_pot(id_number))

            self.plant = ctk.CTkLabel(self, text=f'{plant_name}', font=('Roboto', 12))
            self.plant.pack(padx=10, pady=0, anchor='n')

            for i in range(len(status_list)):
                self.status_label = ctk.CTkLabel(self, text=f'{status_list[i]}', font=('Roboto', 10))
                self.status_label.pack(padx=10, pady=0, anchor='w')

    def pot_frm(self):
        global pots_location
        def datetime_clock():
            global meteo_app
            datetime_ = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
            pots_location = self.profile_location.get()
            self.current_datetime.configure(text=f"{datetime_}\n{pots_location} {self.meteo_app.stations[pots_location]}°C") 
            self.after(60000, datetime_clock)

        def create_pot_event():
            self.db.create_pot()
            print('Empty PyPot created!')
            self.refresh()
            self.select_frame('pots')

        pot_table = self.db.read_pot_tbl()

        self.pots_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.pots_frame.grid_columnconfigure(0, weight=1)
        self.pots_frame_label = ctk.CTkLabel(self.pots_frame, text="PyPots", font=('Roboto', 20))
        self.pots_frame_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky='ew')
        datetime_ = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        pots_location = self.profile_location.get()
        self.current_datetime = ctk.CTkButton(self.pots_frame, width=30, height=60, 
                                              text=f"{datetime_}\n{pots_location} {self.meteo_app.stations[pots_location]}°C", 
                                              font=('Roboto', 16), text_color='gray10', fg_color="#8B8B65", state='disabled')
        self.current_datetime.grid(row=0, column=2, padx=10, pady=10, sticky="ew", ipady=0)
        self.current_datetime.after(1000, datetime_clock)

        btn_width=100
        self.btns_frame = ctk.CTkFrame(self.pots_frame, corner_radius=0, fg_color="gray80")
        self.btns_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew', columnspan=3)
        self.add_pot = ctk.CTkButton(self.btns_frame, width=btn_width, text='Add new pot', command=create_pot_event)
        self.add_pot.pack(padx=10, pady=10, side='left')
        self.sensor_reading_button = ctk.CTkButton(self.btns_frame, width=btn_width, text="SYNC", command=self.sensor_reading_event)
        self.sensor_reading_button.pack(padx=10, pady=10, side='left')

        self.pots_frame.grid_columnconfigure(0, weight=1, uniform='potfrm')
        self.pots_frame.grid_columnconfigure(1, weight=1, uniform='potfrm')
        self.pots_frame.grid_columnconfigure(2, weight=1, uniform='potfrm')

        row, col = 2, 0
        for pot_row in pot_table:
            pot_box = self.Pot_box(self.pots_frame, id_number=pot_row.id_number)
            if col % 3 == 0:
                row += 1
                col = 0
            pot_box.grid(row=row, column=col, padx=10, pady=10, sticky='ew')                
            col += 1  

    def manage_plant(self, id_number, foto_path): #Open window for updateing plant
        plant_root = ctk.CTkToplevel()
        plant_root.title('PyFloraApp - Manage plant')
        plant_root.geometry("700x340")
        plant_root.attributes("-topmost", True)
        plant_root.grab_set()

        plant = self.db.read_plant(id_number)

        plant_label = ctk.CTkLabel(plant_root, text=f"Manage plant {id_number}", font=('Roboto', 20))
        plant_label.pack(padx=10, pady=5)

        image = ctk.CTkImage(Image.open(foto_path), size=(160,200)) 
        foto = ctk.CTkButton(plant_root, width=160, height=200, text='', image=image, state='disabled')
        foto.pack(padx=10, pady=10, anchor='n', side='left', fill='y', expand=True)

        content_frame = ctk.CTkFrame(plant_root)
        content_frame.pack(padx=5, pady=10, anchor='n', side='right', fill='both', expand=True)

        plant_id_label = ctk.CTkLabel(content_frame, text="Plant ID: ", font=('Roboto', 14))
        plant_id_label.grid(row=0, column=0, padx=5, pady=10, sticky='e')
        plant_id = ctk.CTkTextbox(content_frame, width=50, height=20, font=('Roboto', 12), fg_color="gray80", text_color="gray20", activate_scrollbars=False)
        plant_id.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        plant_id.insert('0.0', plant.id_number) # type: ignore
        plant_id.configure(state='disabled')

        plant_name_label = ctk.CTkLabel(content_frame, text="Plant name: ", font=('Roboto', 14))
        plant_name_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')
        plant_name = ctk.CTkTextbox(content_frame, width=200, height=20, font=('Roboto', 12), fg_color="gray80", text_color="gray20", activate_scrollbars=False)
        plant_name.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        if plant.name is None: # type: ignore
            plant_name.insert('0.0', 'nedefinirano')
        else:
            plant_name.insert('0.0', plant.name) # type: ignore
        plant_name.configure(state='disabled')

        plant_foto_label = ctk.CTkLabel(content_frame, text="Photo path: ", font=('Roboto', 14))
        plant_foto_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
        plant_foto_path = ctk.CTkTextbox(content_frame, width=300, height=20, font=('Roboto', 12), fg_color="gray80", text_color="gray20", activate_scrollbars=False)
        plant_foto_path.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        if plant.foto is None: # type: ignore
            plant_foto_path.insert('0.0', 'Path does not exist!')
        else:
            plant_foto_path.insert('0.0', plant.foto) # type: ignore
        plant_foto_path.configure(state='disabled')

        def change():
            plant_change_btn.configure(state='disabled')
            plant_name.configure(fg_color="white", state='normal')
            plant_foto_path.configure(fg_color="white", state='normal')
            plant_accept_btn.configure(state='normal')
            plant_cancel_btn.configure(state='normal')

        def accept():
            name = plant_name.get('0.0','end-1c')
            foto_path = plant_foto_path.get('0.0','end-1c')
            
            if name == '':
                name = 'undefined name'
            if foto_path == '':
                foto_path = None
                
            self.db.update_plant(plant.id_number, name, foto_path) # type: ignore
            time.sleep(0.2)
            plant_id.configure(fg_color="gray80", text_color="gray20", state='disabled')
            plant_name.configure(fg_color="gray80", text_color="gray20", state='disabled')
            plant_foto_path.configure(fg_color="gray80", text_color="gray20", state='disabled')
            plant_change_btn.configure(state='normal')
            plant_accept_btn.configure(state='disabled')

            print('Changes recorded successfully!')
            plant_root.grab_release()
            time.sleep(0.2)
            plant_root.destroy()
            self.refresh()
            self.select_frame('plants')

        def cancel():
            plant_name.delete('0.0','end')
            plant_foto_path.delete('0.0','end')
            plant_name.insert('0.0', plant.name) # type: ignore
            if plant.foto is None: # type: ignore
                plant_foto_path.insert('0.0', 'path does not exist!')
            else:
                plant_foto_path.insert('0.0', plant.foto) # type: ignore
            plant_id.configure(fg_color="gray80", text_color="gray20", state='disabled')
            plant_name.configure(fg_color="gray80", text_color="gray20", state='disabled')
            plant_foto_path.configure(fg_color="gray80", text_color="gray20", state='disabled')
            plant_change_btn.configure(state='normal')
            plant_accept_btn.configure(state='disabled')
            print('Cancelling!')
            plant_root.grab_release()
            time.sleep(0.2)
            plant_root.destroy()
            self.refresh()
            self.select_frame('plants')
            
        def delete_plant():
            if messagebox.askokcancel("PyFloraPots - Pot deleting", "You are about to delete the plant. Continue?"):
                self.db.delete_plant(id_number)
                print(f'Plant {id_number} deleted!')
                plant_root.grab_release()
                time.sleep(0.2)
                plant_root.destroy()
                self.refresh()
                self.select_frame('plants')

        plant_change_btn = ctk.CTkButton(content_frame, text="Change", command=change)
        plant_change_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        plant_accept_btn = ctk.CTkButton(content_frame, text="Accept", command=accept)
        plant_accept_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        plant_accept_btn.configure(state='disabled')
        plant_cancel_btn = ctk.CTkButton(content_frame, text="Cancel", command=cancel)
        plant_cancel_btn.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
        plant_cancel_btn.configure(state='disabled')
        plant_delete_btn = ctk.CTkButton(content_frame, text="Delete plant", command=delete_plant)
        plant_delete_btn.grid(row=8, column=0, columnspan=2, padx=10, pady=5)
        plant_root.mainloop()

    class Plant_box(ctk.CTkFrame):
        def __init__(self, master, id_number, name, foto_path):
            super().__init__(master)
            self.id_number = id_number
            self.name = name
            try:
                image = ctk.CTkImage(Image.open(foto_path), size=(80,100)) 
            except:
                foto_path = 'PyFloraPots/foto/question_mark.jpeg'
                image = ctk.CTkImage(Image.open(foto_path), size=(80,100))
            self.name_label = ctk.CTkLabel(self, text=f'{name}', font=('Roboto', 16))
            self.name_label.pack(padx=10, pady=10)
            self.foto = ctk.CTkButton(self, width=80, height=100, text='', image=image, state='disabled')
            self.foto.pack(padx=10, pady=10)
            self.foto.bind("<Button-1>", lambda event, id_number=id_number, foto_path=foto_path: main_menu_app.manage_plant(id_number, foto_path))

    def plant_frm(self): #PLANTS TAB       
        def create_plant_event():
            crp_root = ctk.CTkToplevel()
            crp_root.title('PyFloraApp - Create new plant')
            crp_root.geometry("500x150")
            crp_root.attributes("-topmost", True)

            crp_label = ctk.CTkLabel(self.profile_frame, text="Add new plant", font=('Roboto', 20))
            crp_label.grid(row=0, column=0, padx=0, pady=10, sticky='ew', columnspan=2)

            crp_name_label = ctk.CTkLabel(crp_root, text="Plant name: ", font=('Roboto', 12))
            crp_name_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
            crp_name = ctk.CTkEntry(crp_root, width=200, height=20, font=('Roboto', 12), fg_color="gray80", text_color="gray20")
            crp_name.grid(row=1, column=1, padx=10, pady=10, sticky='w')
            
            crp_foto_path_label = ctk.CTkLabel(crp_root, text="Photo path: ", font=('Roboto', 12))
            crp_foto_path_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
            crp_foto_path = ctk.CTkEntry(crp_root, width=200, height=20, font=('Roboto', 12), fg_color="gray80", text_color="gray20")
            crp_foto_path.grid(row=2, column=1, padx=10, pady=10, sticky='w')
            
            def accept():
                name = crp_name.get()
                foto_path = crp_foto_path.get()
                if name and foto_path is not None:
                    self.db.create_plant(name, foto_path) 
                else:
                    print('Empty entry!')
                time.sleep(0.1)
                crp_root.attributes("-topmost", False)
                crp_root.destroy()
                self.pot_frm()
                self.plant_frm()
                self.select_frame('plants')
                
            def cancel():
                print('Cancelled')
                time.sleep(0.1)
                crp_root.destroy()

            crp_accept_btn = ctk.CTkButton(crp_root, text="Accept", command=accept)
            crp_accept_btn.grid(row=3, column=0, padx=10, pady=10, columnspan=1)
            crp_cancel_btn = ctk.CTkButton(crp_root, text="Cancel", command=cancel)
            crp_cancel_btn.grid(row=3, column=1, padx=10, pady=10, columnspan=1)
            crp_root.mainloop()
        
        plant_table = self.db.read_plant_tbl()
        self.plants_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.plants_frame.grid_columnconfigure(0, weight=1)
        self.plants_frame_label = ctk.CTkLabel(self.plants_frame, text="Plants", font=('Roboto', 20))
        self.plants_frame_label.grid(row=0, column=0, padx=20, pady=20, sticky='ew', columnspan=3)
        self.add_plant = ctk.CTkButton(self.plants_frame, width=40, height=40, text='Add new plant', command=create_plant_event)
        self.add_plant.grid(row=0, column=3, padx=10, pady=10, sticky='ew')
        self.plants_frame.grid_columnconfigure(0, weight=1, uniform='plantfrm')
        self.plants_frame.grid_columnconfigure(1, weight=1, uniform='plantfrm')
        self.plants_frame.grid_columnconfigure(2, weight=1, uniform='plantfrm')
        self.plants_frame.grid_columnconfigure(3, weight=1, uniform='plantfrm')

        row, col = 2, 0
        for plant_row in plant_table:
            plant_box = self.Plant_box(self.plants_frame, id_number=plant_row.id_number, name=plant_row.name, foto_path=plant_row.foto)
            if col % 4 == 0:
                row += 1
                col = 0
            plant_box.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            col += 1                

    def meas_frm(self):
        self.meas_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.meas_frame.grid_columnconfigure(0, weight=1)
        self.meas_frame.grid_columnconfigure(1, weight=1)

        meas_frame_label = ctk.CTkLabel(self.meas_frame, text="Measurements", font=('Roboto', 20))
        meas_frame_label.grid(row=0, column=0, padx=20, pady=20, sticky='ew', columnspan=2)

        meas_btns_frame = ctk.CTkFrame(self.meas_frame, corner_radius=0, fg_color="gray80")
        meas_btns_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew', columnspan=2)

        def reset_data_manager():
            self.sensors.sensor_data_manager()
            print('Data tables reset!')
            
        reset_record_btn = ctk.CTkButton(meas_btns_frame, width=100, text="Reset", command=reset_data_manager)
        reset_record_btn.pack(padx=10, pady=10, side='left')

        interval_lbl = ctk.CTkLabel(meas_btns_frame, width=100, text="Set interval (sec): ")
        interval_lbl.pack(padx=10, pady=10, side='left')
        interval_txt = ctk.CTkTextbox(meas_btns_frame, width=40, height=20, font=('Roboto', 12), fg_color="white", activate_scrollbars=False)
        interval_txt.pack(padx=10, pady=10, side='left')
        interval_txt.insert('0.0', 5)

        def start_recording_event():
            try:
                interval = int(interval_txt.get('0.0','end-1c'))
                self.sensors.define_interval(interval)
                self.sensors.start_recording()
                start_record_btn.configure(state='disabled')
                stop_record_btn.configure(state='normal')
            except:
                print('The entered interval is not correct!')
        
        def stop_recording_event():
            self.sensors.stop_recording()
            stop_record_btn.configure(state='disabled')
            start_record_btn.configure(state='normal')
        
        def plot_meas():
            pot_table = self.db.read_pot_tbl()
            for pot in pot_table:
                status_val_tuple = self.db.read_status_values(pot.id_number)
                if status_val_tuple:
                    meas_tabs.add(f"Pot {pot.id_number}")
                    df = self.meas.read_csv(pot.id_number)
                    df.datetime
                    figs = self.plots.line_plt(df)
                    row, col = 0, 0
                    for i in range(4):
                        fig = figs[i]
                        fig.set_figwidth(4)
                        fig.set_figheight(3)
                        canvas = FigureCanvasTkAgg(fig, master=meas_tabs.tab(f"Pot {pot.id_number}"))
                        canvas.draw()
                        canvas.get_tk_widget().grid(row=row, column=col, padx=10, pady=10, sticky='ew')
                        col += 1
                        if col % 2 == 0:
                            row += 1
                            col = 0
                plt.close('all')
        
        def refresh_tabs():
            pot_table = self.db.read_pot_tbl()
            for pot in pot_table:
                meas_tabs.delete(f"Pot {pot.id_number}")
            plot_meas()

        start_record_btn = ctk.CTkButton(meas_btns_frame, width=100, text="Start", command=start_recording_event)
        start_record_btn.pack(padx=10, pady=10, side='left')
        stop_record_btn = ctk.CTkButton(meas_btns_frame, width=100, text="Stop", command=stop_recording_event)
        stop_record_btn.pack(padx=10, pady=10, side='left')
        stop_record_btn.configure(state='disabled')
        refresh_btn = ctk.CTkButton(meas_btns_frame, width=100, text="Reload graphs", command=refresh_tabs)
        refresh_btn.pack(padx=10, pady=10, side='left')
        meas_tabs = ctk.CTkTabview(self.meas_frame)
        meas_tabs.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
        plot_meas()

    def profile_frm(self): #MY PROFILE TAB
        global pots_location

        self.profile_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.profile_frame.grid_columnconfigure(0, weight=1)
        self.profile_frame.grid_columnconfigure(1, weight=1)
        
        self.profile_frame_label = ctk.CTkLabel(self.profile_frame, text="My profile", font=('Roboto', 20))
        self.profile_frame_label.grid(row=0, column=0, padx=20, pady=20, sticky='ew', columnspan=2)

        self.profile_name_label = ctk.CTkLabel(self.profile_frame, text="Name: ", font=('Roboto', 12))
        self.profile_name_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.profile_name = ctk.CTkTextbox(self.profile_frame, width=120, height=20, font=('Roboto', 12), 
                                           fg_color="gray80", text_color="gray20", activate_scrollbars=False)
        self.profile_name.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.profile_name.insert('0.0', self.user.name)
        self.profile_name.configure(state='disabled')

        self.profile_surname_label = ctk.CTkLabel(self.profile_frame, text="Surname: ", font=('Roboto', 12))
        self.profile_surname_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.profile_surname = ctk.CTkTextbox(self.profile_frame, width=120, height=20, font=('Roboto', 12), 
                                              fg_color="gray80", text_color="gray20", activate_scrollbars=False)
        self.profile_surname.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.profile_surname.insert('0.0', self.user.surname)
        self.profile_surname.configure(state='disabled')

        self.profile_username_label = ctk.CTkLabel(self.profile_frame, text="Username: ", font=('Roboto', 12))
        self.profile_username_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.profile_username = ctk.CTkTextbox(self.profile_frame, width=120, height=20, font=('Roboto', 12), 
                                               fg_color="gray80", text_color="gray20", activate_scrollbars=False)
        self.profile_username.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        self.profile_username.insert('0.0',self.user.username)
        self.profile_username.configure(state='disabled')

        self.profile_password_label = ctk.CTkLabel(self.profile_frame, text="Password: ", font=('Roboto', 12))
        self.profile_password_label.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.profile_password = ctk.CTkTextbox(self.profile_frame, width=120, height=20, font=('Roboto', 12), 
                                               fg_color="gray80", text_color="gray20", activate_scrollbars=False)
        self.profile_password.grid(row=4, column=1, padx=10, pady=10, sticky='w')
        self.profile_password.insert('0.0',self.user.password)
        self.profile_password.configure(state='disabled')

        self.profile_location_label = ctk.CTkLabel(self.profile_frame, text="Weather station\nlocation: ", font=('Roboto', 12))
        self.profile_location_label.grid(row=5, column=0, padx=10, pady=10, sticky='e')
        station_list = list(self.meteo_app.stations)
        self.profile_location = ctk.CTkComboBox(self.profile_frame, values=station_list, width=120, 
                                                height=20, font=('Roboto', 12), fg_color="gray80", text_color="gray20") # type: ignore
        self.profile_location.set('Zagreb-Grič')
        self.profile_location.grid(row=5, column=1, padx=10, pady=10, sticky='w')
        self.profile_location.configure(state='disabled')

        def profile_change():
            self.profile_change_btn.configure(state='disabled')
            self.profile_name.configure(fg_color="white", state='normal')
            self.profile_surname.configure(fg_color="white", state='normal')
            self.profile_username.configure(fg_color="white", state='normal')
            self.profile_password.configure(fg_color="white", state='normal')
            self.profile_accept_btn.configure(state='normal')
            self.profile_cancel_btn.configure(state='normal')
            self.profile_location.configure(state='normal')

        def profile_accept():
            self.user.name = self.profile_name.get('0.0','end')
            self.user.surname = self.profile_surname.get('0.0','end')
            self.user.username = self.profile_username.get('0.0','end')
            self.user.password = self.profile_password.get('0.0','end')
            self.profile_name.configure(fg_color="gray80", text_color="gray20", state='disabled')
            self.profile_surname.configure(fg_color="gray80", text_color="gray20", state='disabled')
            self.profile_username.configure(fg_color="gray80", text_color="gray20", state='disabled')
            self.profile_password.configure(fg_color="gray80", text_color="gray20", state='disabled')
            self.profile_change_btn.configure(state='normal')
            self.profile_accept_btn.configure(state='disabled')
            self.profile_cancel_btn.configure(state='disabled')
            self.profile_location.configure(state='disabled')
            print('Changes recorded successfully!')

        def profile_cancel():
            self.profile_name.delete('0.0','end')
            self.profile_surname.delete('0.0','end')
            self.profile_username.delete('0.0','end')
            self.profile_password.delete('0.0','end')
            self.profile_name.insert('0.0',self.user.name)
            self.profile_surname.insert('0.0',self.user.surname)
            self.profile_username.insert('0.0',self.user.username)
            self.profile_password.insert('0.0',self.user.password)
            self.profile_name.configure(fg_color="gray80", text_color="gray20", state='disabled')
            self.profile_surname.configure(fg_color="gray80", text_color="gray20", state='disabled')
            self.profile_username.configure(fg_color="gray80", text_color="gray20", state='disabled')
            self.profile_password.configure(fg_color="gray80", text_color="gray20", state='disabled')
            self.profile_change_btn.configure(state='normal')
            self.profile_accept_btn.configure(state='disabled')
            self.profile_cancel_btn.configure(state='disabled')
            self.profile_location.configure(state='disabled')
            print('Cancelling!')

        self.profile_change_btn = ctk.CTkButton(self.profile_frame, text="Change", command=profile_change)
        self.profile_change_btn.grid(row=6, column=0, padx=10, pady=10, columnspan=2)
        self.profile_accept_btn = ctk.CTkButton(self.profile_frame, text="Accept", command=profile_accept, state='disabled')
        self.profile_accept_btn.grid(row=7, column=0, padx=10, pady=10, columnspan=2)
        self.profile_cancel_btn = ctk.CTkButton(self.profile_frame, text="Cancel", command=profile_cancel, state='disabled')
        self.profile_cancel_btn.grid(row=8, column=0, padx=10, pady=10, columnspan=2)

    def run(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    login_app = PyF_login()
    login_app.run()
    if login_app.authentication:
        main_menu_app = PyF_main_menu(login_app.user)
        main_menu_app.run()