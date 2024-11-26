import tkinter as tk
from tkinter import colorchooser
from colorsys import rgb_to_hsv, hsv_to_rgb

def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c / 100) * (1 - k / 100)
    g = 255 * (1 - m / 100) * (1 - k / 100)
    b = 255 * (1 - y / 100) * (1 - k / 100)
    return int(r), int(g), int(b)

def rgb_to_cmyk(r, g, b):
    r /= 255.0
    g /= 255.0
    b /= 255.0

    k = 1 - max(r, g, b)
    if k < 1:
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
    else:
        c = m = y = 0

    return int(c * 100), int(m * 100), int(y * 100), int(k * 100)

def rgb_to_hsv_manual(r, g, b):
    r /= 255.0
    g /= 255.0
    b /= 255.0

    v = max(r, g, b)
    min_value = min(r, g, b)

    if v == 0:
        s = 0
    else:
        s = (v - min_value) / v

    if v - min_value == 0:
        h = 0  
    elif v == r:
        h = (60 * ((g - b) / (v - min_value)) + 360) % 360
    elif v == g:
        h = (60 * ((b - r) / (v - min_value)) + 120) % 360
    elif v == b:
        h = (60 * ((r - g) / (v - min_value)) + 240) % 360
    
    return int(h), int(s * 100), int(v * 100)

def update_color(c, m, y, k):
    c = int(c)
    m = int(m)
    y = int(y)
    k = int(k)

    # Convert CMYK to RGB
    r, g, b = cmyk_to_rgb(c, m, y, k)

    # Update CMYK display frame
    cmyk_color = f'#{r:02x}{g:02x}{b:02x}'
    cmyk_frame.config(bg=cmyk_color)
    cmyk_display.config(text=f"CMYK: ({c}%, {m}%, {y}%, {k}%)")

    # Update RGB display frame
    rgb_display_text = f"RGB: ({r}, {g}, {b})"
    rgb_display.config(text=rgb_display_text)
    rgb_frame.config(bg=cmyk_color)

    # Convert RGB to HSV
    h, s, v = rgb_to_hsv_manual(r, g, b)

    # Update HSV display frame
    hsv_display_text = f"HSV: ({h}, {s}%, {v}%)"
    hsv_display.config(text=hsv_display_text)
    hsv_color = hsv_to_rgb(h / 360.0, s / 100.0, v / 100.0)
    hsv_color_hex = f'#{int(hsv_color[0] * 255):02x}{int(hsv_color[1] * 255):02x}{int(hsv_color[2] * 255):02x}'
    hsv_frame.config(bg=hsv_color_hex)

    # Sync sliders
    c_slider.set(c)
    m_slider.set(m)
    y_slider.set(y)
    k_slider.set(k)

def set_cmyk_from_text_fields():
    try:
        c = float(cmyk_c_entry.get())
        m = float(cmyk_m_entry.get())
        y = float(cmyk_y_entry.get())
        k = float(cmyk_k_entry.get())
        if all(0 <= value <= 100 for value in (c, m, y, k)):
            update_color(c, m, y, k)
        else:
            print("CMYK values must be between 0 and 100")
    except ValueError:
        print("Please enter valid numeric values for CMYK")

def update_color_from_sliders(value):
    """Update the color from the current slider values."""
    c = c_slider.get()
    m = m_slider.get()
    y = y_slider.get()
    k = k_slider.get()
    update_color(c, m, y, k)

def pick_color():
    """Open color chooser and update CMYK values according to the selected RGB color."""
    color_code = colorchooser.askcolor(title="Choose a color")
    if color_code[0]:  # If a color was selected
        r, g, b = map(int, color_code[0])  # Get the RGB values
        # Convert RGB to CMYK
        cmyk_values = rgb_to_cmyk(r, g, b)
        update_color(*cmyk_values)




root = tk.Tk()
root.title("CMYK to RGB to HSV Color Converter")
cmyk_label = tk.Label(root, text="CMYK Color Converter", font=("Arial", 24))
cmyk_label.grid(row=0, column=0, pady=10, columnspan=3)

#frame CMYK
cmyk_frame = tk.Frame(root, height=100, width=300, bg="white", borderwidth=2, relief="solid")
cmyk_frame.grid(row=1, column=0, pady=10, padx=10)
cmyk_frame.pack_propagate(False)  
cmyk_display = tk.Label(cmyk_frame, text="CMYK: (0%, 0%, 0%, 0%)", font=("Arial", 16), bg="white")
cmyk_display.pack()

#frame RGB
rgb_frame = tk.Frame(root, height=100, width=300, bg="white", borderwidth=2, relief="solid")
rgb_frame.grid(row=1, column=1, pady=10, padx=10)
rgb_frame.pack_propagate(False)
rgb_display = tk.Label(rgb_frame, text="RGB: (0, 0, 0)", font=("Arial", 16), bg="white")
rgb_display.pack()

#frame HSV 
hsv_frame = tk.Frame(root, height=100, width=300, bg="white", borderwidth=2, relief="solid")
hsv_frame.grid(row=1, column=2, pady=10, padx=10)
hsv_frame.pack_propagate(False)
hsv_display = tk.Label(hsv_frame, text="HSV: (0, 0%, 0%)", font=("Arial", 16), bg="white")
hsv_display.pack()

# text input
tk.Label(root, text="Cyan (%):").grid(row=5, column=0,padx=5,sticky='e')
tk.Label(root, text="Magenta (%):").grid(row=6, column=0,padx=5,sticky='e')
tk.Label(root, text="Yellow (%):").grid(row=7, column=0,padx=5,sticky='e')
tk.Label(root, text="Key/Black (%):").grid(row=8, column=0,padx=5,sticky='e')

cmyk_c_entry = tk.Entry(root, width=5)
cmyk_c_entry.grid(row=5, column=1, padx=5,sticky='w')
cmyk_m_entry = tk.Entry(root, width=5)
cmyk_m_entry.grid(row=6, column=1, padx=5,sticky='w')
cmyk_y_entry = tk.Entry(root, width=5)
cmyk_y_entry.grid(row=7, column=1, padx=5,sticky='w')
cmyk_k_entry = tk.Entry(root, width=5)
cmyk_k_entry.grid(row=8, column=1, padx=5,sticky='w')

set_button = tk.Button(root, text="Set", command=set_cmyk_from_text_fields)
set_button.grid(row=4, column=0, pady=10, sticky='s')

#color dialogue
pick_color_button = tk.Button(root, text="Pick Color", command=pick_color)
pick_color_button.grid(row=4, column=2, pady=10,sticky='s')

#slider dialogue
c_slider = tk.Scale(root, from_=0, to=100, orient='horizontal', label='Cyan',
                    command=lambda value: update_color_from_sliders(value))
c_slider.grid(row=3, column=0, pady=5)

m_slider = tk.Scale(root, from_=0, to=100, orient='horizontal', label='Magenta',
                    command=lambda value: update_color_from_sliders(value))
m_slider.grid(row=3, column=1, pady=5)

y_slider = tk.Scale(root, from_=0, to=100, orient='horizontal', label='Yellow',
                    command=lambda value: update_color_from_sliders(value))
y_slider.grid(row=3, column=2, pady=5)

k_slider = tk.Scale(root, from_=0, to=100, orient='horizontal', label='Key/Black',
                    command=lambda value: update_color_from_sliders(value))
k_slider.grid(row=4, column=1, pady=5)

root.mainloop()
