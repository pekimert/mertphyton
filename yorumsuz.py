import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode

def generate_qr_code():
    qr_data = "https://payment-portal.example.com"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save("qr_code.png")
    return "qr_code.png"

def complete_payment():
    messagebox.showinfo("Ödeme", "Ödeme tamamlandı!")
    selected_products_list.delete(0, tk.END)
    update_total_price()
    reset_selection_display()

def reset_selection_display():
    for widget in selection_frame.winfo_children():
        widget.destroy()
    selection_frame.grid_columnconfigure(0, weight=1)


def pay_with_qr():
    qr_code_path = generate_qr_code()
    qr_window = tk.Toplevel(root)
    qr_window.title("QR Kodu ile Ödeme")
    qr_window.geometry("300x450")
    img = Image.open(qr_code_path)
    qr_img = ImageTk.PhotoImage(img)
    qr_label = tk.Label(qr_window, image=qr_img)
    qr_label.image = qr_img
    qr_label.pack()
    
    tk.Button(qr_window, text="Ödemeyi Tamamla", command=lambda: [complete_payment(), qr_window.destroy()],
              bg="lightgreen", font=("Arial", 12)).pack(pady=10)

def pay_with_card():
    complete_payment()

def add_to_cart(product_name, product_price):
    current_items = len(selected_products_list.get(0, tk.END))
    col = current_items % 3
    row = current_items // 3

    if row >= 3:
        messagebox.showwarning("Uyarı", "Sepet dolu! Daha fazla ürün eklenemez.")
        return

    product_label = tk.Label(selection_frame, text=f"{product_name} - {product_price}", bg="white", font=("Arial", 10))
    product_label.grid(row=row, column=col, padx=5, pady=5)
    selected_products_list.insert(tk.END, f"{product_name} - {product_price}")
    update_total_price()

def update_total_price():
    total = 0
    for item in selected_products_list.get(0, tk.END):
        price = int(item.split('-')[-1].strip().replace("TL", ""))
        total += price
    total_price_label.config(text=f"{total} TL")

root = tk.Tk()
root.title("Otomat")
root.geometry("680x740")

bg_image = Image.open("x.png")  
bg_image = bg_image.resize((680, 740), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

products1 = [
    {"name": "Su", "price": "5 TL", "x": 195, "y": 285},
    {"name": "Cappy", "price": "10 TL", "x": 275, "y": 285},
    {"name": "Çikolata", "price": "15 TL", "x": 350, "y": 285},
]

for product in products1:
    tk.Label(root, text=product["name"], bg="white", font=("Arial", 12, "bold")).place(x=product["x"] + 15, y=product["y"])
    tk.Label(root, text=product["price"], bg="white", font=("Arial", 10)).place(x=product["x"]+15, y=product["y"]-20)
    tk.Button(root, text="+", command=lambda p=product: add_to_cart(p["name"], p["price"]), bg="lightgrey", font=("Arial", 10), width=2, height=1).place(x=product["x"] + 20, y=product["y"] - 55)

products = [
{"name": "Gofret", "price": "5 TL", "x": 183, "y": 385},
{"name": "Kraker", "price": "10 TL", "x": 265, "y": 385},
{"name": "Şeker", "price": "15 TL", "x": 350, "y": 385},
]

for product in products:
    tk.Label(root, text=product["name"], bg="white", font=("Arial", 12, "bold")).place(x=product["x"] + 15, y=product["y"])
    tk.Label(root, text=product["price"], bg="white", font=("Arial", 10)).place(x=product["x"]+20, y=product["y"]-20)
    tk.Button(root, text="+", command=lambda p=product: add_to_cart(p["name"], p["price"]), bg="lightgrey", font=("Arial", 10), width=2, height=1).place(x=product["x"] + 30, y=product["y"] - 50)

products2 = [
{"name": "Mocha", "price": "5 TL", "x": 186, "y": 510},
{"name": "Latte", "price": "10 TL", "x": 275, "y": 510},
{"name": "Kinder", "price": "15 TL", "x": 347, "y": 510},
]

for product in products2:
    tk.Label(root, text=product["name"], bg="white", font=("Arial", 12, "bold")).place(x=product["x"] + 10, y=product["y"])
    tk.Label(root, text=product["price"], bg="white", font=("Arial", 10)).place(x=product["x"]+17, y=product["y"]-20)
    tk.Button(root, text="+", command=lambda p=product: add_to_cart(p["name"], p["price"]), bg="lightgrey", font=("Arial", 10), width=2, height=1).place(x=product["x"] + 25, y=product["y"] - 50)

selection_frame = tk.Frame(root, bg="white", width=300, height=100)
selection_frame.place(x=170, y=560)
selection_frame.grid_columnconfigure(0, weight=1)

selected_products_list = tk.Listbox(root, font=("Arial", 10), height=3, width=37)
selected_products_list.place_forget()

total_price_label = tk.Label(root, text="0 TL", bg="lightblue", font=("Arial", 12, "bold"))
total_price_label.place(x=473, y=298)

tk.Button(root, text="QR", command=pay_with_qr, bg="lightgreen", font=("Arial", 12), width=5, height=4).place(x=470, y=180)
tk.Button(root, text="Kredi Kart", command=pay_with_card, bg="lightblue", font=("Arial", 12),width=8, height=2).place(x=455, y=490)

root.mainloop()