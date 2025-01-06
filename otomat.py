import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode

secili_urunler_stack = []
secili_urunler_etiketleri = []  

def qr_kodu_olustur():
    qr_verisi = "https://payment-portal.example.com"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_verisi)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save("qr_kodu.png")
    return "qr_kodu.png"

def odeme_tamamlandi():
    messagebox.showinfo("Ödeme", "Ödeme tamamlandı!")
    secili_urunler_listesi.delete(0, tk.END)
    toplam_fiyati_guncelle()
    secim_ekranini_sifirla()

def secim_ekranini_sifirla():
    for widget in secim_cercevesi.winfo_children():
        widget.destroy()
    secim_cercevesi.grid_columnconfigure(0, weight=1)

def qr_ile_odeme():
    qr_kodu_yolu = qr_kodu_olustur()
    qr_penceresi = tk.Toplevel(kok)
    qr_penceresi.title("QR Kodu ile Ödeme")
    qr_penceresi.geometry("300x450")
    img = Image.open(qr_kodu_yolu)
    qr_img = ImageTk.PhotoImage(img)
    qr_label = tk.Label(qr_penceresi, image=qr_img)
    qr_label.image = qr_img
    qr_label.pack()

    tk.Button(qr_penceresi, text="Ödemeyi Tamamla", command=lambda: [odeme_tamamlandi(), qr_penceresi.destroy()],
              bg="lightgreen", font=("Arial", 12)).pack(pady=10)

def kart_ile_odeme():
    odeme_tamamlandi()

def sepete_ekle(urun_adi, urun_fiyati):
    mevcut_urunler = len(secili_urunler_listesi.get(0, tk.END))
    kol = mevcut_urunler % 3
    satir = mevcut_urunler // 3

    if satir >= 3:
        messagebox.showwarning("Uyarı", "Sepet dolu! Daha fazla ürün eklenemez.")
        return

    secili_urunler_stack.append((urun_adi, urun_fiyati))

    urun_etiketi = tk.Label(secim_cercevesi, text=f"{urun_adi} - {urun_fiyati}", bg="white", font=("Arial", 10))
    urun_etiketi.grid(row=satir, column=kol, padx=5, pady=5)
    secili_urunler_listesi.insert(tk.END, f"{urun_adi} - {urun_fiyati}")
    secili_urunler_etiketleri.append(urun_etiketi)

    toplam_fiyati_guncelle()

def geri_urun_al():
    if secili_urunler_stack:
        urun_adi, urun_fiyati = secili_urunler_stack.pop()
        
        secili_urunler_listesi.delete(tk.END)

        if secili_urunler_etiketleri:
            son_etiket = secili_urunler_etiketleri.pop()  
            son_etiket.destroy()  

        toplam_fiyati_guncelle()
    else:
        messagebox.showwarning("Uyarı", "Sepet boş, geri alınacak ürün yok!")

def toplam_fiyati_guncelle():
    toplam = 0
    for urun in secili_urunler_listesi.get(0, tk.END):
        fiyat = int(urun.split('-')[-1].strip().replace("TL", ""))
        toplam += fiyat
    toplam_fiyat_etiketi.config(text=f"{toplam} TL")

kok = tk.Tk()
kok.title("Otomat")
kok.geometry("680x740")

arka_plan_resmi = Image.open("x.png")
arka_plan_resmi = arka_plan_resmi.resize((680, 740), Image.Resampling.LANCZOS)
arka_plan_fotosu = ImageTk.PhotoImage(arka_plan_resmi)
arka_plan_etiketi = tk.Label(kok, image=arka_plan_fotosu)
arka_plan_etiketi.place(relwidth=1, relheight=1)

urunler1 = [
    {"name": "Su", "price": "5 TL", "x": 195, "y": 285},
    {"name": "Cappy", "price": "10 TL", "x": 275, "y": 285},
    {"name": "Çikolata", "price": "15 TL", "x": 350, "y": 285},
]

for urun in urunler1:
    tk.Label(kok, text=urun["name"], bg="lightblue", font=("Arial", 12, "bold")).place(x=urun["x"] + 15, y=urun["y"])
    tk.Label(kok, text=urun["price"], bg="#edeae0", font=("Arial", 10, "bold")).place(x=urun["x"] + 15, y=urun["y"] - 20)
    tk.Button(kok, text="+", command=lambda p=urun: sepete_ekle(p["name"], p["price"]), bg="lightgrey", font=("Arial", 10),
               width=2, height=1).place(x=urun["x"] + 20, y=urun["y"] - 55)

urunler2 = [
    {"name": "Gofret", "price": "5 TL", "x": 183, "y": 385},
    {"name": "Kraker", "price": "10 TL", "x": 265, "y": 385},
    {"name": "Şeker", "price": "15 TL", "x": 350, "y": 385},
]

for urun in urunler2:
    tk.Label(kok, text=urun["name"], bg="lightblue", font=("Arial", 12, "bold")).place(x=urun["x"] + 15, y=urun["y"])
    tk.Label(kok, text=urun["price"], bg="#edeae0", font=("Arial", 10, "bold")).place(x=urun["x"] + 20, y=urun["y"] - 20)
    tk.Button(kok, text="+", command=lambda p=urun: sepete_ekle(p["name"], p["price"]), bg="lightgrey", font=("Arial", 10), 
              width=2, height=1).place(x=urun["x"] + 30, y=urun["y"] - 50)

urunler3 = [
    {"name": "Mocha", "price": "5 TL", "x": 186, "y": 510},
    {"name": "Latte", "price": "10 TL", "x": 275, "y": 510},
    {"name": "Kinder", "price": "15 TL", "x": 347, "y": 510},
]

for urun in urunler3:
    tk.Label(kok, text=urun["name"], bg="lightgrey", font=("Arial", 12, "bold")).place(x=urun["x"] + 10, y=urun["y"])
    tk.Label(kok, text=urun["price"], bg="#edeae0", font=("Arial", 10, "bold")).place(x=urun["x"] + 17, y=urun["y"] - 20)
    tk.Button(kok, text="+", command=lambda p=urun: sepete_ekle(p["name"], p["price"]), bg="lightgrey", font=("Arial", 10), 
              width=2, height=1).place(x=urun["x"] + 25, y=urun["y"] - 50)

secim_cercevesi = tk.Frame(kok, bg="#98817b", width=264, height=60)
secim_cercevesi.place(x=170, y=560)
secim_cercevesi.grid_columnconfigure(0, weight=1)

secili_urunler_listesi = tk.Listbox(kok, font=("Arial", 10, "bold"), height=3, width=37)
secili_urunler_listesi.place_forget()

toplam_fiyat_etiketi = tk.Label(kok, text="0 TL", bg="#04b4dc", font=("Arial", 12, "bold"))
toplam_fiyat_etiketi.place(x=475, y=298)

tk.Button(kok, text="QR", command=qr_ile_odeme, bg="lightgreen", font=("Arial", 12), width=5, height=4).place(x=470, y=180)
tk.Button(kok, text="Kredi Kart", command=kart_ile_odeme, bg="lightblue", font=("Arial", 12), width=8, height=2).place(x=455, y=490)
tk.Button(kok, text="Geri Al", command=geri_urun_al, bg="lightcoral", font=("Arial", 12), width=8, height=2).place(x=455, y=430)

kok.mainloop()
