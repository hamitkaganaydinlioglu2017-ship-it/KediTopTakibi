
# *******************************************************************************
# * PROJE ADI          : KediTopTakibi
# * SİSTEM TANIMI      : Masaüstü Kedi Top Takip Uygulaması
# * GELİŞTİRİCİ        : Abdulkadir GÜNGÖR (a.kadir.gungor.86@gmail.com)
# *                      (Web Sitesi: https://abdulkadirgungor.com )
# * TARİH              : 2026-07-08
# * TEKNİK GEREKSİNİM  : Python 3.x / Tkinter Framework
# *  
# * KÜTÜPHANE SÜRÜMLERİ:
# * 1) pyautogui v0.9.54 (veya üzeri)
# * 2) keyboard v0.13.5 (veya üzeri - opsiyonel)
# *  
# * YAZILIM VE DONANIM :
# * - İşletim Sistemi  : Windows, Linux veya macOS (Ses desteği Windows odaklıdır)
# * - Ses Dosyası      : KediMirlama.wav (Uygulama dizininde yer almalıdır)
# *  
# * KONTROL ARA YÜZÜ   : Fare (Mouse) hareketleri ile global takip
# *******************************************************************************

import tkinter as tk
import math
import random
import sys
import os
import time

# Fareyi ve ekran koordinatlarını yakalayabilmek için pyautogui kütüphanesini içeri alıyoruz.
try:
    import pyautogui
    # Fare ekranın en köşesine gittiğinde uygulamanın çökmesini engellemek için failsafe modunu kapatıyoruz.
    pyautogui.FAILSAFE = False
except ImportError:
    print("HATA: pyautogui bulunamadı. Kurmak için: pip install pyautogui")
    sys.exit(1)

# Klavye kısayollarını (Ctrl+Alt+Q vb.) dinleyebilmek için keyboard kütüphanesini kontrol ediyoruz.
try:
    import keyboard
    HAS_KEYBOARD = True
except ImportError:
    HAS_KEYBOARD = False

# Windows platformunda arka planda kedi mırlama sesi çalabilmek için winsound kütüphanesine bakıyoruz.
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False


