# 🐾 Masaüstü Kedi Top Takip Uygulaması (KediTopTakibi)

Ekranınızda farenizi (daha doğrusu farenizin peşinden koşan 3 boyutlu beyaz bir topu) asenkron olarak takip eden, durduğunda sıkılan, göz kırpan ve konuşma balonlarıyla sizinle etkileşime giren Chibi tarzında sevimli bir masaüstü kedi simülasyonu!

Bu proje, **Python 3.x** ve **Tkinter** framework'ü kullanılarak tamamen yerel kütüphaneler ve matematiksel formüllerle (gelişmiş Canvas çizimleri) geliştirilmiştir.

---

## ✨ Özellikler

* **Dinamik Takip Sistemi:** Beyaz top fare imlecinizi yumuşak bir ivmeyle takip eder; sevimli turuncu tekir kedi ise topa doğru koşar.
* **Chibi Tarzı Vektörel Çizim:** Herhangi bir dış görsel (PNG/JPG) yüklemesine gerek kalmadan tamamen Tkinter Canvas üzerinde katmanlı olarak çizilen animasyonlu kedi gövdesi, kulakları, hareketli bacakları ve kuyruğu.
* **Gelişmiş Durum Makinesi (Sıkılma Modu):** Kedi topun yanında 5 saniyeden fazla hareketsiz kalırsa sıkılır, gözlerini şaşkınlıkla kırpar ve **100 farklı eğlenceli cümle havuzundan** rastgele konuşma balonları çıkarır.
* **Doğal Animasyonlar:** Rastgele zamanlarda devreye giren doğal göz kırpma mekanizması ve hareket yönüne göre asenkron kafa/kuyruk salınımı.
* **Click-Through (Tıklama Geçirgenliği):** Windows API entegrasyonu sayesinde kedi ve top ekrandayken bile arkasında kalan masaüstü simgelerine, klasörlere veya tarayıcı pencerelerine rahatça tıklayabilirsiniz.
* **Asenkron Ses Desteği:** Windows platformunda arka planda ana iş parçacığını (thread) dondurmadan asenkron olarak çalışan rastgele kedi mırlama ses döngüsü.

---

## 🛠️ Teknik Gereksinimler & Kurulum

Projenin çalışması için bilgisayarınızda Python 3.x kurulu olmalıdır. Gerekli harici kütüphaneleri yüklemek için terminalinizde aşağıdaki komutu çalıştırabilirsiniz:

```bash
pip install pyautogui keyboard

```

> 💡 **Not:** `keyboard` ve `winsound` (Windows dahili) kütüphaneleri opsiyoneldir. Sistemde bulunmasalar dahi uygulama çökmez, ilgili özellikleri kapatarak çalışmaya devam eder.

### Dosya Yapısı

Uygulamanın sesli çalışabilmesi için kaynak kodun bulunduğu dizinde şu dosyanın yer alması gerekir:

* `kedi_mirlama.wav` (Uygulama ana dizini veya PyInstaller geçici dizini)

---

## 🚀 Çalıştırma ve Kontroller

Projeyi doğrudan çalıştırmak için:

```bash
python KediTopTakibi.py

```

* **Global Takip:** Fare hareketleri ile topu ve kediyi yönlendirebilirsiniz.
* **Acil Çıkış Kısayolları:** Uygulamayı arka planda tamamen kapatmak için `Ctrl + Alt + Q` veya `Ctrl + Alt + X` kombinasyonlarını kullanabilirsiniz.

---

## 📦 PyInstaller ile EXE Haline Getirme (Derleme)

Projeyi Windows üzerinde tek bir `.exe` dosyası haline getirmek ve ikon, versiyon bilgisi ile ses dosyasını içerisine gömmek için aşağıdaki komutu kullanabilirsiniz:

```bash
pyinstaller --onefile --noconsole --name KediTopTakibi ^
  --icon "KediTopTakibi.ico" ^
  --version-file "version_info.txt" ^
  --add-data "KediMirlama.wav;." ^
  KediTopTakibi.py

```

* `--onefile`: Tüm bağımlılıkları tek bir çalıştırılabilir dosyada toplar.
* `--noconsole`: Arka planda siyah CMD konsol ekranının açılmasını engeller.
* `--add-data`: `kedi_mirlama.wav` dosyasını EXE içerisine gömer ve `sys._MEIPASS` üzerinden dinamik olarak okur.

---

## 📄 Versiyon Bilgisi

* **Ürün Adı:** Masaüstü Kedi Top Takibi
* **Dosya Sürümü / Ürün Sürümü:** 1.0.0.0
* **Telif Hakkı:** © 2026 Abdulkadir Güngör
* **Geliştirici:** Abdulkadir GÜNGÖR
* 📧 E-Posta: a.kadir.gungor.86@gmail.com
* 🌐 Web Sitesi: [abdulkadirgungor.com](https://abdulkadirgungor.com)



---

## 🤝 Emeği Geçenler / Credits

Bu projenin geliştirilmesinde aşağıdaki açık kaynaklı varlıklar ve ses efektleri kullanılmıştır. Katkılarından dolayı içerik üreticilerine teşekkür ederiz:

* **Ses Efektleri:** * `KediMirlama.wav` ses efekti Pixabay üzerinden **Yomecerlm3** tarafından sağlanmıştır. ([Pixabay Profil Bağlantısı](https://pixabay.com/tr/users/yomecerlm3-44330422/))
* **Görseller ve İkonlar:** * `KediTopTakibi.ico` kedi hayvan ikonu Icon-Icons.com üzerinden **kerismaker** tarafından tasarlanmıştır. ([Icon-Icons Yazar Bağlantısı](https://icon-icons.com/authors/750-kerismaker))

---

*Geliştirme Tarihi: 2026-07-08*
