import tkinter as tk
from tkinter import Menu, Toplevel, Label, Button
from tkinter.ttk import Combobox  # Combobox'u ttk'den import ettik
import webbrowser  # Link açmak için
import serial  # Seri portlarla iletişim için pySerial kütüphanesi

# Harfleri Mors koduna çeviren sözlük
morse_code = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    "0": "-----"
}

# Mors kodundan harflere çeviren sözlük (tersi)
text_code = {v: k for k, v in morse_code.items()}

def convert_to_morse(text):
    """Metni Mors koduna çevirir."""
    text = text.upper()
    result = []
    for char in text:
        if char == " ":
            result.append(" / ")  # Kelime arası boşluk
        elif char in morse_code:
            result.append(morse_code[char])
    return " ".join(result)

def convert_to_text(morse):
    """Morse kodunu metne çevirir."""
    morse_chars = morse.split(" ")
    result = []
    for morse_char in morse_chars:
        if morse_char == "/":
            result.append(" ")  # Kelime arası boşluk
        elif morse_char in text_code:
            result.append(text_code[morse_char])
    return "".join(result)

def on_convert():
    """Kullanıcıdan alınan metni veya morseyi çevirir."""
    input_text = input_field.get()
    if "." in input_text or "-" in input_text:
        # Morse kodu metne çevirme
        output_text = convert_to_text(input_text)
    else:
        # Normal metni Morse koduna çevirme
        output_text = convert_to_morse(input_text)
    output_label.config(text=output_text)

def copy_to_clipboard(event):
    """Çıktıyı kopyalar ve 3 saniye sonra mesajı gizler."""
    output_text = output_label.cget("text")
    if output_text:
        root.clipboard_clear()  # Mevcut panoyu temizle
        root.clipboard_append(output_text)  # Yeni metni panoya ekle
        root.update()  # Panoyu güncelle
        output_label.config(text="Kopyalandı: " + output_text)  # Kopyalandı mesajı göster
        root.after(3000, lambda: output_label.config(text=output_text))  # 3 saniye sonra orijinal metni geri yükle

def open_link(event):
    """Linke tıklandığında web sayfasını açar."""
    webbrowser.open("http://qrv73.com")

def on_comport_connect():
    """Bağlantı butonuna basıldığında comport seçim formu açılır."""
    # Comport penceresini oluştur
    comport_window = Toplevel(root)
    comport_window.title("Comport Seçimi")

    # Seri portları listele
    ports = serial.tools.list_ports.comports()

    label = Label(comport_window, text="Lütfen bir COM portu seçin:")
    label.pack(pady=10)

    # Combobox ile portları listeleme
    port_combobox = Combobox(comport_window, state="readonly", width=40)
    port_combobox['values'] = [port.device for port in ports]
    port_combobox.pack(pady=10)

    # Port seçildikten sonra işlemi gerçekleştiren buton
    def connect_to_port():
        selected_port = port_combobox.get()
        if selected_port:
            print(f"Bağlanılıyor: {selected_port}")
            comport_window.destroy()
        else:
            print("Port seçilmedi!")

    connect_button = Button(comport_window, text="Bağlan", command=connect_to_port)
    connect_button.pack(pady=10)

    cancel_button = Button(comport_window, text="İptal", command=comport_window.destroy)
    cancel_button.pack(pady=10)

# GUI'yi oluştur
root = tk.Tk()
root.title("Mors Kodu Çevirici")

# Pencereyi merkezleme
window_width = 500
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int((screen_height - window_height) / 2)
position_right = int((screen_width - window_width) / 2)
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Formun boyutlandırılmasını devre dışı bırak
root.resizable(False, False)

# Menü ekleme
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Bağlantı menüsü
connection_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Bağlantı", menu=connection_menu)
connection_menu.add_command(label="Comport Bağlan", command=on_comport_connect)

# Otomatik Oku Çevir checkbox ekleme
auto_convert_var = tk.BooleanVar()
menu_bar.add_checkbutton(label="Otomatik Oku Çevir", onvalue=True, offvalue=False, variable=auto_convert_var)

# Başlık etiketini oluştur (Büyük yazı)
title_label = tk.Label(root, text="QRV73 Morse Translator", font=("Helvetica", 24, "bold"), fg="blue")
title_label.pack(pady=20)

# Alt başlık (Mors kodunda yazı)
morse_title = convert_to_morse("QRV73 Morse Translator")
morse_label = tk.Label(root, text=morse_title, font=("Helvetica", 14, "italic"))
morse_label.pack(pady=10)

# Metin veya morse girişi
input_label = tk.Label(root, text="Metin veya Morse kodu girin:")
input_label.pack(pady=10)

input_field = tk.Entry(root, width=40)
input_field.pack(pady=5)

# Çevirme butonu
convert_button = tk.Button(root, text="Çevir", command=on_convert)
convert_button.pack(pady=10)

# Çıktı etiketi (kopyalama özelliği ile)
output_label = tk.Label(root, text="", width=40, height=4, relief="solid", cursor="hand2")
output_label.pack(pady=10)
output_label.bind("<Button-1>", copy_to_clipboard)  # Tıklanma olayını bağla

# Alt kısmı oluştur
footer_label = tk.Label(root, text="Programming By QRV73.com", fg="blue", cursor="hand2")
footer_label.pack(side="bottom", pady=10)
footer_label.bind("<Button-1>", open_link)

# GUI'yi başlat
root.mainloop()
