import tkinter as tk
import ctypes

# Windows kütüphanelerini tanımlama (Tıklama engelini kaldırmak için)
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020

def tiklama_engelini_kaldir(window):
    # Pencerenin Windows üzerindeki kimlik numarasını (handle) alıyoruz
    hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
    # Mevcut pencere stillerini alıyoruz
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    # Şeffaflık ve tıklamayı arkaya geçirme özelliklerini ekliyoruz
    style |= WS_EX_LAYERED | WS_EX_TRANSPARENT
    # Yeni stili pencereye uyguluyoruz
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

# Örnek Pencere Tanımlaması (Projenizdeki pencereler için uygulayın)
root = tk.Tk()
root.attributes("-topmost", True)  # Her zaman üstte kalma özelliği

# --- EKLEMENİZ GEREKEN KRİTİK KISIM ---
# Kedi veya Top penceresi oluşturulduktan hemen sonra bu fonksiyonu çağırın:
tiklama_engelini_kaldir(root) 
# --------------------------------------

root.mainloop()
