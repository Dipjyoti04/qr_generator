import tkinter as tk 
from tkinter import messagebox, filedialog, colorchooser
from PIL import Image, ImageTk, ImageColor
import qrcode
import io
import re
from qrcode.image.styles.moduledrawers import SquareModuleDrawer, CircleModuleDrawer, RoundedModuleDrawer
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H



#______________________________________________________________________________________
#This script is a GUI version of the qr_generator.py. IT has many options and features as like a app. $-}
#If you found this useful buy me a coffe 😉🍵
#--------------------------------------------------------------------------------------


# Global Variables
qr_image_global = None
last_url = None
qr_fg_color = "black"
qr_bg_color = "white"
qr_box_size = 10
qr_border_size = 4
qr_error_level = ERROR_CORRECT_L
qr_style = "square"  # Options: square, circle, dot


def sanitize_filename(url):
    return re.sub(r'[\\/*?:"<>|]', '_', url).strip().replace("https://", "").replace("http://", "").replace("/", "_")


def generate_qr():
    global qr_image_global, last_url

    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL.")
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    last_url = url

    fg_rgb = ImageColor.getrgb(qr_fg_color)
    bg_rgb = ImageColor.getrgb(qr_bg_color)

    if fg_rgb == bg_rgb:
        messagebox.showerror("Color Error", "Foreground and background colors cannot be the same.")
        return

    qr = qrcode.QRCode(
        version=None,
        error_correction=qr_error_level,
        box_size=qr_box_size,
        border=qr_border_size,
    )
    qr.add_data(url)
    qr.make(fit=True)

    drawer_map = {
        "square": SquareModuleDrawer(),
        "circle": CircleModuleDrawer(),
        "dot": RoundedModuleDrawer()
    }

    try:
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=drawer_map.get(qr_style, SquareModuleDrawer()),
            color_mask=SolidFillColorMask(front_color=fg_rgb, back_color=bg_rgb)
        )
    except Exception as e:
        messagebox.showerror("QR Generation Error", str(e))
        return

    qr_image_global = img

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img = Image.open(buffer)
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)

    qr_label.config(image=tk_img)
    qr_label.image = tk_img
    download_button.pack(pady=5)
    edit_button.pack(pady=5)
    revert_button.pack(pady=5, side="right")


def save_qr():
    if qr_image_global is None or last_url is None:
        messagebox.showwarning("No QR Code", "Please generate a QR code first.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                    initialfile=sanitize_filename(last_url) + ".png",
                    filetypes=[("PNG files", "*.png")])
    if file_path:
        qr_image_global.save(file_path)
        messagebox.showinfo("Saved", f"QR code saved to:\n{file_path}")


def set_fg_color():
    global qr_fg_color
    color = colorchooser.askcolor(title="Choose QR Color")[1]
    if color:
        qr_fg_color = color
        generate_qr()


def set_bg_color():
    global qr_bg_color
    color = colorchooser.askcolor(title="Choose Background Color")[1]
    if color:
        qr_bg_color = color
        generate_qr()


def update_box_size(value):
    global qr_box_size
    qr_box_size = int(value)
    generate_qr()


def update_border_size(value):
    global qr_border_size
    qr_border_size = int(value)
    generate_qr()


def set_style(style):
    global qr_style
    qr_style = style
    generate_qr()


def set_error_level(level):
    global qr_error_level
    qr_error_level = {
        "L": ERROR_CORRECT_L,
        "M": ERROR_CORRECT_M,
        "Q": ERROR_CORRECT_Q,
        "H": ERROR_CORRECT_H
    }[level]
    generate_qr()


def toggle_customization():
    if customize_frame.winfo_ismapped():
        customize_frame.pack_forget()
    else:
        customize_frame.pack(pady=5)


def revert_qr():
    global qr_fg_color, qr_bg_color, qr_style, qr_error_level, qr_border_size
    qr_fg_color = "black"
    qr_bg_color = "white"
    qr_style = "square"
    qr_error_level = ERROR_CORRECT_L
    qr_border_size = 4
    generate_qr()

