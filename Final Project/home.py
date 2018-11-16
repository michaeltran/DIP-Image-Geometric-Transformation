from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from Tranformations import Transformations
from Affine import Affine
import threading
import cv2
import numpy as np

DEFAULT_WIDTH = 300
DEFAULT_HEIGHT = 300

normal_text = ('helvetica', 9)
bold_text = ('helvetica', 9, 'bold')

# open browser
def open_explorer():
    global input_selected_file
    global selected_photo

    open_explorer.selected_file = filedialog.askopenfilename(initialdir="./")
    input_selected_file = open_explorer.selected_file

    # handling cancel operation
    if not input_selected_file:
        return

    #print("selected file is : ",  open_explorer.selected_file)
    path = "Inputs/current_input.png"
    input_ref_img = cv2.imread(input_selected_file)
    cv2.imwrite(path,input_ref_img)
    selected_image = Image.open(path)
    selected_image = selected_image.resize((DEFAULT_WIDTH,DEFAULT_HEIGHT))
    selected_photo = ImageTk.PhotoImage(selected_image)

    place_image_details(open_explorer.selected_file,input_ref_img.shape)

    CreatePhotoCanvas()

    #input_photo_panel = Label(window, image=selected_photo, bg="white", relief="groove")
    #input_photo_panel.image = selected_photo
    #input_photo_panel.place(x=400+offset_param, y=50)
    #place_image_details(open_explorer.selected_file,input_ref_img.shape)


def CreatePointOnCanvas(canvas, x, y, color, label):
    x1, y1 = (x - 10), (y - 10)
    x2, y2 = (x + 10), (y + 10)
    canvas.create_oval(x1, y1, x2, y2, fill=color)
    canvas.create_text(x, y, text=label)

def CreateMainPointOnCanvas(canvas, x, y, color, label):
    x1, y1 = (x - 10), (y - 10)
    x2, y2 = (x + 10), (y + 10)
    canvas.create_oval(x1, y1, x2, y2, fill=color)
    canvas.create_text(x, y, text=label, font=('helvetica', 12, 'bold'))


def click_coords(event):
    if int(radiobtn_operation_var.get()) == 4:
        global current_bolded_pt

        if (current_bolded_pt == affine_pt1):
            affine_pt1_x_entry.delete(0, END)
            affine_pt1_x_entry.insert(0, event.x)
            affine_pt1_y_entry.delete(0, END)
            affine_pt1_y_entry.insert(0, event.y)
            affine_pt1.config(font=normal_text)
            affine_pt2.config(font=bold_text)
            current_bolded_pt = affine_pt2
        elif (current_bolded_pt == affine_pt2):
            affine_pt2_x_entry.delete(0, END)
            affine_pt2_x_entry.insert(0, event.x)
            affine_pt2_y_entry.delete(0, END)
            affine_pt2_y_entry.insert(0, event.y)
            affine_pt2.config(font=normal_text)
            affine_pt3.config(font=bold_text)
            current_bolded_pt = affine_pt3
        elif (current_bolded_pt == affine_pt3):
            affine_pt3_x_entry.delete(0, END)
            affine_pt3_x_entry.insert(0, event.x)
            affine_pt3_y_entry.delete(0, END)
            affine_pt3_y_entry.insert(0, event.y)
            affine_pt3.config(font=normal_text)
            affine_pt4.config(font=bold_text)
            current_bolded_pt = affine_pt4
        elif (current_bolded_pt == affine_pt4):
            affine_pt4_x_entry.delete(0, END)
            affine_pt4_x_entry.insert(0, event.x)
            affine_pt4_y_entry.delete(0, END)
            affine_pt4_y_entry.insert(0, event.y)
            affine_pt4.config(font=normal_text)
            affine_pt5.config(font=bold_text)
            current_bolded_pt = affine_pt5
        elif (current_bolded_pt == affine_pt5):
            affine_pt5_x_entry.delete(0, END)
            affine_pt5_x_entry.insert(0, event.x)
            affine_pt5_y_entry.delete(0, END)
            affine_pt5_y_entry.insert(0, event.y)
            affine_pt5.config(font=normal_text)
            affine_pt6.config(font=bold_text)
            current_bolded_pt = affine_pt6
        elif (current_bolded_pt == affine_pt6):
            affine_pt6_x_entry.delete(0, END)
            affine_pt6_x_entry.insert(0, event.x)
            affine_pt6_y_entry.delete(0, END)
            affine_pt6_y_entry.insert(0, event.y)

        CreatePhotoCanvas()