def resource_path(relative_path):
    """
    Bu fonksiyon projenin hem ham .py dosyası olarak çalışırken hem de PyInstaller 
    ile tek bir .exe haline getirildiğinde gömülü kaynak dosyalarını (örneğin .wav sesini) 
    doğru geçici klasörden bulabilmesi için yolu dinamik olarak ayarlar.
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller paketlendiğinde geçici dosyaları buraya açar
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__)) # Normal çalışmada dosya dizini
    return os.path.join(base_path, relative_path)


# Kedimizin çıkaracağı mırlama ses dosyasının tam yolunu sisteme tanıtıyoruz.
PURR_SOUND_FILE = resource_path("KediMirlama.wav")

# --- GENEL AYARLAR VE HASSASİYET PARAMETRELERİ ---
CLICK_THROUGH = True          # True ise kedi ve top ekrandayken altındaki masaüstü simgelerine tıklanabilir.
TRANSPARENT_KEY = "#010101"   # Arka planın tamamen şeffaf görünmesi için kullanılacak maske rengi.
FPS = 60                      # Ekran yenileme hızımız (Saniyede 60 kare cizim yapılacak).
CAT_SPEED = 0.06              # Kedinin topa yaklaşırkenki yumuşak ivmesi (Sayı büyürse kedi çok hızlı koşar).
BALL_SPEED = 0.18             # Beyaz topun fare imlecini takip etme esnekliği.
STOP_DISTANCE = 70            # Kedi topa bu kadar piksel yaklaşınca durup beklemeye geçecek.

BORED_AFTER_SECONDS = 5.0     # Kedi kaç saniye boyunca hareketsiz kalırsa sıkılma moduna geçsin?
BUBBLE_DURATION = 4.0         # Konuşma balonunun ekranda kalacağı süre (saniye cinsinden).

# Kedimizin sıkıldığı anlarda rastgele söyleyeceği 100 farklı eğlenceli cümle havuzu.
BUBBLE_TEXTS = [
    "Sıkıldım. Hadi devam edelim.", "Miyav... top nerede kaldı?", "Ben buradayım, sen neredesin?",
    "Uyuklamaya başlayacağım az kalsın.", "Top ile oynamak istiyorum!", "Hey, unuttun mu beni?",
    "Kuyruğumu sallamaktan yoruldum.", "Biraz hareket lazım bana.", "Fareyi biraz oynat da göreyim.",
    "Patilerim uyuşmaya başladı.", "Bekliyorum, top nerede?", "Canım sıkılıyor ama seni seviyorum.",
    "Şekerim, biraz ilgi ister miyim?", "Miyav miyav, oyun zamanı!", "Kuyruğum sabırsızlıkla titriyor.",
    "Hazırım, top gelsin!", "Bir kedi bu kadar bekler mi?", "Gözlerim kapanıyor, uyandır beni.",
    "Top uzaklaştı, üzüldüm.", "Haydi biraz koşalım!", "Kulaklarım seni dinliyor.",
    "Pati atlamaya hazırım.", "Şu an tam bir tembel kedi gibiyim.", "Biraz hareket görmek isterim.",
    "Kediler de sıkılır bilirsin.", "Top nerede saklandı acaba?", "Zıplamak için can atıyorum.",
    "Uykum geliyor ama önce oyun.", "Beni fark ettin mi?", "Kuyruğumla oynayacağım o zaman.",
    "Sanki zaman durdu.", "Bir hareket görsem yeter.", "Miyav, sabrım tükeniyor.",
    "Top olmadan sıkılıyorum.", "Yerimde duramıyorum artık.", "Küçük bir oyun olur mu?",
    "Şurada mı yoksa burada mı top?", "Enerjim boşa gidiyor.", "Hadi ama, bekliyorum!",
    "Patilerimi ısıtmam lazım.", "Boş boş oturmak sıkıcı.", "Bir şeyler yapalım artık.",
    "Miyavlarım cevapsız kalıyor.", "Gözlerimi açık tutmak zor.", "Top nerede, merak ediyorum.",
    "Kuyruğum kendi kendine dans ediyor.", "Biraz eğlence lazım bana.", "Bekleme modundayım.",
    "Şimdi ne yapsam acaba?", "Miyav, oyun oynamak istiyorum.", "Sabrım azalıyor yavaş yavaş.",
    "Fareyi biraz kıpırdat.", "Uzun süredir kımıldamadım.", "Bu kadar durgunluk kediye yakışmaz.",
    "Zıplayacak yer arıyorum.", "Top gelmezse ben giderim.", "Miyav... hâlâ oradayım.",
    "Enerjim taşmak üzere.", "Bir top görsem coşarım.", "Kediliğimi kaybediyorum sanki.",
    "Hareketsizlik bana göre değil.", "Sıkıntıdan esniyorum.", "Patilerim yerinde duramıyor.",
    "Top olmadan hayat sıkıcı.", "Biraz koşuşturma iyi gelir.", "Miyav, canlanmak istiyorum.",
    "Kuyruğum sabırsızlıktan kıvranıyor.", "Bir şeyler oluyor mu acaba?", "Sessizlik beni sıkıyor.",
    "Top nerede kayboldu?", "Uyumadan önce biraz oyun.", "Miyav, hala buradayım unutma.",
    "Kediler hareket sever bilirsin.", "Şu an tam bir bekleyiş içindeyim.", "Fare hareket etmiyor, garip.",
    "Biraz ilgiye ihtiyacım var.", "Top gelirse mutlu olurum.", "Miyavlamaktan boğazım kurudu.",
    "Kuyruğum artık kendi işine bakıyor.", "Durmak bana hiç uymuyor.", "Bir hareket bekliyorum sabırla.",
    "Top nerede kaldı, meraktayım.", "Miyav, biraz eğlenelim mi?", "Patilerimi germem lazım.",
    "Bu sessizlik uzun sürüyor.", "Zıplamak için bahane arıyorum.", "Top ile buluşmak istiyorum.",
    "Miyav, sıkıldığımı söylemiştim.", "Kuyruğum bile sabırsızlanıyor artık.", "Biraz hareket görsem keyfim yerine gelir.",
    "Top gelmezse kendim ararım.", "Miyav, hâlâ bekliyorum burada.", "Şu an içim geçmek üzere.",
    "Bir oyun molası hakkım var.", "Top nerelerde dolaşıyor acaba?", "Miyavlarımı duyan yok mu?",
    "Kediliğim tembelliğe yeniliyor.", "Biraz canlanmam lazım artık.", "Top gelirse gününüz güzel geçer.",
    "Miyav, sabrım test ediyorsun."
]

FORCED_BLINK_FRAMES = 10      # Kedi sıkıldığında gözlerini kaç kare (frame) boyunca kapalı tutsun?
PURR_MIN_DELAY_MS = 7000      # Mırlama sesinin tekrar etmesi için en az beklenecek süre (milisaniye).
PURR_MAX_DELAY_MS = 24000     # Mırlama sesinin tekrar etmesi için en fazla beklenecek süre (milisaniye).


class DesktopPet:
    def __init__(self):
        # Tkinter pencere yapısını kuruyoruz.
        self.root = tk.Tk()
        self.root.overrideredirect(True)          # Pencerenin kapatma butonu ve başlık çubuğunu gizliyoruz.
        self.root.attributes("-topmost", True)     # Kedimizin her zaman diğer pencerelerin üstünde kalmasını sağlıyoruz.
        self.root.attributes("-transparentcolor", TRANSPARENT_KEY) # Belirlediğimiz rengi pencerede tamamen şeffaf yapıyoruz.

        # Ekranın tam genişlik ve yüksekliğini alıp pencereyi tüm ekrana yayıyoruz.
        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()
        self.root.geometry(f"{self.sw}x{self.sh}+0+0")

        # Çizimleri yapacağımız Canvas (tuval) bileşenini oluşturuyoruz.
        self.canvas = tk.Canvas(
            self.root, width=self.sw, height=self.sh,
            bg=TRANSPARENT_KEY, highlightthickness=0
        )
        self.canvas.pack()

        # İlk açılışta top ve kedi ekranın ortasında konumlansın.
        self.ball_x, self.ball_y = self.sw / 2, self.sh / 2
        self.cat_x, self.cat_y = self.sw / 2 - 150, self.sh / 2
        self.direction = 1     # 1: Sağa doğru bakış, -1: Sola doğru bakış.
        
        # Göz kırpma, kuyruk ve ayak animasyonlarının salınım zamanlayıcıları.
        self.blink_timer = random.randint(60, 180)
        self.tail_phase = 0.0
        self.leg_phase = 0.0

        # Kedinin sıkılma (Bored) durumunu takip eden basit bir durum makinesi değişkenleri.
        self.stop_start = None        # Kedinin durmaya başladığı zaman damgası.
        self.bored_triggered = False  # Sıkılma durumu tetiklendi mi?
        self.forced_blink_counter = 0 # Sıkılma anındaki ani göz kırpma sayacı.
        self.bubble_until = 0.0       # Konuşma balonunun ekrandan silineceği zaman.
        self.current_bubble_text = BUBBLE_TEXTS[0]

        # Windows işletim sisteminde tıklama geçirgenliğini aktif ediyoruz.
        if CLICK_THROUGH:
            self.root.after(200, self.make_click_through)

        # Eğer keyboard kütüphanesi yüklüyse acil çıkış kısayollarını bağlıyoruz.
        if HAS_KEYBOARD:
            try:
                keyboard.add_hotkey("ctrl+alt+q", self.root.destroy)
                keyboard.add_hotkey("ctrl+alt+x", self.root.destroy)
            except Exception as e:
                print("Kısayol ayarlanamadı:", e)

        # Mırlama sesi döngüsünü rastgele sürelerle tetikliyoruz.
        if HAS_WINSOUND:
            if not os.path.exists(PURR_SOUND_FILE):
                print(f"Uyarı: '{PURR_SOUND_FILE}' bulunamadı.")
            self.root.after(random.randint(PURR_MIN_DELAY_MS, PURR_MAX_DELAY_MS), self.purr_loop)
        else:
            print("Bilgi: Mirlama sesi özelliği sadece Windows'ta çalışır (winsound).")

        # Ana animasyon döngüsünü ve pencereyi başlatıyoruz.
        self.animate()
        self.root.mainloop()

    def make_click_through(self):
        """
        Windows API'lerini (ctypes) kullanarak pencereyi tıklamalara karşı tamamen geçirgen hale getirir. 
        Böylece kedi ekranda gezinirken arka plandaki klasörlere veya tarayıcıya tıklayabilirsin.
        """
        try:
            import ctypes
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            WS_EX_TRANSPARENT = 0x00000020
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(
                hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED | WS_EX_TRANSPARENT
            )
        except Exception as e:
            print("Click-through ayarlanamadı:", e)

    def purr_loop(self):
        """
        Arka planda ana iş parçacığını (thread) dondurmadan, asenkron (SND_ASYNC) olarak 
        gerçek kedi mırlama sesini çalar ve bir sonraki çalma zamanını rastgele ayarlar.
        """
        try:
            if os.path.exists(PURR_SOUND_FILE):
                winsound.PlaySound(
                    PURR_SOUND_FILE,
                    winsound.SND_FILENAME | winsound.SND_ASYNC
                )
        except Exception as e:
            print("Mırlama sesi çalınamadı:", e)
        finally:
            # Belirlenen rastgele süre bittiğinde bu fonksiyonu tekrar çağırıyoruz.
            self.root.after(random.randint(PURR_MIN_DELAY_MS, PURR_MAX_DELAY_MS), self.purr_loop)

    def draw_ball(self, x, y, r=18):
        """
        Ekranda farenin peşinden koşan 3 boyutlu, gölgeli beyaz topu 
        iç içe geçmiş renk katmanları kullanarak çizer.
        """
        # Önce topun yerdeki hafif siyah gölgesini çiziyoruz.
        self.canvas.create_oval(
            x - r * 0.8, y + r * 0.7, x + r * 0.8, y + r * 1.1,
            fill="#202020", outline=""
        )
        # Topun dış sınır çizgisi.
        self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                 fill="#eeeeee", outline="#b8b8b8", width=1.5)
        # 3B küre efekti vermek için iç içe gradyan halkaları ekliyoruz.
        colors = ["#c9c9c9", "#dcdcdc", "#ebebeb", "#f6f6f6", "#ffffff"]
        n = len(colors)
        for i, c in enumerate(colors):
            shrink = i * (r / n)
            self.canvas.create_oval(
                x - r + shrink * 0.5, y - r + shrink * 0.5,
                x + r - shrink * 0.3, y + r - shrink * 0.3,
                fill=c, outline=""
            )
        # Topun üzerindeki ışık parlama noktası.
        self.canvas.create_oval(
            x - r * 0.45, y - r * 0.65, x - r * 0.05, y - r * 0.25,
            fill="#ffffff", outline=""
        )

    def draw_bubble(self, cx, top_y, text):
        """
        Kedi sıkıldığında kafasının üstünde beliren, köşeleri ovalleştirilmiş 
        estetik konuşma balonunu ve içindeki metni çizer.
        """
        w, h = 220, 62
        x1, y1 = cx - w / 2, top_y - h
        x2, y2 = cx + w / 2, top_y
        r = 16

        # Balonun yuvarlak köşelerini yaylar yardımıyla oluşturuyoruz.
        self.canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, fill="#ffffff", outline="#4a3527", style="pieslice")
        self.canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, fill="#ffffff", outline="#4a3527", style="pieslice")
        self.canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, fill="#ffffff", outline="#4a3527", style="pieslice")
        self.canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, fill="#ffffff", outline="#4a3527", style="pieslice")
        
        # Köşelerin içini kapatmak için düz dikdörtgen dolgular ekliyoruz.
        self.canvas.create_rectangle(x1 + r, y1, x2 - r, y2, fill="#ffffff", outline="")
        self.canvas.create_rectangle(x1, y1 + r, x2, y2 - r, fill="#ffffff", outline="")
        
        # Kenar çizgilerini çekiyoruz.
        self.canvas.create_line(x1 + r, y1, x2 - r, y1, fill="#4a3527", width=1.5)
        self.canvas.create_line(x1 + r, y2, x2 - r, y2, fill="#4a3527", width=1.5)
        self.canvas.create_line(x1, y1 + r, x1, y2 - r, fill="#4a3527", width=1.5)
        self.canvas.create_line(x2, y1 + r, x2, y2 - r, fill="#4a3527", width=1.5)

        # Balonun kedinin kafasını işaret eden küçük üçgen kuyruğu.
        self.canvas.create_polygon(cx - 10, y2 - 2, cx + 10, y2 - 2, cx, y2 + 16, fill="#ffffff", outline="#4a3527")

        # Metni balonun tam ortasına yerleştiriyoruz.
        self.canvas.create_text(cx, (y1 + y2) / 2, text=text, font=("Segoe UI", 10, "bold"),
                                 fill="#4a3527", width=w - 24, justify="center")

    def draw_cat(self, x, y, direction, moving, blink_override=False):
        """
        Chibi tarzında sevimli, turuncu tekir kedimizin tüm vücut hatlarını, 
        kuyruğunu, patilerini ve yüz mimiklerini canvas üzerinde çizen ana görsel fonksiyon.
        """
        d = direction
        # Eğer kedi hareket ediyorsa bacak salınımını, duruyorsa sadece kuyruk salınımını hesaplıyoruz.
        leg_off = math.sin(self.leg_phase) * 4 if moving else 0
        tail_off = math.sin(self.tail_phase) * 22

        # Sevimli kedi renk paletimiz
        BODY = "#ff9d42"       
        BODY_DARK = "#e07a1a"  
        STRIPE = "#c65e00"     
        BELLY = "#fff3df"      
        EAR_IN = "#ffc4d6"     
        PAW = "#fff3df"
        BLUSH = "#ffb3c6"

        # Yerdeki kedi gölgesi
        self.canvas.create_oval(x - 42, y + 40, x + 42, y + 50, fill="#1a1a1a", outline="")

        # Sallanan dinamik kedi kuyruğu (Ucu beyaz detaylı)
        tx = x - d * 38
        self.canvas.create_line(
            tx, y + 8, tx - d * 22, y - 8 + tail_off, tx - d * 38, y - 30 + tail_off * 1.4,
            fill=BODY, width=14, smooth=True, capstyle="round"
        )
        self.canvas.create_oval(tx - d * 42 - 6, y - 34 + tail_off * 1.4, tx - d * 42 + 6, y - 22 + tail_off * 1.4, fill=BELLY, outline="")

        # Arka patilerin çizimi
        self.canvas.create_oval(x - 24 * d - 12, y + 14 - leg_off, x - 2 * d - 12, y + 40 - leg_off, fill=PAW, outline=BODY_DARK, width=1.5)
        self.canvas.create_oval(x + 2 * d - 12, y + 14 + leg_off, x + 24 * d - 12, y + 40 + leg_off, fill=PAW, outline=BODY_DARK, width=1.5)

        # Tombul kedi gövdesi ve üzerindeki tekir çizgileri
        self.canvas.create_oval(x - 42, y - 22, x + 42, y + 32, fill=BODY, outline=BODY_DARK, width=2)
        for i in range(3):
            gx = x - 12 + i * 12
            self.canvas.create_line(gx, y - 18, gx - 4, y - 6, fill=STRIPE, width=2, capstyle="round")
        # Beyaz göğüs lekesi
        self.canvas.create_oval(x - 22, y - 2, x + 22, y + 30, fill=BELLY, outline="")

        # Ön patilerin çizimi
        self.canvas.create_oval(x - 22 * d + 14, y + 6 - leg_off, x - 2 * d + 14, y + 36 - leg_off, fill=PAW, outline=BODY_DARK, width=1.5)
        self.canvas.create_oval(x + 2 * d + 14, y + 6 + leg_off, x + 22 * d + 14, y + 36 + leg_off, fill=PAW, outline=BODY_DARK, width=1.5)

        # Büyük kafa yapısı (Chibi oranı için gövdeye göre geniş tutuldu)
        hx, hy = x + d * 30, y - 34
        HR = 37  
        self.canvas.create_oval(hx - HR, hy - HR + 2, hx + HR, hy + HR + 2, fill=BODY, outline=BODY_DARK, width=2)
        self.canvas.create_oval(hx - 17, hy + 6, hx + 17, hy + HR + 4, fill=BELLY, outline="")

        # Kulaklar ve pembe iç kulak dokusu
        self.canvas.create_polygon(hx - 29 * d, hy - 18, hx - 13 * d, hy - 53, hx + 3 * d, hy - 16, fill=BODY, outline=BODY_DARK, smooth=True)
        self.canvas.create_polygon(hx - 21 * d, hy - 25, hx - 13 * d, hy - 44, hx - 4 * d, hy - 21, fill=EAR_IN, outline="", smooth=True)
        self.canvas.create_polygon(hx + 9 * d, hy - 16, hx + 21 * d, hy - 53, hx + 35 * d, hy - 18, fill=BODY, outline=BODY_DARK, smooth=True)
        self.canvas.create_polygon(hx + 13 * d, hy - 21, hx + 21 * d, hy - 44, hx + 27 * d, hy - 25, fill=EAR_IN, outline="", smooth=True)

        # Alındaki sevimli çizgiler ve yanak allıkları
        for i in range(3):
            self.canvas.create_line(hx - 6 + i * 6 - 3, hy - 32, hx - 10 + i * 6 - 3, hy - 21, fill=STRIPE, width=2, capstyle="round")
        self.canvas.create_oval(hx - 28, hy + 1, hx - 12, hy + 13, fill=BLUSH, outline="")
        self.canvas.create_oval(hx + 12, hy + 1, hx + 28, hy + 13, fill=BLUSH, outline="")

        # Gözlerin kırpılma veya açık olma durumunun yönetimi
        blink = blink_override or (self.blink_timer < 6)
        eye_y = hy - 2
        for ex in (hx - 14 * d, hx + 14 * d):
            if blink:
                # Göz kırpıyorsa sadece ince bir yay (çizgi) gösteriyoruz.
                self.canvas.create_arc(ex - 9, eye_y - 6, ex + 9, eye_y + 6, start=0, extent=180, style="arc", width=2.5, outline="#2a1a10")
            else:
                # Gözler açıksa derinlik katan çift parlama noktalı anime gözü çiziyoruz.
                self.canvas.create_oval(ex - 10, eye_y - 12, ex + 10, eye_y + 12, fill="#3a2a1a", outline="")
                self.canvas.create_oval(ex - 7, eye_y - 9, ex + 7, eye_y + 6, fill="#a86a2a", outline="")
                self.canvas.create_oval(ex - 6, eye_y - 9, ex - 1, eye_y - 2, fill="#ffffff", outline="")
                self.canvas.create_oval(ex + 1, eye_y + 1, ex + 4, eye_y + 4, fill="#ffffff", outline="")

        # Küçük pembe burun ve "w" şeklindeki ağız hattı
        nx = hx + d * 18
        self.canvas.create_polygon(nx - 4, hy + 14, nx + 4, hy + 14, nx, hy + 18, fill="#e8869c", outline="")
        self.canvas.create_line(nx, hy + 18, nx - 5 * d, hy + 22, smooth=True, fill="#4a3527", width=1.5)
        self.canvas.create_line(nx, hy + 18, nx + 3 * d, hy + 21, smooth=True, fill="#4a3527", width=1.5)

        # Beyaz kedi bıyıkları
        for i in range(3):
            yy = hy + 10 + i * 4
            self.canvas.create_line(nx - 2, yy, nx - 34 * d, yy - 5 + i * 3, fill="#ffffff", width=1)
            self.canvas.create_line(nx - 2, yy, nx - 34 * d, yy - 5 + i * 3, fill="#c9c9c9", width=1, dash=(4, 2))

        # Konuşma balonunun tam kafasının üstüne denk gelmesi için üst uç koordinatını döndürüyoruz.
        return hx, hy - HR  

    def animate(self):
        """
        Saniyede 60 kez çalışan, fare konumunu okuyup topu ve kediyi hareket ettiren, 
        sıkılma durumlarını denetleyen ana oyun/animasyon döngüsü.
        """
        self.canvas.delete("all") # Önceki kareden kalan tüm çizimleri temizliyoruz.
        now = time.time()

        # Farenin ekrandaki anlık X ve Y koordinatını alıyoruz.
        mx, my = pyautogui.position()

        # Top farenin konumuna doğru yumuşak bir ivmeyle (asenkron takip) kayıyor.
        self.ball_x += (mx - self.ball_x) * BALL_SPEED
        self.ball_y += (my - self.ball_y) * BALL_SPEED

        # Kedinin topa olan mesafesini ve yönünü hipotenüs formülüyle buluyoruz.
        dx = self.ball_x - self.cat_x
        dy = self.ball_y - self.cat_y
        dist = math.hypot(dx, dy)

        moving = dist > STOP_DISTANCE
        if moving:
            # Eğer kedi topa uzaksa ona doğru koşmaya başlar.
            self.cat_x += dx * CAT_SPEED
            self.cat_y += dy * CAT_SPEED
            if abs(dx) > 2:
                self.direction = 1 if dx > 0 else -1 # Gitmekte olduğu yöne kafasını çevirir.
            self.leg_phase += 0.35
            self.tail_phase += 0.15

            # Kedi hareket ettiği an canlanır; tüm sıkılma sayaçları sıfırlanır.
            self.stop_start = None
            self.bored_triggered = False
            self.forced_blink_counter = 0
            self.bubble_until = 0.0
        else:
            # Kedi topun yanında duruyorsa sadece kuyruğu hafifçe salınır.
            self.tail_phase += 0.06
            if self.stop_start is None:
                self.stop_start = now # Durmaya başladığı anı kaydet.
            elapsed_stopped = now - self.stop_start

            # Belirlenen süreden uzun süre beklerse kedi sıkılır.
            if elapsed_stopped >= BORED_AFTER_SECONDS and not self.bored_triggered:
                self.bored_triggered = True
                self.forced_blink_counter = FORCED_BLINK_FRAMES # Gözlerini şaşkınlıkla kırpar.
                self.bubble_until = now + FORCED_BLINK_FRAMES / FPS + BUBBLE_DURATION
                self.current_bubble_text = random.choice(BUBBLE_TEXTS) # Havuzdan laf seçer.

        # Sıkılınca tetiklenen ani göz kırpma sayacı geri sayımı.
        force_blink_now = self.forced_blink_counter > 0
        if force_blink_now:
            self.forced_blink_counter -= 1

        # Kedinin normal zamandaki doğal, rastgele göz kırpma mekanizması.
        if not force_blink_now:
            self.blink_timer -= 1
            if self.blink_timer < 0:
                self.blink_timer = random.randint(90, 220)

        # Önce topu, ardından topun üzerine basacak şekilde kediyi ekrana çizdiriyoruz.
        self.draw_ball(self.ball_x, self.ball_y)
        head_top_x, head_top_y = self.draw_cat(
            self.cat_x, self.cat_y, self.direction, moving, blink_override=force_blink_now
        )

        # Eğer kedi hala duruyorsa ve konuşma süresi bitmediyse balonu ekranda gösteriyoruz.
        if (not moving) and self.bored_triggered and not force_blink_now and now < self.bubble_until:
            self.draw_bubble(head_top_x, head_top_y - 6, self.current_bubble_text)

        # FPS'e göre (yaklaşık 16.6 ms sonra) bu fonksiyonun yeniden çalışmasını sağlıyoruz.
        self.root.after(int(1000 / FPS), self.animate)


if __name__ == "__main__":
    # Uygulamayı ayağa kaldırıyoruz.
    DesktopPet()