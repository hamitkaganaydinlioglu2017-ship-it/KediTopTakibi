# 🐾 KediTopTakibi (Desktop Cat & Ball Tracker)

🇹🇷 Türkçe | 🇬🇧 English — *bu belge her iki dili de içerir / this document contains both languages*

Farenizi (daha doğrusu farenin peşinden koşan 3 boyutlu beyaz bir topu) asenkron olarak takip eden, durduğunda sıkılan, göz kırpan ve konuşma balonlarıyla sizinle etkileşime giren Chibi tarzında sevimli bir masaüstü kedi simülasyonu.
*A cute Chibi-style desktop cat simulation that asynchronously chases your mouse cursor (or rather, a 3D white ball that chases your cursor), gets bored when it stops, blinks, and interacts with you through speech bubbles.*

Proje tamamen **Python 3.x** ve **Tkinter** ile, dış görsel dosyası kullanılmadan (gelişmiş Canvas çizimleriyle) geliştirilmiştir.
*Built entirely with **Python 3.x** and **Tkinter**, using only native libraries and mathematical formulas (advanced Canvas drawing) — no external image assets.*

---

## 💾 İndirme / Downloads

| Sürüm / Version | Açıklama / Description | Bağlantı / Link |
|---|---|---|
| **v2.0.0.0** (Güncel / Latest) | Derlenmiş Windows sürümü — çoklu monitör, dil ve ayar dosyası desteği içerir. *Compiled Windows build — includes multi-monitor, language and settings-file support.* (`.zip`, `settings/` klasörüyle birlikte / with the `settings/` folder) | [KediTopTakibi.zip](https://github.com/abdulkadirgungor86/KediTopTakibi/releases/download/v2.0.0.0/KediTopTakibi.zip) |
| **v1.0.0.0** (İlk Sürüm / Initial Release) | Tek dosya `.exe`, yalnızca birincil monitör desteği. *Single-file `.exe`, primary monitor only.* | [KediTopTakibi.exe](https://github.com/abdulkadirgungor86/KediTopTakibi/releases/download/v1.0.0.0/KediTopTakibi.exe) |

Tüm sürümler için: [GitHub Releases sayfası](https://github.com/abdulkadirgungor86/KediTopTakibi/releases) · Kaynak kod / Source code: [github.com/abdulkadirgungor86/KediTopTakibi](https://github.com/abdulkadirgungor86/KediTopTakibi)

> ⚠️ v2.0.0.0'ı çalıştırmak için indirdiğiniz `.zip` içindeki **`settings/` klasörünü `.exe` ile aynı dizinde tutmanız gerekir** — uygulama başlarken ayarları ve dili bu klasörden okur.
> *To run v2.0.0.0, keep the **`settings/` folder in the same directory as the `.exe`** — the app reads its configuration and language from this folder at startup.*

---

## 🆕 v2.0.0.0 Yenilikleri / What's New in v2.0.0.0

* **🖥️ Tam Çoklu Monitör Desteği / Full Multi-Monitor Support**
  TR: v1.0.0.0'daki en büyük eksiklik giderildi. Kedi ve top artık sadece birincil monitörde değil, sisteme bağlı **tüm monitörlerde** çalışır; fareniz hangi ekrana geçerse geçsin kesintisiz takip eder.
  EN: The biggest limitation of v1.0.0.0 is fixed. The cat and ball now work across **every monitor** connected to your system, not just the primary one — move your mouse to any screen and they follow it seamlessly.

* **🌍 Çoklu Dil Desteği / Multi-Language Support**
  TR: Uygulama **varsayılan olarak Türkçe** açılır. Aktif dil `settings/settings.json` içindeki `LANGUAGE` alanından okunur ve metinler kaynak koddan tamamen bağımsız `settings/lang/tr.json` / `settings/lang/en.json` dosyalarından yüklenir.
  EN: The app **defaults to Turkish** on launch. The active language is read from the `LANGUAGE` field in `settings/settings.json`, and text is loaded from `settings/lang/tr.json` / `settings/lang/en.json`, completely decoupled from the source code.

  **İngilizceye geçmek için / To switch to English:**
  `settings/settings.json` içinde `"LANGUAGE": "tr"` satırını `"LANGUAGE": "en"` olarak değiştirip uygulamayı yeniden başlatın.
  *Change the `"LANGUAGE": "tr"` line in `settings/settings.json` to `"LANGUAGE": "en"` and restart the app.*

  **Başka bir dil eklemek için / To add another language:**
  `settings/lang/` klasörüne örneğin `de.json` adında yeni bir dosya ekleyip (`tr.json`/`en.json` ile aynı `messages` ve `bubble_texts` yapısında) `settings.json` içinde `"LANGUAGE": "de"` yazmanız yeterlidir — kaynak kodda hiçbir değişiklik gerekmez.
  *Drop a new file such as `de.json` into `settings/lang/` (following the same `messages` and `bubble_texts` structure as `tr.json`/`en.json`) and set `"LANGUAGE": "de"` in `settings.json` — no source code changes needed.*

* **⚙️ Ayrı Ayarlar Dosyası / Dedicated Settings File (`settings/settings.json`)**
  TR: Mırlama süresi, hız, sıkılma zamanlaması, aktif dil ve daha fazlası kaynak koda dokunmadan bu dosyadan değiştirilebilir.
  EN: Purring duration, speed, boredom timing, the active language, and more can be changed from this file without touching the source code.

* **📦 Kullanıcı Tarafından Özelleştirilebilir Dosyalar / User-Customizable Files**
  TR: `settings/` klasörü hem `.py` olarak çalıştırırken hem de derlenmiş `.exe` yanına konduğunda okunur; yani derlenmiş sürümde bile **yeniden derlemeye gerek kalmadan** dil veya ayar değiştirilebilir.
  EN: The `settings/` folder is read both when running as `.py` and when placed next to a compiled `.exe`, meaning you can change the language or settings of a compiled build **without recompiling**.

---

## ✨ Genel Özellikler / General Features

* **Dinamik Takip / Dynamic Tracking:** Beyaz top fareyi yumuşak bir ivmeyle takip eder, kedi ise topu kovalar. *The white ball follows your cursor with smooth easing; the cat then chases the ball.*
* **Chibi Tarzı Vektörel Çizim / Chibi-Style Vector Drawing:** Kedi tamamen Tkinter Canvas üzerinde katmanlı çizilir, dış görsel dosyası kullanılmaz. *The animated cat is drawn entirely in layers on the Canvas — no external image assets required.*
* **Sıkılma Modu / Boredom Mode:** Kedi topun yanında birkaç saniye hareketsiz kalırsa sıkılır, göz kırpar ve **100 farklı cümleden** oluşan havuzdan rastgele konuşma balonu gösterir (TR ve EN). *If the cat stays still next to the ball, it gets bored, blinks, and shows a random line from a **pool of 100** (available in both languages).*
* **Doğal Animasyonlar / Natural Animations:** Rastgele göz kırpma, harekete bağlı asenkron kafa/kuyruk salınımı. *Randomly-timed blinking, plus asynchronous head/tail sway based on movement.*
* **Click-Through:** Windows API sayesinde kedi ve topun arkasındaki simge/pencerelere tıklanabilir. *Thanks to Windows API integration, you can click through the cat and ball onto whatever is behind them.*
* **Asenkron Ses / Asynchronous Sound:** Windows'ta ana iş parçacığını dondurmadan rastgele mırlama sesi çalar. *A randomly-timed purring loop that plays asynchronously on Windows without freezing the main thread.*

---

## 🛠️ Gereksinimler & Kurulum / Requirements & Installation

Python 3.x gereklidir. Gerekli kütüphaneler:
*Python 3.x is required. Install the required libraries with:*

```bash
pip install pyautogui keyboard
```

> 💡 `keyboard` ve `winsound` (Windows dahili) opsiyoneldir; yoklarsa uygulama çökmez, ilgili özellik kapanır.
> *`keyboard` and `winsound` (built into Windows) are optional — the app won't crash if they're missing, it simply disables the related feature.*
>
> 💡 Windows dışı sistemlerde tüm monitörlerin otomatik algılanması için isteğe bağlı `pip install screeninfo` kurabilirsiniz; kurulu değilse yalnızca birincil monitör kullanılır.
> *On non-Windows systems, optionally install `pip install screeninfo` to auto-detect all monitors; without it, the app falls back to the primary monitor only.*

### 📁 Klasör Yapısı / File Structure

```
KediTopTakibi/
├── KediTopTakibi.py         # Ana uygulama kodu / Main application code
├── version_info.txt         # PyInstaller sürüm bilgisi / PyInstaller version info
├── CREDITS.txt               # Katkı/telif bilgileri / Credits & attributions
└── settings/                 # Kullanıcı tarafından düzenlenebilir / User-editable
    ├── settings.json          # Tüm ayarlar (hız, süre, dil vb.) / All settings (speed, timing, language, etc.)
    ├── lang/
    │   ├── tr.json              # Türkçe metinler (varsayılan) / Turkish text (default)
    │   └── en.json              # İngilizce metinler / English text
    └── assets/
        └── KediMirlama.wav      # Mırlama ses dosyası / Purring sound file
```

> 📌 `settings/` klasörü uygulamanın her başlangıcında yeniden okunur; `.exe` ile **aynı dizinde** olmalıdır.
> *The `settings/` folder is re-read every time the app starts and must live in the **same directory** as the `.exe`.*

---

## ⚙️ Ayarlar Dosyası / Settings File (`settings/settings.json`)

| Değişken / Variable | Açıklama / Description | Varsayılan / Default |
|---|---|---|
| `LANGUAGE` | Aktif dil kodu / Active language code (`"tr"` veya/or `"en"`) | `"tr"` |
| `LANGUAGE_FOLDER` | Dil dosyalarının klasörü / Folder containing language files | `"lang"` |
| `SOUND_FILE` | Mırlama ses dosyası yolu (settings klasörüne göre) / Purring sound path (relative to `settings/`) | `"assets/KediMirlama.wav"` |
| `PURR_MIN_DELAY_MS` / `PURR_MAX_DELAY_MS` | Mırlama sesleri arası gecikme aralığı (ms) / Delay range between purring sounds (ms) | `7000` / `24000` |
| `CLICK_THROUGH` | Tıklama geçirgenliği açık/kapalı / Toggle click-through | `true` |
| `TRANSPARENT_KEY` | Şeffaflık için kullanılan renk anahtarı / Color key used for transparency | `"#010101"` |
| `FPS` | Saniyedeki kare sayısı / Frames per second | `60` |
| `MULTI_MONITOR_SUPPORT` | Çoklu monitör desteği açık/kapalı / Toggle multi-monitor support | `true` |
| `CAT_SPEED` / `BALL_SPEED` | Kedi ve topun hareket hassasiyeti / Movement sensitivity | `0.06` / `0.18` |
| `STOP_DISTANCE` | Kedinin topa yaklaşınca durma mesafesi / Distance at which the cat stops near the ball | `70` |
| `BORED_AFTER_SECONDS` | Sıkılmaya başlama süresi (sn) / Time before boredom kicks in (sec) | `5.0` |
| `BUBBLE_DURATION` | Konuşma balonunun ekranda kalma süresi (sn) / Speech bubble display duration (sec) | `4.0` |
| `FORCED_BLINK_FRAMES` | Sıkılma anındaki göz kırpma kare sayısı / Blink frame count when bored | `10` |

Değerleri değiştirmek için `settings.json` dosyasını herhangi bir metin editörüyle açıp düzenlemeniz ve uygulamayı yeniden başlatmanız yeterlidir.
*Just open `settings.json` in any text editor, edit the values, and restart the app.*

## 🌍 Dil Dosyaları / Language Files (`settings/lang/`)

TR: Dil dosyaları düz JSON'dır; `messages` (uygulama içi bilgi/uyarı metinleri) ve `bubble_texts` (kedinin sıkılınca söylediği 100 rastgele cümle) bölümlerinden oluşur.
EN: Language files are plain JSON, made up of `messages` (in-app info/warning text) and `bubble_texts` (the 100 random lines the cat says when bored).

Uygulama **varsayılan olarak Türkçe** (`tr.json`) ile açılır; İngilizceye geçmek için `settings.json` içindeki `LANGUAGE` değerini `"en"` yapmanız yeterlidir — hazır `en.json` dosyası zaten pakette bulunur. Yeni bir dil eklemek isterseniz `lang/` klasörüne aynı yapıda bir JSON dosyası (örn. `de.json`) ekleyip `LANGUAGE` değerini o dile göre ayarlamanız yeterlidir.
*The app **defaults to Turkish** (`tr.json`). To switch to English, just set `LANGUAGE` to `"en"` in `settings.json` — the `en.json` file already ships in the package. To add a new language, drop a JSON file with the same structure (e.g. `de.json`) into `lang/` and set `LANGUAGE` accordingly.*

---

## 🚀 Çalıştırma ve Kontroller / Running & Controls

Projeyi doğrudan çalıştırmak için / To run the project directly:

```bash
python KediTopTakibi.py
```

* **Global Takip / Global Tracking:** Fareniz topu ve kediyi yönlendirir — artık **tüm monitörlerde**. *Your mouse movements drive the ball and cat — now across **every monitor**.*
* **Acil Çıkış / Emergency Exit:** `Ctrl + Alt + Q` veya `Ctrl + Alt + X` ile arka planda çalışan uygulamayı tamamen kapatabilirsiniz. *Use `Ctrl + Alt + Q` or `Ctrl + Alt + X` to fully close the app running in the background.*

---

## 📦 PyInstaller ile EXE Oluşturma / Building an EXE with PyInstaller

```bash
pyinstaller --onefile --noconsole --name KediTopTakibi ^
  --icon "KediTopTakibi.ico" ^
  --version-file "version_info.txt" ^
  KediTopTakibi.py
```

TR: `settings/` klasörü (settings.json, lang/, assets/) EXE içine **gömülmez** — derleme sonrasında `settings/` klasörünü elle `.exe` ile aynı dizine kopyalamanız gerekir. Bu sayede kullanıcılar `.exe`'yi yeniden derlemeden dili veya ayarları değiştirebilir.
EN: The `settings/` folder (settings.json, lang/, assets/) is **not embedded** into the EXE — after building, manually copy the `settings/` folder next to the `.exe`. This lets users change the language or settings without recompiling.

---

## 📄 Versiyon Bilgisi / Version Information

* **Ürün Adı / Product Name:** Masaüstü Kedi Top Takibi / Desktop Cat & Ball Tracker
* **Sürüm / Version:** 2.0.0.0
* **Telif Hakkı / Copyright:** © 2026 Abdulkadir Güngör
* **Geliştirici / Developer:** Abdulkadir GÜNGÖR
* 📧 E-posta / Email: a.kadir.gungor.86@gmail.com
* 🌐 Web Sitesi / Website: [abdulkadirgungor.com](https://abdulkadirgungor.com)

---

## 🤝 Emeği Geçenler / Credits

* **Ses Efektleri / Sound Effects:** `KediMirlama.wav` — **Yomecerlm3** via Pixabay. ([Pixabay Profili / Profile](https://pixabay.com/tr/users/yomecerlm3-44330422/))
* **Görseller ve İkonlar / Graphics & Icons:** `KediTopTakibi.ico` — **kerismaker** via Icon-Icons.com. ([Icon-Icons Yazar / Author](https://icon-icons.com/authors/750-kerismaker))

Daha fazla ayrıntı için / For more details, see [CREDITS.txt](CREDITS.txt).

---

*Geliştirme Tarihi / Development Date: 2026-07-08 · Son Güncelleme / Last Updated (v2.0.0.0): 2026-07-12*