def CreatePhotoCanvas():
    global selected_photo

    try:
        selected_photo # does selected_photo exist in the current namespace
    except NameError:
        return

    try:
        input_photo_panel.delete("all")
    except NameError:
        temp = 1

    input_photo_panel = Canvas(window, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
    input_photo_panel.pack(expand=YES, fill=BOTH)
    input_photo_panel.create_image(2, 2, image=selected_photo, anchor=NW)
    input_photo_panel.img = selected_photo
    input_photo_panel.place(x=400+offset_param, y=50)

    if affine_pt1_x_entry.get().isdigit() and affine_pt1_y_entry.get().isdigit():
        if current_bolded_pt == affine_pt1:
            CreateMainPointOnCanvas(input_photo_panel, float(affine_pt1_x_entry.get()), float(affine_pt1_y_entry.get()), "#476042", '1')
        else:
            CreatePointOnCanvas(input_photo_panel, float(affine_pt1_x_entry.get()), float(affine_pt1_y_entry.get()), "#476042", '1')
    if affine_pt2_x_entry.get().isdigit() and affine_pt2_y_entry.get().isdigit():
        if current_bolded_pt == affine_pt2:
            CreateMainPointOnCanvas(input_photo_panel, float(affine_pt2_x_entry.get()), float(affine_pt2_y_entry.get()), "#476042", '2')
        else:
            CreatePointOnCanvas(input_photo_panel, float(affine_pt2_x_entry.get()), float(affine_pt2_y_entry.get()), "#476042", '2')
    if affine_pt3_x_entry.get().isdigit() and affine_pt3_y_entry.get().isdigit():
        if current_bolded_pt == affine_pt3:
            CreateMainPointOnCanvas(input_photo_panel, float(affine_pt3_x_entry.get()), float(affine_pt3_y_entry.get()), "#476042", '3')
        else:
            CreatePointOnCanvas(input_photo_panel, float(affine_pt3_x_entry.get()), float(affine_pt3_y_entry.get()), "#476042", '3')
    if affine_pt4_x_entry.get().isdigit() and affine_pt4_y_entry.get().isdigit():
        if current_bolded_pt == affine_pt4:
            CreateMainPointOnCanvas(input_photo_panel, float(affine_pt4_x_entry.get()), float(affine_pt4_y_entry.get()), "#FF0000", '1')
        else:
            CreatePointOnCanvas(input_photo_panel, float(affine_pt4_x_entry.get()), float(affine_pt4_y_entry.get()), "#FF0000", '1')
    if affine_pt5_x_entry.get().isdigit() and affine_pt5_y_entry.get().isdigit():
        if current_bolded_pt == affine_pt5:
            CreateMainPointOnCanvas(input_photo_panel, float(affine_pt5_x_entry.get()), float(affine_pt5_y_entry.get()), "#FF0000", '2')
        else:
            CreatePointOnCanvas(input_photo_panel, float(affine_pt5_x_entry.get()), float(affine_pt5_y_entry.get()), "#FF0000", '2')
    if affine_pt6_x_entry.get().isdigit() and affine_pt6_y_entry.get().isdigit():
        if current_bolded_pt == affine_pt6:
            CreateMainPointOnCanvas(input_photo_panel, float(affine_pt6_x_entry.get()), float(affine_pt6_y_entry.get()), "#FF0000", '3')
        else:
            CreatePointOnCanvas(input_photo_panel, float(affine_pt6_x_entry.get()), float(affine_pt6_y_entry.get()), "#FF0000", '3')

    input_photo_panel.bind("<Button 1>", click_coords)


def place_image_details(file_path,size):
    global properties_label, img_name, img_name_val, img_ht, img_ht_val, img_wd, img_wd_val

    file_path = str(file_path)
    file_path = file_path[::-1]
    name = file_path[:file_path.index('/')]
    name = name[::-1]
    print(name)
    height = size[0]
    width = size[1]

    properties_label = Label(window, text="Image Details", bg="white", fg="#337ab7", font=("Helvetica", 14))
    properties_label.place(x=820 + offset_param, y=50)
    img_name = Label(window, text="Name", bg="white", fg="#337ab7", font=("Helvetica", 10, "bold"))
    img_name.place(x=820 + offset_param, y=90)
    img_name_val = Label(window, text=name, bg="white", fg="#337ab7", font=("Helvetica", 10))
    img_name_val.place(x=910 + offset_param, y=90)
    img_ht = Label(window, text="Height", bg="white", fg="#337ab7", font=("Helvetica", 10, "bold"))
    img_ht.place(x=820 + offset_param, y=120)
    img_ht_val = Label(window, text = str(height) + " px", bg="white", fg="#337ab7", font=("Helvetica", 10))
    img_ht_val.place(x=910 + offset_param, y=120)
    img_wd = Label(window, text="Width", bg="white", fg="#337ab7", font=("Helvetica", 10, "bold"))
    img_wd.place(x=820 + offset_param, y=150)
    img_wd_val = Label(window, text = str(width) +" px", bg="white", fg="#337ab7", font=("Helvetica", 10))
    img_wd_val.place(x=910 + offset_param, y=150)


def init_operations():
    opertions_dict[1] = "Scaling"
    opertions_dict[2] = "Rotation"
    opertions_dict[3] = "Translation"
    opertions_dict[4] = "Affine Tranformation"
    opertions_dict[5] = "Polar Tranformation"
    opertions_dict[6] = "Log Polar Tranformation"

"""
def init_interpolations():
    interpolation_dict[100] = "Nearest Neigbhor"
    interpolation_dict[200] = "Bilinear"
    interpolation_dict[300] = "Cubic"
    interpolation_dict[400] = "Lanczos4"
"""

def init_output_types():
    output_type_dict[1000] = "Cropped Image"
    output_type_dict[2000] = "Full Image"


def create_widgets(operation_val):
    if operation_val == 1:
        scale_x.place(x=800+offset_param, y=427)
        scale_x_entry.place(x=900+offset_param,y=430)
        scale_x_entry.insert(0,"1")
        scale_y.place(x=800+offset_param, y=457)
        scale_y_entry.place(x=900+offset_param, y=460)
        scale_y_entry.insert(0, "1")
        interpolation_label.place(x=800+offset_param,y= 493)
        interpolations_popup.place(x=900 + offset_param, y=490)

    elif operation_val == 2:
        degrees.place(x=800+offset_param, y=427)
        degrees_entry.place(x=900+offset_param,y=430)
        degrees_entry.insert(0, "0")
        direction_label.place(x=800+offset_param, y=463)
        popupMenu.place(x=900+offset_param, y=460)

    elif operation_val == 3:
        translate_x.place(x=800+offset_param, y=427)
        translate_x_entry.place(x=900+offset_param,y=430)
        translate_x_entry.insert(0,"0")
        translate_y.place(x=800+offset_param, y=457)
        translate_y_entry.place(x=900+offset_param, y=460)
        translate_y_entry.insert(0, "0")

    elif operation_val == 4:
        affine_pt1.place(x=800+offset_param, y=427)
        affine_pt1_x_entry.place(x=950+offset_param, y=430)
        affine_pt1_y_entry.place(x=950+offset_param + 75, y=430)

        affine_pt2.place(x=800+offset_param, y=457)
        affine_pt2_x_entry.place(x=950+offset_param, y=460)
        affine_pt2_y_entry.place(x=950+offset_param + 75, y=460)

        affine_pt3.place(x=800+offset_param, y=487)
        affine_pt3_x_entry.place(x=950+offset_param, y=490)
        affine_pt3_y_entry.place(x=950+offset_param + 75, y=490)

        affine_pt4.place(x=800+offset_param, y=517)
        affine_pt4_x_entry.place(x=950+offset_param, y=520)
        affine_pt4_y_entry.place(x=950+offset_param + 75, y=520)

        affine_pt5.place(x=800+offset_param, y=547)
        affine_pt5_x_entry.place(x=950+offset_param, y=550)
        affine_pt5_y_entry.place(x=950+offset_param + 75, y=550)

        affine_pt6.place(x=800+offset_param, y=577)
        affine_pt6_x_entry.place(x=950+offset_param, y=580)
        affine_pt6_y_entry.place(x=950+offset_param + 75, y=580)

        global current_bolded_pt
        affine_pt1.config(font=bold_text)
        affine_pt2.config(font=normal_text)
        affine_pt3.config(font=normal_text)
        affine_pt4.config(font=normal_text)
        affine_pt5.config(font=normal_text)
        affine_pt6.config(font=normal_text)
        current_bolded_pt = affine_pt1


def operation_changed():
    print("Operation changed")
    value = int(radiobtn_operation_var.get())
    #print(direction.get())
    remove_all_widgets()
    create_widgets(value)
    CreatePhotoCanvas()


def init_widgets():
    global scale_x, scale_x_entry, scale_y, scale_y_entry,interpolation_label,interpolations_popup
    global degrees, degrees_entry, direction_label,popupMenu
    global translate_x, translate_x_entry, translate_y, translate_y_entry
    global affine_pt1, affine_pt1_x_entry, affine_pt1_y_entry
    global affine_pt2, affine_pt2_x_entry, affine_pt2_y_entry
    global affine_pt3, affine_pt3_x_entry, affine_pt3_y_entry
    global affine_pt4, affine_pt4_x_entry, affine_pt4_y_entry
    global affine_pt5, affine_pt5_x_entry, affine_pt5_y_entry
    global affine_pt6, affine_pt6_x_entry, affine_pt6_y_entry

    scale_x = Label(window, text="Scale X Factor", bg="white")
    scale_x_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5")
    scale_y = Label(window, text="Scale Y Factor", bg="white")
    scale_y_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5")
    interpolation_label = Label(window, text="Interpolation", bg="white")
    interpolations_popup = OptionMenu(window, interpolation_choice, *interpolation_techniques)

    degrees = Label(window, text="Rotation Angle", bg="white")
    degrees_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5")
    direction_label = Label(window, text="Direction", bg="white")
    popupMenu = OptionMenu(window, direction, *choices)

    translate_x = Label(window, text="Translate X", bg="white")
    translate_x_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5")
    translate_y = Label(window, text="Translate Y", bg="white")
    translate_y_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5")

    def callback(sv):
        CreatePhotoCanvas()

    sv1 = StringVar()
    sv2 = StringVar()
    sv3 = StringVar()
    sv4 = StringVar()
    sv5 = StringVar()
    sv6 = StringVar()
    sv7 = StringVar()
    sv8 = StringVar()
    sv9 = StringVar()
    sv10 = StringVar()
    sv11 = StringVar()
    sv12 = StringVar()
    sv1.trace("w", lambda name, index, mode, sv=sv1: callback(sv1))
    sv2.trace("w", lambda name, index, mode, sv=sv2: callback(sv2))
    sv3.trace("w", lambda name, index, mode, sv=sv3: callback(sv3))
    sv4.trace("w", lambda name, index, mode, sv=sv4: callback(sv4))
    sv5.trace("w", lambda name, index, mode, sv=sv5: callback(sv5))
    sv6.trace("w", lambda name, index, mode, sv=sv6: callback(sv6))
    sv7.trace("w", lambda name, index, mode, sv=sv7: callback(sv7))
    sv8.trace("w", lambda name, index, mode, sv=sv8: callback(sv8))
    sv9.trace("w", lambda name, index, mode, sv=sv9: callback(sv9))
    sv10.trace("w", lambda name, index, mode, sv=sv10: callback(sv10))
    sv11.trace("w", lambda name, index, mode, sv=sv11: callback(sv11))
    sv12.trace("w", lambda name, index, mode, sv=sv12: callback(sv12))

    affine_pt1 = Label(window, text="Original Point 1 (x, y)", bg="white", font=('helvetica', 9))
    affine_pt1_x_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5", textvariable=sv1)
    affine_pt1_y_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5", textvariable=sv2)
    affine_pt2 = Label(window, text="Original Point 2 (x, y)", bg="white", font=('helvetica', 9))
    affine_pt2_x_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5", textvariable=sv3)
    affine_pt2_y_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5", textvariable=sv4)
    affine_pt3 = Label(window, text="Original Point 3 (x, y)", bg="white", font=('helvetica', 9))
    affine_pt3_x_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5", textvariable=sv5)
    affine_pt3_y_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5", textvariable=sv6)
    affine_pt4 = Label(window, text="Target Point 1 (x, y)", bg="white", font=('helvetica', 9))
    affine_pt4_x_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5", textvariable=sv7)
    affine_pt4_y_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5", textvariable=sv8)
    affine_pt5 = Label(window, text="Target Point 2 (x, y)", bg="white", font=('helvetica', 9))
    affine_pt5_x_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5", textvariable=sv9)
    affine_pt5_y_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5", textvariable=sv10)
    affine_pt6 = Label(window, text="Target Point 3 (x, y)", bg="white", font=('helvetica', 9))
    affine_pt6_x_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5", textvariable=sv11)
    affine_pt6_y_entry = Entry(window, width=10, relief="ridge", bg="#F5F5F5", textvariable=sv12)

    global current_bolded_pt
    affine_pt1.config(font=bold_text)
    current_bolded_pt = affine_pt1

    affine_pt1.bind("<Button-1>", lambda event : SelectAffineLabel(event, affine_pt1))
    affine_pt2.bind("<Button-1>", lambda event : SelectAffineLabel(event, affine_pt2))
    affine_pt3.bind("<Button-1>", lambda event : SelectAffineLabel(event, affine_pt3))
    affine_pt4.bind("<Button-1>", lambda event : SelectAffineLabel(event, affine_pt4))
    affine_pt5.bind("<Button-1>", lambda event : SelectAffineLabel(event, affine_pt5))
    affine_pt6.bind("<Button-1>", lambda event : SelectAffineLabel(event, affine_pt6))


def SelectAffineLabel(event, pt):
    global current_bolded_pt
    if current_bolded_pt == pt:
        pass
    else:
        current_bolded_pt.config(font=normal_text)
        pt.config(font=bold_text)
        current_bolded_pt = pt

    CreatePhotoCanvas()

def remove_all_widgets():
    scale_x.place_forget()
    scale_x_entry.delete(0, 'end')
    scale_x_entry.place_forget()
    scale_y.place_forget()
    scale_y_entry.delete(0, 'end')
    scale_y_entry.place_forget()
    interpolation_label.place_forget()
    interpolations_popup.place_forget()

    degrees.place_forget()
    degrees_entry.delete(0, 'end')
    degrees_entry.place_forget()
    direction_label.place_forget()
    popupMenu.place_forget()

    translate_x.place_forget()
    translate_x_entry.delete(0, 'end')
    translate_x_entry.place_forget()
    translate_y.place_forget()
    translate_y_entry.delete(0, 'end')
    translate_y_entry.place_forget()

    affine_pt1.place_forget()
    affine_pt1_x_entry.delete(0, 'end')
    affine_pt1_x_entry.place_forget()
    affine_pt1_y_entry.delete(0, 'end')
    affine_pt1_y_entry.place_forget()
    affine_pt2.place_forget()
    affine_pt2_x_entry.delete(0, 'end')
    affine_pt2_x_entry.place_forget()
    affine_pt2_y_entry.delete(0, 'end')
    affine_pt2_y_entry.place_forget()
    affine_pt3.place_forget()
    affine_pt3_x_entry.delete(0, 'end')
    affine_pt3_x_entry.place_forget()
    affine_pt3_y_entry.delete(0, 'end')
    affine_pt3_y_entry.place_forget()
    affine_pt4.place_forget()
    affine_pt4_x_entry.delete(0, 'end')
    affine_pt4_x_entry.place_forget()
    affine_pt4_y_entry.delete(0, 'end')
    affine_pt4_y_entry.place_forget()
    affine_pt5.place_forget()
    affine_pt5_x_entry.delete(0, 'end')
    affine_pt5_x_entry.place_forget()
    affine_pt5_y_entry.delete(0, 'end')
    affine_pt5_y_entry.place_forget()
    affine_pt6.place_forget()
    affine_pt6_x_entry.delete(0, 'end')
    affine_pt6_x_entry.place_forget()
    affine_pt6_y_entry.delete(0, 'end')
    affine_pt6_y_entry.place_forget()


def show_result():
    thread_1 = threading.Thread(target=transform_image)
    show_progressbar()
    thread_1.start()


def show_progressbar():

    global progress_canvas

    progress_canvas = Toplevel()
    p_canvas = Canvas(progress_canvas, width=500, height=200,bg="white")
    p_canvas.pack(expand=YES, fill=BOTH)
    display = Label(p_canvas, text="Processing...", bg="white", fg="black", font=("Helvetica", 12))
    display.place(x=215,y=70)
    progress_bar = ttk.Progressbar(p_canvas, orient="horizontal", length=300, mode="indeterminate")
    progress_bar.place(x=100, y=100)
    progress_bar.start(50)


def close_progressbar():
    print("progress bar close function")
    progress_canvas.destroy()


def transform_image():
    #print("thread 2")
    operation_var = int(radiobtn_operation_var.get())
    operation = opertions_dict[operation_var]
    image_display_var = int(output_type_var.get())
    show_full_image = False
    if image_display_var == 2000:
        show_full_image = True

    transformation_ref = Transformations()
    affine_ref = Affine()

    if not input_selected_file:
        messagebox.showerror("Error", "Please select the input file")
        return

    if operation == 'Scaling':
        x_factor = float(scale_x_entry.get())
        y_factor = float(scale_y_entry.get())
        selected_interpolation = interpolation_choice.get()

        output_img_name, height, width= transformation_ref.scale_image(input_selected_file, x_factor, y_factor,selected_interpolation)


    elif operation == "Translation":
        x_units = int(float(translate_x_entry.get()))
        y_units = int(float(translate_y_entry.get()))

        output_img_name, height, width= transformation_ref.translate_image(input_selected_file, x_units ,y_units)

    elif operation == "Rotation":
        angle = float(degrees_entry.get())
        direction_value = direction.get()
        #print("angle :", angle,direction_value)
        output_img_name, height, width = transformation_ref.rotate_image(input_selected_file, angle, direction_value)

    elif operation == "Affine Tranformation":
        pts1 = np.float32([[float(affine_pt1_x_entry.get()), float(affine_pt1_y_entry.get())], 
                           [float(affine_pt2_x_entry.get()), float(affine_pt2_y_entry.get())],
                           [float(affine_pt3_x_entry.get()), float(affine_pt3_y_entry.get())]])
        pts2 = np.float32([[float(affine_pt4_x_entry.get()), float(affine_pt4_y_entry.get())],
                           [float(affine_pt5_x_entry.get()), float(affine_pt5_y_entry.get())],
                           [float(affine_pt6_x_entry.get()), float(affine_pt6_y_entry.get())]])

        output_img_name, height, width = affine_ref.affine_transform(input_selected_file, pts1, pts2)

    place_output_image(output_img_name, height, width)


def place_output_image(output_img_name, height, width):
    global save_img_name_ref

    close_progressbar()
    #progress_canvas.destroy()

    output_image = Image.open(output_img_name)
    output_image = output_image.resize((width, height), Image.ANTIALIAS)
    output_photo = ImageTk.PhotoImage(output_image)

    save_img_name_ref = output_img_name

    """
    output_photo_panel = Label(window, image=output_photo, bg="white", relief="groove")
    output_photo_panel.image = output_photo
    output_photo_panel.place(x=800 + offset_param, y=50)
    """

    output_canvas = Toplevel()
    canvas = Canvas(output_canvas, width=width+100, height=height+100,bg="white")
    canvas.pack(expand=YES, fill=BOTH)

    save_btn = Button(canvas, text="Save",width=7, bg="#5cb85c",fg="white",command=save_img)


    # image not visual
    canvas.create_image(50, 50, image=output_photo, anchor=NW)
    save_btn.place(x=width/2+20,y=20)
    # assigned the gif1 to the canvas object
    canvas.img = output_photo


def save_img():
    filename = filedialog.asksaveasfilename()
    if not filename:
        return
    try :
        cv2.imwrite(filename,cv2.imread(save_img_name_ref,1))
        messagebox.showinfo('Success', 'Image has been saved')
    except Exception as Exp:
        messagebox.showerror("Sorry","Some error has occurred while saving")

def reset():
    global properties_label, img_name, img_name_val, img_ht, img_ht_val, img_wd, img_wd_val
    global input_selected_file

    init_default_input()
    properties_label.place_forget()
    img_name.place_forget()
    img_name_val.place_forget()
    img_ht.place_forget()
    img_ht_val.place_forget()
    img_wd.place_forget()
    img_wd_val.place_forget()

    input_selected_file = None


def init_default_input():
    global offset_param, default_input_file_path, input_image, input_photo, input_photo_panel

    default_input_file_path = "default_input_image.png"

    input_image = Image.open(default_input_file_path)
    input_image = input_image.resize((DEFAULT_WIDTH, DEFAULT_HEIGHT), Image.ANTIALIAS)
    input_photo = ImageTk.PhotoImage(input_image)

    input_photo_panel = Canvas(window, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT,bg="white")
    input_photo_panel.pack(expand=YES, fill=BOTH)
    input_photo_panel.create_image(2, 2, image=input_photo, anchor=NW)
    input_photo_panel.img = input_photo

    #input_photo_panel = Label(window, image=input_photo, bg="white", relief="groove")
    #input_photo_panel.image = input_photo
    #input_photo_panel.place(x=400 + offset_param, y=50)
    input_photo_panel.place(x=400 + offset_param, y=50)

window = Tk()

#size of the window
window.geometry("1200x700")
window.title("Image Geometric Transformations")
window.configure(background="white")
offset_param = 0
input_selected_file = None
save_img_name_ref = None

# placing input image
input_title = Label(window,text="Image Preview",bg="white",fg="Tomato",font=("Helvetica", 16))
input_title.place(x=490+offset_param, y=15)
default_input_file_path = None
input_image = None
input_photo = None
input_photo_panel = None
init_default_input()


#image details
properties_label = None
img_name = None
img_name_val = None
img_ht = None
img_ht_val = None
img_wd = None
img_wd_val = None

"""
# placing output image
output_title = Label(window,text="OUTPUT",bg="white",fg="Tomato",font=("Helvetica", 16))
output_title.place(x=910+offset_param, y=15)
default_output_file_path = "default_output_image.png"

output_image = Image.open(default_output_file_path)
output_image = output_image.resize((DEFAULT_WIDTH, DEFAULT_HEIGHT), Image.ANTIALIAS)
output_photo = ImageTk.PhotoImage(output_image)

output_photo_panel = Label(window, image = output_photo,bg="white",relief="groove")
output_photo_panel.image = output_photo
output_photo_panel.place(x=800+offset_param,y=50)
"""

# browse input image
browse_btn = Button(window,text="Browse",width=7,command=open_explorer, bg="#337ab7",fg="white",font="none 10 bold")
browse_btn.place(x=520+offset_param, y=360)

#widgets for Scaling
scale_x = None
scale_x_entry = None
scale_y = None
scale_y_entry = None
interpolations_popup = None
interpolation_label = None
interpolation_choice = StringVar(window)
interpolation_techniques = ['Nearest Neigbhor','Bilinear','Cubic','Lanczos4']
interpolation_choice.set('Nearest Neigbhor')

#widgets for Rotation
degrees = None
degrees_entry = None
direction_label = None
popupMenu = None
direction = StringVar(window)
choices = ['Clockwise','Anti-Clockwise']
direction.set('Clockwise')

#widgets for Translation
translate_x = None
translate_x_entry = None
translate_y = None
translate_y_entry = None

init_widgets()

progress_canvas = None

# Operations
operation_label = Label(window,text="Select Operation",bg="white",fg="DodgerBlue",font=("Helvetica", 14))
operation_label.place(x=200+offset_param,y=400)

radiobtn_operation_var = IntVar()
radiobtn_operation_var.set(1)

opertions_dict = {}
init_operations()
keys = opertions_dict.keys()
total_operations = len(keys)
x_counter = 200
y_counter = 430
changed_col = False
for idx,key in enumerate(keys):
    option = Radiobutton(window,
                text=opertions_dict[key],
                padx=20,
                command=operation_changed,
                variable=radiobtn_operation_var,
                value=key,
                bg="white")
    option.place(x=x_counter+offset_param,y=y_counter)
    y_counter += 30
"""
# Interpolations
interpolation_label = Label(window,text="Select Interpolation",bg="white",fg="DodgerBlue",font=("Helvetica", 14))
interpolation_label.place(x=100+offset_param,y=490)

radiobtn_interpolation_var = IntVar()
radiobtn_interpolation_var.set(100)

interpolation_dict = {}
init_interpolations()
keys = interpolation_dict.keys()
total_interpolations = len(keys)
x_counter = 100
y_counter = 520
changed_col = False
for idx,key in enumerate(keys):
    option = Radiobutton(window,
                text=interpolation_dict[key],
                padx=20,
                variable=radiobtn_interpolation_var,
                value=key,
                bg="white")
    option.place(x=x_counter+offset_param,y=y_counter)
    x_counter += 200
    if not changed_col and idx >= total_interpolations/2-1:
        changed_col = True
        x_counter = 100
        y_counter = 550
"""

# output image size
#output_type_label = Label(window,text="Output Image",bg="white",fg="DodgerBlue",font=("Helvetica", 14))
#output_type_label.place(x=100+offset_param,y=490)

output_type_var = IntVar()
output_type_var.set(1000)

output_type_dict = {}
"""
init_output_types()
keys = output_type_dict.keys()
total_output_types = len(keys)
x_counter = 100
y_counter = 520
changed_col = False
for idx,key in enumerate(keys):
    option = Radiobutton(window,
                text=output_type_dict[key],
                padx=20,
                variable=output_type_var,
                value=key,
                bg="white")
    option.place(x=x_counter+offset_param,y=y_counter)
    x_counter += 200
"""

# ok button
ok_btn = Button(window,text="Show",width=7,command=show_result, bg="#5cb85c",fg="white",font="none 10 bold")
ok_btn.place(x=490+offset_param, y=620)

# reset button
reset_btn = Button(window,text="Reset",width=7,command=reset, bg="#d9534f",fg="white",font="none 10 bold")
reset_btn.place(x=570+offset_param, y=620)

#progress_bar = ttk.Progressbar(window,orient ="horizontal",length = 200, mode ="indeterminate")


params_label = Label(window,text="Parameters",bg="white",fg="DodgerBlue",font=("Helvetica", 14))
params_label.place(x=800+offset_param,y=395)
create_widgets(1)

window.mainloop()