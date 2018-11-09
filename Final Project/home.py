from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from Tranformations import Transformations
import cv2

DEFAULT_WIDTH = 300
DEFAULT_HEIGHT = 300


# open browser
def open_explorer():
    open_explorer.selected_file = filedialog.askopenfilename(initialdir="./")
    #print("selected file is : ",  open_explorer.selected_file)
    selected_image = Image.open(open_explorer.selected_file)
    selected_image = selected_image.resize((DEFAULT_WIDTH,DEFAULT_HEIGHT))
    selected_photo = ImageTk.PhotoImage(selected_image)
    input_photo_panel = Label(window, image=selected_photo, bg="white", relief="groove")
    input_photo_panel.image = selected_photo
    input_photo_panel.place(x=200+offset_param, y=50)


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
        translate_x_entry.insert(0,"1")
        translate_y.place(x=800+offset_param, y=457)
        translate_y_entry.place(x=900+offset_param, y=460)
        translate_y_entry.insert(0, "1")


def operation_changed():
    print("Operation changed")
    value = int(radiobtn_operation_var.get())
    #print(direction.get())
    remove_all_widgets()
    create_widgets(value)


def init_widgets():
    global scale_x, scale_x_entry, scale_y, scale_y_entry,interpolation_label,interpolations_popup
    global degrees, degrees_entry, direction_label,popupMenu
    global translate_x, translate_x_entry, translate_y, translate_y_entry

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


def transform_image():
    operation_var = int(radiobtn_operation_var.get())
    operation = opertions_dict[operation_var]
    image_display_var = int(output_type_var.get())
    show_full_image = False
    if image_display_var == 2000:
        show_full_image = True

    if operation == 'Scaling':
        x_factor = float(scale_x_entry.get())
        y_factor = float(scale_y_entry.get())
        selected_interpolation = interpolation_choice.get()
        transformation_ref = Transformations()
        output_img_name, height, width= transformation_ref.scale(open_explorer.selected_file, x_factor, y_factor,selected_interpolation,show_full_image)
        place_output_image(output_img_name, height, width)


def place_output_image(output_img_name, height, width):
    output_image = Image.open(output_img_name)
    output_image = output_image.resize((width, height), Image.ANTIALIAS)
    output_photo = ImageTk.PhotoImage(output_image)

    output_photo_panel = Label(window, image=output_photo, bg="white", relief="groove")
    output_photo_panel.image = output_photo
    output_photo_panel.place(x=800 + offset_param, y=50)

    output_canvas = Toplevel()
    canvas = Canvas(output_canvas, width=width, height=height)
    canvas.pack(expand=YES, fill=BOTH)
    
    # image not visual
    canvas.create_image(50, 10, image=output_photo, anchor=NW)
    # assigned the gif1 to the canvas object
    canvas.img = output_photo


window = Tk()

#size of the window
window.geometry("1000x500")
window.title("Image Geometric Transformations")
window.configure(background="white")
offset_param = 0
# placing input image
input_title = Label(window,text="INPUT",bg="white",fg="Tomato",font=("Helvetica", 16))
input_title.place(x=310+offset_param, y=15)
default_input_file_path = "default_input_image.png"

input_image = Image.open(default_input_file_path)
input_image = input_image.resize((DEFAULT_WIDTH, DEFAULT_HEIGHT), Image.ANTIALIAS)
input_photo = ImageTk.PhotoImage(input_image)

input_photo_panel = Label(window, image = input_photo,bg="white",relief="groove")
input_photo_panel.image = input_photo
input_photo_panel.place(x=200+offset_param,y=50)

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

# browse input image
browse_btn = Button(window,text="Browse",width=10,command=open_explorer, bg="DodgerBlue",fg="white",font="none 10 bold")
browse_btn.place(x=310+offset_param, y=360)

#widgets for Scaling
scale_x = None
scale_x_entry = None
scale_y = None
scale_y_entry = None
interpolations_popup = None
interpolation_label = None
interpolation_choice = StringVar(window)
interpolation_techniques = {'Nearest Neigbhor','Bilinear','Cubic','Lanczos4'}
interpolation_choice.set('Nearest Neigbhor')

#widgets for Rotation
degrees = None
degrees_entry = None
direction_label = None
popupMenu = None
direction = StringVar(window)
choices = {'Clockwise','Anti-Clockwise'}
direction.set('Clockwise')

#widgets for Translation
translate_x = None
translate_x_entry = None
translate_y = None
translate_y_entry = None

init_widgets()

# Operations
operation_label = Label(window,text="Select Operation",bg="white",fg="DodgerBlue",font=("Helvetica", 14))
operation_label.place(x=100+offset_param,y=400)

radiobtn_operation_var = IntVar()
radiobtn_operation_var.set(1)

opertions_dict = {}
init_operations()
keys = opertions_dict.keys()
total_operations = len(keys)
x_counter = 100
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
    x_counter += 175
    if not changed_col and idx >= total_operations/2 - 1:
        changed_col = True
        x_counter = 100
        y_counter = 460
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
output_type_label = Label(window,text="Output Image",bg="white",fg="DodgerBlue",font=("Helvetica", 14))
output_type_label.place(x=100+offset_param,y=490)

output_type_var = IntVar()
output_type_var.set(1000)

output_type_dict = {}
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


# ok button
ok_btn = Button(window,text="Ok",width=5,command=transform_image, bg="DodgerBlue",fg="white",font="none 10 bold")
ok_btn.place(x=330+offset_param, y=560)

# save button
save_btn = Button(window,text="Save",width=5, bg="DodgerBlue",fg="white",font="none 10 bold")
save_btn.place(x=400+offset_param, y=560)


params_label = Label(window,text="Parameters",bg="white",fg="DodgerBlue",font=("Helvetica", 14))
params_label.place(x=800+offset_param,y=395)
create_widgets(1)

window.mainloop()