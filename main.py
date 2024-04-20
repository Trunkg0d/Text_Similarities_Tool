from customtkinter import CTk, set_appearance_mode, CTkFrame, CTkLabel, CTkImage, CTkButton, END, CTkTextbox, \
    CTkRadioButton, CTkScrollableFrame
from CTkTable import CTkTable
from PIL import Image, ImageDraw
from models.model import Model
from numpy import array, any, where, uint8
from re import split
import tkinter as tk
import os


class CustomTkinterLabel(tk.Label):
    def __init__(self, master=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.config(font=("Arial", 12), bg="#ffffff")
class App(CTk):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.geometry("1150x850")

        self.resizable(0, 0)
        self.title("Identify text similarities application")
        set_appearance_mode("light")

        self.sidebar_frame = CTkFrame(master=self, fg_color="#2A8C55", width=176, height=650, corner_radius=0)
        self.sidebar_frame.pack_propagate(0)
        self.sidebar_frame.pack(fill="y", anchor="w", side="left")

        self.logo_img_data = Image.open("images/logo.png")
        self.width, self.height = self.logo_img_data.size
        size = (min(self.width, self.height), min(self.width, self.height))

        # self.logo_img_data = Image.open("images/remind.png")
        # width, height = self.logo_img_data.size
        # size = (min(width, height), min(width, height))

        # Create a mask in the shape of a circle
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)

        # Resize the original image to fit the circle
        logo_img_data = self.logo_img_data.resize(size)

        # Apply the circular mask to the image
        circular_image = Image.new("RGBA", size, (0, 0, 0, 0))
        circular_image.paste(logo_img_data, (0, 0), mask=mask)
        # logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(80, 80))
        logo_img = CTkImage(dark_image=circular_image, light_image=circular_image, size=(125, 125))

        CTkLabel(master=self.sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

        # self.logo_img = CTkImage(dark_image=self.logo_img_data, light_image=self.logo_img_data, size=(125, 125))
        # CTkLabel(master=self.sidebar_frame, text="", image=self.logo_img).pack(pady=(38, 0), anchor="center")

        # CTkLabel(master=sidebar_frame, text="Identify Text", font=("Arial Bold", 25), text_color="#fff").pack(pady=(38, 0), anchor="center")
        # CTkLabel(master=sidebar_frame, text="Similarity", font=("Arial Bold", 25), text_color="#fff").pack(pady=(5, 0), anchor="center")

        self.analytics_checked_img_data = Image.open("images/analytics_icon_checked.png")
        self.analytics_img_data = Image.open("images/analytics_icon.png")
        self.analytics_checked_img = CTkImage(dark_image=self.analytics_checked_img_data,
                                              light_image=self.analytics_checked_img_data)
        self.analytics_img = CTkImage(dark_image=self.analytics_img_data, light_image=self.analytics_img_data)
        self.dashboard_button = CTkButton(master=self.sidebar_frame, image=self.analytics_img, text="Dashboard",
                                          fg_color="transparent",
                                          font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.dashboard_button.pack(anchor="center", ipady=5, pady=(100, 0))

        # dashboard_button = CTkButton(master=sidebar_frame, image=analytics_img, text="Dashboard", fg_color="transparent",
        #                              font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        # dashboard_button.pack(anchor="center", ipady=5, pady=(100, 0))

        self.settings_img_data = Image.open("images/settings_icon.png")
        self.settings_img = CTkImage(dark_image=self.settings_img_data, light_image=self.settings_img_data)
        self.settings_img_checked_data = Image.open("images/settings_icon_checked.png")
        self.settings_checked_img = CTkImage(dark_image=self.settings_img_checked_data,
                                             light_image=self.settings_img_checked_data)
        self.setting_button = CTkButton(master=self.sidebar_frame, image=self.settings_img, text="Settings",
                                        fg_color="transparent",
                                        font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        # setting_button = CTkButton(master=sidebar_frame, image=settings_img, text="Settings", fg_color="transparent",
        #                            font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.setting_button.pack(anchor="center", ipady=5, pady=(16, 0), )
        self.about_img_data = Image.open("images/about.png")
        self.about_img = CTkImage(dark_image=self.about_img_data, light_image=self.about_img_data)

        self.about_checked_img_data = Image.open("images/about_checked.png")
        self.about_checked_img = CTkImage(dark_image=self.about_checked_img_data,
                                          light_image=self.about_checked_img_data)

        self.about_button = CTkButton(master=self.sidebar_frame, image=self.about_img, text="About",
                                      fg_color="transparent",
                                      font=("Arial Bold", 14),
                                      hover_color="#207244", anchor="w")
        self.about_button.pack(anchor="center", ipady=5, pady=(300, 0))

        #
        # main_view = CTkFrame(master=app, fg_color="#fff",  width=680, height=650, corner_radius=0)
        # main_view.pack_propagate(0)
        # main_view.pack(side="left")
        # grid = CTkFrame(master=main_view, fg_color="transparent")
        # grid.pack(fill="both", padx=27, pady=(31,0))
        # CTkTextbox(master=grid, fg_color="#F0F0F0", width=300, corner_radius=8).grid(row=3, column=1, rowspan=5, sticky="w", pady=(16, 0), padx=(25,0), ipady=10)

        self.main_view = CTkFrame(master=self, fg_color="#ffffff", width=2000, height=1000, corner_radius=0)
        self.main_view.pack_propagate(0)
        # self.main_view.pack(side="left")

        # self.intro_frame = CTkFrame(master=self.main_view, fg_color="#2A8C55", width=900, height=10, corner_radius=0)
        # self.intro_frame.pack_propagate(0)
        # self.intro_frame.pack(fill='both', padx=0, pady=(0, 0))
        # CTkLabel(master=self.intro_frame, text="Dashboard", text_color="#fff", font=("Arial Black", 15)).grid(
        #     row = 0,
        #     column = 0,
        #     sticky='w',
        #     padx=(20,0)
        # )
        #

        self.compare_frame = CTkFrame(master=self.main_view, fg_color="#fff", width=1000, height=1000, corner_radius=0)
        self.compare_frame.pack_propagate(0)
        # compare_frame.pack(side="left")

        self.compare_frame.pack(fill='both', padx=0, pady=(30, 0))

        self.textbox1 = CTkTextbox(master=self.compare_frame, fg_color="#f0f0f0", width=457, height=300,
                                   corner_radius=8, font=('Arial', 14))
        self.textbox1.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")

        self.textbox2 = CTkTextbox(master=self.compare_frame, fg_color="#f0f0f0", width=457, height=300,
                                   corner_radius=8, font=('Arial', 14))
        self.textbox2.grid(row=2, column=1, padx=(0, 0), pady=5, sticky="nsew")

        CTkLabel(master=self.compare_frame, text="Reference Text", text_color="#2A8C55", font=("Arial Black", 16)).grid(
            row=1,
            column=0,
            sticky='w',
            padx=(20, 0))
        self.textbox1_charnum = CTkLabel(master=self.compare_frame, text="0/5000", text_color="#2A8C55",
                                         font=("Arial Black", 12))
        self.textbox1_charnum.grid(row=1, column=0, sticky='e', padx=(20, 21))

        CTkLabel(master=self.compare_frame, text="Text for Comparison", text_color="#2A8C55",
                 font=("Arial Black", 16)).grid(row=1,
                                                column=1,
                                                sticky='w')
        self.textbox2_charnum = CTkLabel(master=self.compare_frame, text="0/5000", text_color="#2A8C55",
                                         font=("Arial Black", 12))
        self.textbox2_charnum.grid(row=1, column=1, sticky='e', padx=(20, 1))

        self.label1 = CTkLabel(master=self.compare_frame, text="Enter text to here", fg_color="#f0f0f0",
                               text_color="#3bca7b",
                               font=("Arial Black", 25))
        self.label1.grid(row=2, column=0, sticky='w', padx=(120, 0))
        self.label2 = CTkLabel(master=self.compare_frame, text="Enter text to here", fg_color="#f0f0f0",
                               text_color="#3bca7b",
                               font=("Arial Black", 25))
        self.label2.grid(row=2, column=1, sticky='w', padx=(100, 0))

        self.textbox1.bind("<KeyRelease>",
                           lambda event, lbl=self.label1, txt=self.textbox1: self.update_label(event, lbl, txt,
                                                                                               self.textbox1_charnum))
        self.textbox2.bind("<KeyRelease>",
                           lambda event, lbl=self.label2, txt=self.textbox2: self.update_label(event, lbl, txt,
                                                                                               self.textbox2_charnum))

        self.textbox1.tag_config("highlight", background="#ffff00")
        self.textbox2.tag_config("highlight", background="#ffff00")

        # Add the tag to the first two words
        # textbox1.tag_add("highlight", "1.0", "1.2")
        # textbox2.tag_add("highlight", "1.0", "1.2")

        self.metrics_frame = CTkFrame(master=self.main_view, fg_color="transparent", width=2000, height=1000,
                                      corner_radius=0)
        self.metrics_frame.pack(anchor="n", fill="x", padx=165, pady=(36, 0))
        # compare_frame.pack(side="left")

        self.result_text = CTkLabel(master=self.metrics_frame, text_color="#2A8C55", text="Result",
                                    font=("Arial Black", 18))
        self.result_text.pack(anchor="w")
        self.canvas = tk.Canvas(self.metrics_frame, bg="white", height=10, highlightthickness=0)
        self.canvas.create_line(0, 1, 605, 1, fill="#2A8C55", width=3)  # Adjust the line width and position as needed
        self.canvas.pack(fill="x")
        # sentence_info_frame.pack(fill='both', padx=205, pady=(20, 0))

        self.num_of_sentence_metric = CTkFrame(master=self.metrics_frame, fg_color="transparent", width=170, height=80)
        self.num_of_sentence_metric.grid_propagate(0)
        self.num_of_sentence_metric.pack(side="left")

        self.dup_sentence_metric = CTkFrame(master=self.metrics_frame, fg_color="transparent", width=170, height=80)
        self.dup_sentence_metric.grid_propagate(0)
        self.dup_sentence_metric.pack(side="left", expand=True, anchor="center")
        self.ratio_sentence_metric = CTkFrame(master=self.metrics_frame, fg_color="transparent", width=170, height=80)
        self.ratio_sentence_metric.grid_propagate(0)
        self.ratio_sentence_metric.pack(side="right")
        self.label_numofsentence_01 = CTkLabel(master=self.num_of_sentence_metric, text_color="#2A8C55", text="--",
                                               font=("Arial Black", 30))
        self.label_numofsentence_01.grid(row=0, column=0, padx=(0, 0), pady=(0, 0))
        self.label_numofsentence_02 = CTkLabel(master=self.dup_sentence_metric, text_color="#2A8C55", text="--",
                                               font=("Arial Black", 30))
        self.label_numofsentence_02.grid(row=0, column=0, padx=(0, 0), pady=(0, 0))
        self.label_numofsentence_03 = CTkLabel(master=self.ratio_sentence_metric, text_color="#2A8C55", text="--",
                                               font=("Arial Black", 30))
        self.label_numofsentence_03.grid(row=0, column=0, padx=(0, 0), pady=(0, 0))
        # label_numofsentence_1 = CTkLabel(master=sentence_info_frame, text_color="#9F9F9F", text="%", font=("Arial Black", 15))
        # label_numofsentence_1.grid(row=0, column=1, padx=(75, 0), pady=(0, 0))

        # dup_sentence_metric = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=200, height=60)
        # dup_sentence_metric.grid_propagate(0)
        # dup_sentence_metric.pack(side="left", expand=True, anchor='center')

        self.label_numofsentence_11 = CTkLabel(master=self.num_of_sentence_metric, text_color="#2A8C55",
                                               text="NUMBER OF SENTENCES",
                                               font=("Arial Black", 12))
        self.label_numofsentence_11.grid(row=1, column=0, padx=(0, 0), pady=(0, 0))

        self.label_numofsentence_12 = CTkLabel(master=self.dup_sentence_metric, text_color="#2A8C55",
                                               text="DUPLICATE SENTENCES",
                                               font=("Arial Black", 12))
        self.label_numofsentence_12.grid(row=1, column=0, padx=(0, 0), pady=(0, 0))

        self.label_numofsentence_13 = CTkLabel(master=self.ratio_sentence_metric, text_color="#2A8C55",
                                               text="DUPLICATE RATIO",
                                               font=("Arial Black", 12))
        self.label_numofsentence_13.grid(row=1, column=0, padx=(0, 0), pady=(0, 0))
        # label_numofsentence_percent = CTkLabel(master=main_view, text_color="#9F9F9F", text="0", font=("Arial Black", 50))
        # label_numofsentence_percent.pack(anchor="center", pady=(0,0), ipady = 0)
        # #
        # label_numofsentence_1 = CTkLabel(master=main_view, text_color="#9F9F9F", text="%", font=("Arial Black", 15))
        # label_numofsentence_1.pack(anchor="center", pady=(0,0))
        #
        # label_numofsentence_2 = CTkLabel(master=main_view, text_color="#9F9F9F", text="NUMBER OF SENTENCES", font=("Arial Black", 7))
        # label_numofsentence_2.pack(anchor="center", pady=(0,0))

        self.check_button = CTkButton(master=self.main_view, text="Check Duplicate", font=("Arial Black", 15),
                                      text_color="#fff",
                                      fg_color="#2A8C55", hover_color="#207244", anchor="w")
        self.check_button.pack(anchor="center", ipady=5, pady=(30, 0))

        # table_data = [
        #     ["sentence duplicate in paragraph 1", "sentence duplicate in paragraph 2"],
        #     ["lorem ipsum is simply dummy text of the printing and typesetting industry.", "lorem ipsum is simply dummy text of the printing and typesetting industry."],
        #     ["lorem ipsum is simply dummy text of the printing and typesetting industry.", "lorem ipsum is simply dummy text of the printing and typesetting industry."],
        #     ["lorem ipsum is simply dummy text of the printing and typesetting industry.", "lorem ipsum is simply dummy text of the printing and typesetting industry."],
        #     ["lorem ipsum is simply dummy text of the printing and typesetting industry.", "lorem ipsum is simply dummy text of the printing and typesetting industry."],
        #     ["lorem ipsum is simply dummy text of the printing and typesetting industry.", "lorem ipsum is simply dummy text of the printing and typesetting industry."]
        #     # ["", ""]
        #     # ["order id", "item name", "customer", "address", "status", "quantity"],
        #     # ['3833', 'smartphone', 'alice', '123 main st', 'confirmed', '8'],
        #     # ['6432', 'laptop', 'bob', '456 elm st', 'packing', '5'],
        #     # ['2180', 'tablet', 'crystal', '789 oak st', 'delivered', '1'],
        #     # ['5438', 'headphones', 'john', '101 pine st', 'confirmed', '9'],
        #     # ['9144', 'camera', 'david', '202 cedar st', 'processing', '2'],
        #     # ['7689', 'printer', 'alice', '303 maple st', 'cancelled', '2'],
        #     # ['1323', 'smartwatch', 'crystal', '404 birch st', 'shipping', '6'],
        #     # ['7391', 'keyboard', 'john', '505 redwood st', 'cancelled', '10'],
        #     # ['4915', 'monitor', 'alice', '606 fir st', 'shipping', '6'],
        #     # ['5548', 'external hard drive', 'david', '707 oak st', 'delivered', '10'],
        #     # ['5485', 'table lamp', 'crystal', '808 pine st', 'confirmed', '4'],
        #     # ['7764', 'desk chair', 'bob', '909 cedar st', 'processing', '9'],
        #     # ['8252', 'coffee maker', 'john', '1010 elm st', 'confirmed', '6'],
        #     # ['2377', 'blender', 'david', '1111 redwood st', 'shipping', '2'],
        #     # ['5287', 'toaster', 'alice', '1212 maple st', 'processing', '1'],
        #     # ['7739', 'microwave', 'crystal', '1313 cedar st', 'confirmed', '8'],
        #     # ['3129', 'refrigerator', 'john', '1414 oak st', 'processing', '5'],
        #     # ['4789', 'vacuum cleaner', 'bob', '1515 pine st', 'cancelled', '10']
        # ]

        self.row_nums = None
        self.table_data = [
            ["                        Sentence duplicate in Reference Text                       ",
             "                    Sentence duplicate in Comparision Text                    "],
            [], [], [], [], []
        ]
        self.preds = None

        self.table_frame = CTkScrollableFrame(master=self.main_view, fg_color="transparent")
        self.table_frame.pack(expand=True, fill="both", padx=27, pady=21)
        # table = CTkTable(master=table_frame, values=table_data, colors=["#22252a", "#28282c"],command=show, header_color="#2A8C55", hover_color="#B4B4B4")

        self.table = CTkTable(master=self.table_frame, column=2, values=self.table_data, colors=["#E6E6E6", "#EEEEEE"],
                              command=self.show, header_color="#2A8C55", hover_color="#B4B4B4", font=("Arial", 13))
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        self.table.pack(expand=True)
        self.past_row = 5

        self.check_button.configure(command=self.handle_button_click)
        self.setting_button.configure(command=self.handle_setting_click)
        self.about_button.configure(command=self.handle_about_click)
        self.dashboard_button.configure(command=self.handle_dashboard_click)

        self.current_view = "setting"

        # this for setting view
        self.setting_view = CTkFrame(master=self, fg_color="#ffffff", width=2000, height=1000, corner_radius=0)
        self.setting_view.pack_propagate(0)
        self.setting_intro = CTkLabel(master=self.setting_view, text="Settings", font=("Arial Black", 25),
                                      text_color="#2A8C55")
        self.setting_intro.pack(anchor="nw", pady=(29, 0), padx=27)

        self.setting_grid = CTkFrame(master=self.setting_view, fg_color="transparent")
        self.setting_grid.pack_propagate(0)
        self.setting_grid.pack(fill="both", padx=27, pady=(31, 0))

        self.setting_note = CTkLabel(master=self.setting_grid, text="Note from Authors: This will be completed implement soon.",
                                     font=("Arial", 15), text_color="#000000")
        self.setting_note.pack(anchor="w", pady=(29, 0), padx=270)

        CTkLabel(master=self.setting_grid, text="Model predict:", font=("Arial Bold", 17), text_color="#52A476",
                 justify="left").grid(row=0, column=0, sticky="w", pady=(100, 0))

        self.status_var = tk.IntVar(value=0)

        CTkRadioButton(master=self.setting_grid, variable=self.status_var, value=0, text="model_name",
                       font=("Arial Bold", 14), text_color="#52A476", fg_color="#52A476", border_color="#52A476",
                       hover_color="#207244").grid(row=3, column=0, sticky="w", pady=(16, 0))


        CTkLabel(master=self.setting_grid, text="Font size", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=6, column=0, sticky="w", pady=(42, 0))


        # CTkLabel(master=self.grid, text="Preview", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=6, column=1, sticky="w")
        # CTkEntry(master=self.grid, fg_color="#F0F0F0", border_width=0, width=300).grid(row=6, column=1, ipady=10)

        self.quantity_frame = CTkFrame(master=self.setting_grid, fg_color="transparent")
        self.quantity_frame.grid(row=7, column=0, pady=(21,0), sticky="w")
        CTkButton(master=self.quantity_frame, text="-", width=25, fg_color="#2A8C55", hover_color="#207244", font=("Arial Black", 16)).pack(side="left", anchor="w")
        CTkLabel(master=self.quantity_frame, text="01", text_color="#2A8C55", font=("Arial Black", 16)).pack(side="left", anchor="w", padx=10)
        CTkButton(master=self.quantity_frame, text="+", width=25,  fg_color="#2A8C55",hover_color="#207244", font=("Arial Black", 16)).pack(side="left", anchor="w")


        # this for about view
        self.about_view = CTkFrame(master=self, fg_color="#ffffff", width=2000, height=1000, corner_radius=0)
        self.about_view.pack_propagate(0)
        self.about_intro = CTkLabel(master=self.about_view, text="Abouts", font=("Arial Black", 25),
                                      text_color="#2A8C55")
        self.about_intro.pack(anchor="nw", pady=(29, 0), padx=27)

        self.about_grid = CTkFrame(master=self.about_view, fg_color="transparent")
        self.about_grid.pack(fill="both", padx=27, pady=(31, 0))

        self.logo_hcmus_01_data = Image.open("images/fit-logo-eng--V5.png")
        size = (self.logo_hcmus_01_data.size[0]/1.25, self.logo_hcmus_01_data.size[1]/1.25)
        self.logo_hcmus_01 = CTkImage(dark_image=self.logo_hcmus_01_data, light_image=self.logo_hcmus_01_data, size=size)

        self.logo_hcmus_02_data = Image.open("images/clc_hcmus.png")
        size = (self.logo_hcmus_02_data.size[0]/8, self.logo_hcmus_02_data.size[1]/8)
        self.logo_hcmus_02 = CTkImage(dark_image=self.logo_hcmus_02_data, light_image=self.logo_hcmus_02_data, size=size)

        CTkLabel(master=self.about_grid, text="", image=self.logo_hcmus_01).grid(row=2, column=0, padx=(200, 0), pady=0, sticky="w")
        CTkLabel(master=self.about_grid, text="", image=self.logo_hcmus_02).grid(row=2, column=1, padx=20, pady=0, sticky="w")



        self.project_info = (
            "This project is part of the Course Introduction to Natural Language Processing (CSC15006) -\n University of Science, VNU-HCM\n\n"
            "The team members collaborating on this project include:\n"
            "Lê Phạm Hoàng Trung\n"
            "Trần Ngọc Bảo\n"
            "Lê Văn Tấn\n"
            "Nguyễn Thế Phong\n\n"
            "For further information, please feel free to contact us via email\n at nguyenthephong508@gmail.com.\n\n"
            "This project repository link: https://github.com/phong-nt-990/Project10.NLP"
        )

        self.about_grid_2 = CTkFrame(master=self.about_view, fg_color="transparent")
        self.about_grid_2.pack(fill="both", padx=27, pady=(25, 0))

        self.about_intro = CTkLabel(master=self.about_grid_2, text="Identifying Text Similarity Tools in Internal Data Repository", font=("Arial Black", 25),
                                    text_color="#2A8C55")
        self.about_intro.pack(anchor="nw", pady=(15, 35), padx=27)

        self.text_box = tk.Text(self.about_grid_2, height=30, width=75, font=('Roboto', 12),borderwidth=0, highlightthickness=0)
        self.text_box.insert(tk.END, self.project_info)
        self.text_box.tag_configure("center", justify='center')  # Creating a tag to center the text
        self.text_box.tag_add("center", "1.0", "end")  # Applying the 'center' tag to the entire text
        self.text_box.tag_add("link", "13.30", END)
        self.text_box.tag_configure("link", foreground="blue", underline=True)
        self.text_box.tag_bind("link", "<Button-1>", self.open_link)
        self.text_box.tag_bind("link", "<Enter>", lambda event: self.text_box.config(cursor="hand2"))
        self.text_box.tag_bind("link", "<Leave>", lambda event: self.text_box.config(cursor=""))
        self.text_box.config(state='disabled')
        self.text_box.pack(anchor="center")

        self.select_frame_by_name("main")

    def open_link(sekf, event):
    # Code to open the link goes here
    # For example:
        link = "https://github.com/phong-nt-990/Project10.NLP"
        os.system("start " + link)
    def processing_text(self, input: str):
        threshold = 50
        tmp = input.split()
        count = 0
        res = ""
        for i in tmp:
            count += len(i)
            if count >= threshold:
                res = res + i + "\n"
                count = 0
            else:
                res = res + i + " "
        return res

    def add_transparent_padding_left(self, image, padding_width):
        # Open the image using Pillow
        img = image.copy()

        # Determine new dimensions with added padding
        new_width = img.width + padding_width
        new_height = img.height

        # Create a new transparent image with the increased width
        new_img = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))

        # Paste the original image onto the new image with padding
        new_img.paste(img, (padding_width, 0))

        # Save the modified image
        return new_img

    def update_label(self, event, label, textbox, charnum):
        # Check if the textbox has content
        content = textbox.get("1.0", END)
        if len(content) > 1:
            label.configure(text="")
            print(len(content))
            # label.config(text="")
            # print(content)
        else:
            # label.config(text="Enter text here")
            label.configure(text="Enter text to here")
        charnum.configure(text=str(len(content) - 1) + "/5000")

    def get_sentence_indices(self, paragraph):
        sentences = split('(?<=[.!?]) +', paragraph)
        # print(len(paragraph))
        sentence_indices = {}
        current_index = 0
        for i, sentence in enumerate(sentences):
            start_index = current_index
            end_index = start_index + len(sentence) - 1
            # print(paragraph[end_index + 1])
            # print(end_index)
            if end_index + 1 < len(paragraph) and paragraph[end_index + 1] == '.':
                print(paragraph[end_index + 1])
                sentence_indices[i] = [start_index, end_index + 1]
            else:
                sentence_indices[i] = [start_index, end_index]
            current_index = end_index + 2
        return sentence_indices

    def textbox_highlight(self, row_index: int):
        paragraph_1 = self.textbox1.get("1.0", END)
        paragraph_2 = self.textbox2.get("1.0", END)
        p1 = self.get_sentence_indices(paragraph_1)
        p2 = self.get_sentence_indices(paragraph_2)
        start_1, end_1 = p1[self.preds[row_index - 1][0]][0], p1[self.preds[row_index - 1][0]][1]
        start_2, end_2 = p2[self.preds[row_index - 1][1]][0], p2[self.preds[row_index - 1][1]][1]
        self.textbox1.tag_add("highlight", "1." + str(start_1), "1." + str(end_1 + 1))
        self.textbox2.tag_add("highlight", "1." + str(start_2), "1." + str(end_2 + 1))

    def show(self, cell):
        # global row_nums
        # print(cell["row"])
        if cell["row"] == 0: return
        if cell["row"] != self.row_nums:
            if self.row_nums is None:
                self.table.select_row(cell["row"])
                self.row_nums = cell["row"]
                if self.table.get_row(self.row_nums)[0] != ' ':
                    self.textbox_highlight(self.row_nums)
            else:
                self.table.deselect_row(self.row_nums)
                self.table.select_row(cell["row"])
                self.row_nums = cell["row"]
                if self.table.get_row(self.row_nums)[0] != ' ':
                    # dehighlight
                    self.textbox1.tag_remove("highlight", "1.0", END)
                    self.textbox2.tag_remove("highlight", "1.0", END)
                    self.textbox_highlight(self.row_nums)

        else:
            self.table.deselect_row(cell["row"])
            self.row_nums = None
            self.textbox1.tag_remove("highlight", "1.0", END)
            self.textbox2.tag_remove("highlight", "1.0", END)

    # print("==debug===")
    # print(table.get_row(row_nums))
    # row_nums.remove(cell["row"])

    def preds_processing(self, num_sentence: int):
        get_2sentence_from_index = {}
        p = array(self.preds, dtype=uint8)
        p = p.reshape((num_sentence, -1))
        print(p)
        count = 0
        for index, value in enumerate(p):
            if any(value == 1):
                tmp = []
                tmp.append(index)
                tmp.append(where(value == 1)[0][0])
                get_2sentence_from_index[count] = tmp
                count += 1
        return get_2sentence_from_index

    def handle_button_click(self):
        if self.row_nums is not None:
            self.table.deselect_row(self.row_nums)
            self.row_nums = None
            self.textbox1.tag_remove("highlight", "1.0", END)
            self.textbox2.tag_remove("highlight", "1.0", END)
        self.check_button.configure(text="   Processing  ")
        self.check_button.update()

        # time.sleep(0.5)

        # print("Button clicked")
        # global past_row
        # global preds

        paragraph1 = self.textbox1.get("1.0", END)
        paragraph2 = self.textbox2.get("1.0", END)
        number_of_sentences2, number_of_sentences1, result, self.preds = self.model.predict(paragraph1, paragraph2)
        self.preds = self.preds_processing(number_of_sentences1)
        # print(self.preds)
        # print("==== debug ====")
        # print(preds)
        duplicate_ratio = round(len(result) / number_of_sentences2 * 100, 1)
        if round(duplicate_ratio, 0) == int(duplicate_ratio):
            duplicate_ratio = int(duplicate_ratio)

        self.label_numofsentence_01.configure(text=str(number_of_sentences2))
        self.label_numofsentence_02.configure(text=str(len(result)))
        self.label_numofsentence_03.configure(text=str(duplicate_ratio) + "%")

        # Processing text
        for i in range(len(result)):
            for j in range(len(result[i])):
                result[i][j] = self.processing_text(result[i][j])

        self.table.configure(values=self.table_data)
        for i in range(self.past_row):
            self.table.delete_row(1)
        self.past_row = 0
        # table.update_values(result)
        # table.add_row(["1","2"])
        for i in result:
            self.table.add_row(i)
            self.past_row += 1

        # textbox1.tag_add("start", "1.1", "2.4")
        # textbox1.tag_config("here", background="yellow", foreground="blue")
        self.check_button.configure(text="Check Duplicate")

        # textbox1.tag_add("highlight", "1.0", "1.2")
        # textbox2.tag_add("highlight", "1.0", "1.2")
        # table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        # table.pack(expand=True)

    # setting_button.configure(command=handle_setting_click)

    def select_frame_by_name(self, name):
        # set button color for selected button

        # self.dashboard_button = CTkButton(master=self.sidebar_frame, image=self.analytics_img, text="Dashboard",
        #                                   fg_color="#fff", text_color="#2A8C55",
        #                                   font=("Arial Bold", 14), hover_color="#eee", anchor="w")

        # self.setting_button = CTkButton(master=self.sidebar_frame, image=self.settings_img, text="Settings",
        #                                 fg_color="transparent",
        #                                 font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        if name == "main":
            self.dashboard_button.configure(fg_color="#fff", image=self.analytics_checked_img, text_color="#2A8C55",
                                            hover_color="#eee")
        else:
            self.dashboard_button.configure(fg_color="transparent", image=self.analytics_img, text_color="#fff",
                                            hover_color="#207244")
        if name == "setting":
            self.setting_button.configure(fg_color="#fff", image=self.settings_checked_img, text_color="#2A8C55",
                                          hover_color="#eee")
        else:
            self.setting_button.configure(fg_color="transparent", image=self.settings_img, text_color="#fff",
                                          hover_color="#207244")
        if name == "about":
            self.about_button.configure(fg_color="#fff", image=self.about_checked_img, text_color="#2A8C55",
                                        hover_color="#eee")
        else:
            self.about_button.configure(fg_color="transparent", image=self.about_img, text_color="#fff",
                                        hover_color="#207244")
        # self.setting_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        # self.about_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "main":
            # self.main_view.pack_propagate(0)
            self.main_view.pack(side="left")
        else:
            self.main_view.pack_forget()
        if name == "setting":
            self.setting_view.pack(side="left")
        else:
            self.setting_view.pack_forget()
        if name == "about":
            self.about_view.pack(side="left")
        else:
            self.about_view.pack_forget()

        self.current_view = name

    def handle_dashboard_click(self):
        if self.current_view != "main":
            self.select_frame_by_name("main")

    def handle_setting_click(self):
        if self.current_view != "setting":
            self.select_frame_by_name("setting")

    def handle_about_click(self):
        if self.current_view != "about":
            self.select_frame_by_name("about")

def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