# GUI Setup
root = tk.Tk()
root.iconbitmap('icon.ico')
root.title("QR Generator")
root.geometry("400x790")
root.configure(bg="#ace5ff")
root.resizable(False, False)

button_style = {
    "bg": "#6FC5FF", "fg": "#fff", "font": ("Arial", 11, "bold"),
    "activebackground": "#5fb5ef", "activeforeground": "#fff",
    "relief": "flat", "bd": 0, "padx": 20, "pady": 10, "highlightthickness": 0
}

rounded_corner = {"border": 0, "highlightthickness": 0}

style_all_buttons = {
    **button_style,
    "highlightbackground": "#6FC5FF",
    "highlightcolor": "#6FC5FF",
    "bd": 0
}

entry_style = {"relief": "flat", "highlightthickness": 0, "bd": 0, "justify": "center"}


qr_label_frame = tk.Frame(root, bg="#ace5ff")
tk.Label(root, text="QR Generator", font=("Arial", 16, "bold"), bg="#ace5ff", fg="black").pack(pady=(25, 5))

url_entry = tk.Entry(root, font=("Arial", 12), width=30, **entry_style)
url_entry.pack(pady=5)

tk.Button(root, text="Generate QR Code", command=generate_qr, **style_all_buttons).pack(pady=8)

qr_label = tk.Label(qr_label_frame, bg="#ace5ff")
qr_label.pack(side="left", padx=5)

revert_button = tk.Button(qr_label_frame, text="↺", command=revert_qr, font=("Arial", 14, "bold"), bg="#6FC5FF", fg="white", relief="flat", bd=0, highlightthickness=0)
revert_button.pack(side="right", padx=5)
qr_label_frame.pack(pady=10)

download_button = tk.Button(root, text="Download QR", command=save_qr, **style_all_buttons)
edit_button = tk.Button(root, text="Edit QR", command=toggle_customization, **style_all_buttons)

customize_frame = tk.Frame(root, bg="#ace5ff")

color_frame = tk.Frame(customize_frame, bg="#ace5ff")
tk.Button(color_frame, text="QR Color", command=set_fg_color, **style_all_buttons).pack(side="left", padx=5)
tk.Button(color_frame, text="QR BG Color", command=set_bg_color, **style_all_buttons).pack(side="left", padx=5)
color_frame.pack(pady=4)

tk.Label(customize_frame, text="QR Style", bg="#ace5ff", fg="black", font=("Arial", 10)).pack()
style_frame = tk.Frame(customize_frame, bg="#ace5ff")
tk.Button(style_frame, text="Square", command=lambda: set_style("square"), **style_all_buttons).pack(side="left", padx=5)
tk.Button(style_frame, text="Circle", command=lambda: set_style("circle"), **style_all_buttons).pack(side="left", padx=5)
tk.Button(style_frame, text="Dot", command=lambda: set_style("dot"), **style_all_buttons).pack(side="left", padx=5)
style_frame.pack(pady=4)

tk.Label(customize_frame, text="Border Size", bg="#ace5ff", fg="black", font=("Arial", 10)).pack()
tk.Scale(customize_frame, from_=1, to=10, orient="horizontal", bg="#ace5ff", fg="black",
         troughcolor="#6FC5FF", highlightthickness=0, command=update_border_size, length=200).pack(pady=2)

tk.Label(customize_frame, text="Error Correction", bg="#ace5ff", fg="black", font=("Arial", 10)).pack()
error_frame = tk.Frame(customize_frame, bg="#ace5ff")
tk.Button(error_frame, text="L (7%)", command=lambda: set_error_level("L"), **style_all_buttons).pack(side="left", padx=5)
tk.Button(error_frame, text="M (15%)", command=lambda: set_error_level("M"), **style_all_buttons).pack(side="left", padx=5)
tk.Button(error_frame, text="Q (25%)", command=lambda: set_error_level("Q"), **style_all_buttons).pack(side="left", padx=5)
tk.Button(error_frame, text="H (30%)", command=lambda: set_error_level("H"), **style_all_buttons).pack(side="left", padx=5)
error_frame.pack(pady=4)

root.mainloop()