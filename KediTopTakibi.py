
# *******************************************************************************
# * PROJECT NAME        : KediTopTakibi (Desktop Cat & Ball Tracker)
# * DESCRIPTION         : Desktop cat-and-ball tracking application
# * DEVELOPER           : Abdulkadir GUNGOR (a.kadir.gungor.86@gmail.com)
# *                       (Website: https://abdulkadirgungor.com )
# * VERSION             : 2.0.0.0
# * DATE                : 2026-07-12
# * TECH REQUIREMENTS   : Python 3.x / Tkinter framework
# *
# * LIBRARY VERSIONS:
# * 1) pyautogui v0.9.54 (or newer)
# * 2) keyboard v0.13.5 (or newer - optional)
# *
# * SOFTWARE AND HARDWARE:
# * - OS                : Windows, Linux or macOS (sound support is Windows-focused)
# * - Settings folder   : settings/  (lives in the SAME folder as the app/exe)
# *      settings/settings.json        -> all configurable parameters
# *      settings/lang/tr.json,en.json -> languages (new ones can be added)
# *      settings/assets/KediMirlama.wav -> sound file (replaceable)
# *
# * v2.0.0.0 NEW FEATURES:
# * - Full multi-monitor support: the cat and ball now work on WHICHEVER
# *   monitor the mouse is on.
# * - Language support (Turkish / English), read from external JSON files
# *   instead of being hardcoded in the source.
# * - Settings file (settings/settings.json): speed, timing, language and
# *   every other parameter can be changed without touching the source
# *   code or the compiled executable.
# * - ALL Python code lives in a single file (KediTopTakibi.py); only the
# *   "settings" folder (settings/languages/sounds) stays outside the
# *   build, fully editable by the user.
# *
# * CONTROL INTERFACE   : Global tracking via mouse movement
# *******************************************************************************

import tkinter as tk
import math
import random
import sys
import os
import time
import json
import platform
import types

# Import pyautogui so we can read the mouse position and screen coordinates.
try:
    import pyautogui
    # Disable the fail-safe so the app doesn't crash when the mouse hits a screen corner.
    pyautogui.FAILSAFE = False
except ImportError:
    print("ERROR: pyautogui not found. To install: pip install pyautogui")
    sys.exit(1)

# Check for the keyboard library so we can listen for hotkeys (Ctrl+Alt+Q, etc.).
try:
    import keyboard
    HAS_KEYBOARD = True
except ImportError:
    HAS_KEYBOARD = False

# Check for winsound so we can play the purring sound in the background on Windows.
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False


# --- PATH / FILE HELPERS -------------------------------------------------------

def get_app_dir():
    """
    Returns the folder that contains the source file when running as .py,
    or the folder that contains the executable when frozen into a .exe.
    The "settings" folder (settings.json, lang/, assets/) is always looked
    up relative to this folder so the user can edit it freely.
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


APP_DIR = get_app_dir()

# The single external folder the user is free to edit after building the app.
SETTINGS_DIR = os.path.join(APP_DIR, "settings")
SETTINGS_JSON_PATH = os.path.join(SETTINGS_DIR, "settings.json")


# --- DEFAULT (FALLBACK) SETTINGS AND LANGUAGE VALUES ---------------------------
# Last-resort (built-in) values used so the app keeps running without
# crashing even if settings/settings.json or settings/lang/*.json cannot
# be found or read for any reason.

_DEFAULT_SETTINGS = {
    "LANGUAGE": "tr",
    "LANGUAGE_FOLDER": "lang",
    "SOUND_FILE": "assets/KediMirlama.wav",
    "PURR_MIN_DELAY_MS": 7000,
    "PURR_MAX_DELAY_MS": 24000,
    "CLICK_THROUGH": True,
    "TRANSPARENT_KEY": "#010101",
    "FPS": 60,
    "MULTI_MONITOR_SUPPORT": True,
    "CAT_SPEED": 0.06,
    "BALL_SPEED": 0.18,
    "STOP_DISTANCE": 70,
    "BORED_AFTER_SECONDS": 5.0,
    "BUBBLE_DURATION": 4.0,
    "FORCED_BLINK_FRAMES": 10,
}

_DEFAULT_LANG = {
    "meta": {"language_name": "Built-in default", "language_code": "default"},
    "messages": {
        "pyautogui_missing": "ERROR: pyautogui not found.",
        "hotkey_error": "Could not register hotkey: {error}",
        "sound_missing": "Warning: '{path}' not found.",
        "sound_windows_only": "Info: The purring sound feature only works on Windows.",
        "click_through_error": "Could not enable click-through: {error}",
        "purr_error": "Could not play purring sound: {error}",
        "settings_load_error": "Could not load settings file ({path}): {error}",
        "lang_load_error": "Could not load language file ({path}): {error}",
        "multi_monitor_error": "Could not detect multiple monitors: {error}",
        "multi_monitor_active": "Info: Virtual screen is {width}x{height}.",
        "starting": "Starting... (v2.0.0.0)",
    },
    "bubble_texts": [
        "Meow!", "Where's the ball?", "Playtime!", "I'm a bit bored.", "Let's play.",
    ],
}


def load_settings():
    """
    Loads settings/settings.json (from the "settings" folder next to the
    app/exe). If the file is missing or unreadable, falls back to the
    built-in default values (wrapped in a SimpleNamespace for attribute access).
    """
    if os.path.exists(SETTINGS_JSON_PATH):
        try:
            with open(SETTINGS_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Ignore comment/description fields (e.g. keys starting with "_").
            data = {k: v for k, v in data.items() if not k.startswith("_")}
            # Fill in any missing keys with defaults (for forward compatibility).
            for key, value in _DEFAULT_SETTINGS.items():
                data.setdefault(key, value)
            return types.SimpleNamespace(**data)
        except Exception as e:
            print(f"Could not load settings file ({SETTINGS_JSON_PATH}), using default settings: {e}")
    else:
        print(f"Info: '{SETTINGS_JSON_PATH}' not found, using default settings.")
    return types.SimpleNamespace(**_DEFAULT_SETTINGS)


def load_language(settings_module):
    """
    Loads settings/<LANGUAGE_FOLDER>/<code>.json based on the language code
    set in settings/settings.json. Falls back to the built-in default text
    if the file cannot be found or read.
    """
    lang_code = getattr(settings_module, "LANGUAGE", "tr")
    lang_folder = getattr(settings_module, "LANGUAGE_FOLDER", "lang")
    lang_path = os.path.join(SETTINGS_DIR, lang_folder, f"{lang_code}.json")

    if os.path.exists(lang_path):
        try:
            with open(lang_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "messages" not in data:
                data["messages"] = {}
            if "bubble_texts" not in data or not data["bubble_texts"]:
                data["bubble_texts"] = _DEFAULT_LANG["bubble_texts"]
            # Fill in any missing message keys with defaults.
            for key, value in _DEFAULT_LANG["messages"].items():
                data["messages"].setdefault(key, value)
            return data
        except Exception as e:
            print(f"Could not load language file ({lang_path}): {e}")
    else:
        print(f"Info: '{lang_path}' not found, using built-in default text.")
    return _DEFAULT_LANG


# Load settings and language before anything else.
settings = load_settings()
LANG = load_language(settings)


def tr(key, **kwargs):
    """Short helper (translate) that returns text from the active language file."""
    text = LANG.get("messages", {}).get(key) or _DEFAULT_LANG["messages"].get(key, key)
    try:
        return text.format(**kwargs)
    except Exception:
        return text


BUBBLE_TEXTS = LANG.get("bubble_texts") or _DEFAULT_LANG["bubble_texts"]

# Build the full path to the purring sound file.
# SOUND_FILE is relative to the settings folder, e.g. "assets/KediMirlama.wav".
# Users can drop their own .wav file into settings/assets and change the file
# name here to customize the app without recompiling.
PURR_SOUND_FILE = os.path.join(SETTINGS_DIR, getattr(settings, "SOUND_FILE", "assets/KediMirlama.wav"))


class DesktopPet:
    def __init__(self):
        print(tr("starting"))

        # Set up the Tkinter window.
        self.root = tk.Tk()
        self.root.overrideredirect(True)          # Hide the close button and title bar.
        self.root.attributes("-topmost", True)     # Keep the cat always on top of other windows.
        self.root.attributes("-transparentcolor", settings.TRANSPARENT_KEY)  # Make the chosen color fully transparent.

        # --- MULTI-MONITOR SUPPORT -------------------------------------------
        # Compute the top-left corner (vx, vy) and total width/height (sw, sh)
        # of the "virtual screen" spanning all monitors. This lets the window
        # cover more than just the primary monitor, so the cat and ball can
        # follow the mouse no matter which monitor it's on.
        if getattr(settings, "MULTI_MONITOR_SUPPORT", True):
            self.vx, self.vy, self.sw, self.sh = self.get_virtual_screen_metrics()
        else:
            self.vx, self.vy = 0, 0
            self.sw = self.root.winfo_screenwidth()
            self.sh = self.root.winfo_screenheight()

        print(tr("multi_monitor_active", width=self.sw, height=self.sh))

        # Position the window to cover the entire computed virtual screen.
        # Negative offsets (secondary monitors placed left/above) are supported.
        x_part = f"+{self.vx}" if self.vx >= 0 else f"{self.vx}"
        y_part = f"+{self.vy}" if self.vy >= 0 else f"{self.vy}"
        self.root.geometry(f"{self.sw}x{self.sh}{x_part}{y_part}")

        # Create the canvas we'll draw everything on.
        self.canvas = tk.Canvas(
            self.root, width=self.sw, height=self.sh,
            bg=settings.TRANSPARENT_KEY, highlightthickness=0
        )
        self.canvas.pack()

        # On startup, the ball and cat are placed in the center of the virtual
        # screen (i.e. across all monitors). These coordinates are ABSOLUTE
        # screen coordinates, using the same coordinate system as pyautogui.position().
        self.ball_x = self.vx + self.sw / 2
        self.ball_y = self.vy + self.sh / 2
        self.cat_x = self.ball_x - 150
        self.cat_y = self.ball_y
        self.direction = 1     # 1: facing right, -1: facing left.

        # Timers/phases for the blink, tail, and leg animations.
        self.blink_timer = random.randint(60, 180)
        self.tail_phase = 0.0
        self.leg_phase = 0.0

        # Simple state-machine variables tracking the cat's "bored" state.
        self.stop_start = None        # Timestamp when the cat started standing still.
        self.bored_triggered = False  # Has the bored state been triggered?
        self.forced_blink_counter = 0  # Countdown for the surprised blink when bored.
        self.bubble_until = 0.0       # Time when the speech bubble should disappear.
        self.current_bubble_text = BUBBLE_TEXTS[0]

        # Enable click-through on Windows.
        if settings.CLICK_THROUGH:
            self.root.after(200, self.make_click_through)

        # If the keyboard library is available, bind the emergency exit hotkeys.
        if HAS_KEYBOARD:
            try:
                keyboard.add_hotkey("ctrl+alt+q", self.root.destroy)
                keyboard.add_hotkey("ctrl+alt+x", self.root.destroy)
            except Exception as e:
                print(tr("hotkey_error", error=e))

        # Trigger the purring sound loop at random intervals.
        if HAS_WINSOUND:
            if not os.path.exists(PURR_SOUND_FILE):
                print(tr("sound_missing", path=PURR_SOUND_FILE))
            self.root.after(random.randint(settings.PURR_MIN_DELAY_MS, settings.PURR_MAX_DELAY_MS), self.purr_loop)
        else:
            print(tr("sound_windows_only"))

        # Start the main animation loop and the window's event loop.
        self.animate()
        self.root.mainloop()

    def get_virtual_screen_metrics(self):
        """
        Returns the top-left corner (vx, vy) and total size (width, height)
        of the virtual screen spanning ALL monitors on the system. Uses the
        native Windows API (ctypes) on Windows, and the optional
        'screeninfo' library on other systems if available. If neither is
        possible, falls back to the primary monitor only (legacy behavior).
        """
        system = platform.system()

        if system == "Windows":
            try:
                import ctypes
                user32 = ctypes.windll.user32
                try:
                    # Prevents incorrect (too small) measurements on high-DPI screens.
                    user32.SetProcessDPIAware()
                except Exception:
                    pass

                SM_XVIRTUALSCREEN = 76
                SM_YVIRTUALSCREEN = 77
                SM_CXVIRTUALSCREEN = 78
                SM_CYVIRTUALSCREEN = 79

                vx = user32.GetSystemMetrics(SM_XVIRTUALSCREEN)
                vy = user32.GetSystemMetrics(SM_YVIRTUALSCREEN)
                vw = user32.GetSystemMetrics(SM_CXVIRTUALSCREEN)
                vh = user32.GetSystemMetrics(SM_CYVIRTUALSCREEN)

                if vw > 0 and vh > 0:
                    return vx, vy, vw, vh
            except Exception as e:
                print(tr("multi_monitor_error", error=e))
        else:
            # Linux/macOS: if the optional 'screeninfo' library is available,
            # compute the combined bounding box of all monitors.
            try:
                from screeninfo import get_monitors
                monitors = get_monitors()
                if monitors:
                    min_x = min(m.x for m in monitors)
                    min_y = min(m.y for m in monitors)
                    max_x = max(m.x + m.width for m in monitors)
                    max_y = max(m.y + m.height for m in monitors)
                    return min_x, min_y, (max_x - min_x), (max_y - min_y)
            except Exception:
                pass  # screeninfo not installed or info unavailable; fall back below.

        # Fallback: primary monitor only (legacy behavior).
        return 0, 0, self.root.winfo_screenwidth(), self.root.winfo_screenheight()

    def make_click_through(self):
        """
        Uses the Windows API (ctypes) to make the window fully click-through.
        This lets you click on desktop icons or windows underneath the cat
        while it's roaming the screen.
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
            print(tr("click_through_error", error=e))

    def purr_loop(self):
        """
        Plays the actual cat purring sound asynchronously (SND_ASYNC) without
        blocking the main thread, then schedules the next playback at a
        random interval.
        """
        try:
            if os.path.exists(PURR_SOUND_FILE):
                winsound.PlaySound(
                    PURR_SOUND_FILE,
                    winsound.SND_FILENAME | winsound.SND_ASYNC
                )
        except Exception as e:
            print(tr("purr_error", error=e))
        finally:
            # Schedule this function to run again after a random delay.
            self.root.after(random.randint(settings.PURR_MIN_DELAY_MS, settings.PURR_MAX_DELAY_MS), self.purr_loop)

    def draw_ball(self, x, y, r=18):
        """
        Draws the 3D-looking, shaded white ball that chases the mouse,
        using nested color layers. (x, y) are CANVAS-LOCAL (i.e. in-window) coordinates.
        """
        # First draw the ball's soft black shadow on the ground.
        self.canvas.create_oval(
            x - r * 0.8, y + r * 0.7, x + r * 0.8, y + r * 1.1,
            fill="#202020", outline=""
        )
        # The ball's outer outline.
        self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                 fill="#eeeeee", outline="#b8b8b8", width=1.5)
        # Add nested gradient rings for a 3D sphere effect.
        colors = ["#c9c9c9", "#dcdcdc", "#ebebeb", "#f6f6f6", "#ffffff"]
        n = len(colors)
        for i, c in enumerate(colors):
            shrink = i * (r / n)
            self.canvas.create_oval(
                x - r + shrink * 0.5, y - r + shrink * 0.5,
                x + r - shrink * 0.3, y + r - shrink * 0.3,
                fill=c, outline=""
            )
        # The highlight/shine spot on the ball.
        self.canvas.create_oval(
            x - r * 0.45, y - r * 0.65, x - r * 0.05, y - r * 0.25,
            fill="#ffffff", outline=""
        )

    def draw_bubble(self, cx, top_y, text):
        """
        Draws the rounded-corner speech bubble and its text that appears
        above the cat's head when it gets bored.
        """
        w, h = 220, 62
        x1, y1 = cx - w / 2, top_y - h
        x2, y2 = cx + w / 2, top_y
        r = 16

        # Build the bubble's rounded corners using arcs.
        self.canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, fill="#ffffff", outline="#4a3527", style="pieslice")
        self.canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, fill="#ffffff", outline="#4a3527", style="pieslice")
        self.canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, fill="#ffffff", outline="#4a3527", style="pieslice")
        self.canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, fill="#ffffff", outline="#4a3527", style="pieslice")

        # Fill the corners in with plain rectangles.
        self.canvas.create_rectangle(x1 + r, y1, x2 - r, y2, fill="#ffffff", outline="")
        self.canvas.create_rectangle(x1, y1 + r, x2, y2 - r, fill="#ffffff", outline="")

        # Draw the border lines.
        self.canvas.create_line(x1 + r, y1, x2 - r, y1, fill="#4a3527", width=1.5)
        self.canvas.create_line(x1 + r, y2, x2 - r, y2, fill="#4a3527", width=1.5)
        self.canvas.create_line(x1, y1 + r, x1, y2 - r, fill="#4a3527", width=1.5)
        self.canvas.create_line(x2, y1 + r, x2, y2 - r, fill="#4a3527", width=1.5)

        # The small triangular tail pointing at the cat's head.
        self.canvas.create_polygon(cx - 10, y2 - 2, cx + 10, y2 - 2, cx, y2 + 16, fill="#ffffff", outline="#4a3527")

        # Place the text right in the middle of the bubble.
        self.canvas.create_text(cx, (y1 + y2) / 2, text=text, font=("Segoe UI", 10, "bold"),
                                 fill="#4a3527", width=w - 24, justify="center")

    def draw_cat(self, x, y, direction, moving, blink_override=False):
        """
        Draws the cute, chibi-style orange tabby cat's entire body outline,
        tail, paws and facial expressions on the canvas.
        (x, y) are CANVAS-LOCAL (i.e. in-window) coordinates.
        """
        d = direction
        # If the cat is moving, compute the leg-swing offset; otherwise only the tail sways.
        leg_off = math.sin(self.leg_phase) * 4 if moving else 0
        tail_off = math.sin(self.tail_phase) * 22

        # Our cute cat color palette.
        BODY = "#ff9d42"
        BODY_DARK = "#e07a1a"
        STRIPE = "#c65e00"
        BELLY = "#fff3df"
        EAR_IN = "#ffc4d6"
        PAW = "#fff3df"
        BLUSH = "#ffb3c6"

        # The cat's shadow on the ground.
        self.canvas.create_oval(x - 42, y + 40, x + 42, y + 50, fill="#1a1a1a", outline="")

        # The swaying, dynamic cat tail (with a white-tipped detail).
        tx = x - d * 38
        self.canvas.create_line(
            tx, y + 8, tx - d * 22, y - 8 + tail_off, tx - d * 38, y - 30 + tail_off * 1.4,
            fill=BODY, width=14, smooth=True, capstyle="round"
        )
        self.canvas.create_oval(tx - d * 42 - 6, y - 34 + tail_off * 1.4, tx - d * 42 + 6, y - 22 + tail_off * 1.4, fill=BELLY, outline="")

        # Draw the hind paws.
        self.canvas.create_oval(x - 24 * d - 12, y + 14 - leg_off, x - 2 * d - 12, y + 40 - leg_off, fill=PAW, outline=BODY_DARK, width=1.5)
        self.canvas.create_oval(x + 2 * d - 12, y + 14 + leg_off, x + 24 * d - 12, y + 40 + leg_off, fill=PAW, outline=BODY_DARK, width=1.5)

        # The chubby cat body and its tabby stripes.
        self.canvas.create_oval(x - 42, y - 22, x + 42, y + 32, fill=BODY, outline=BODY_DARK, width=2)
        for i in range(3):
            gx = x - 12 + i * 12
            self.canvas.create_line(gx, y - 18, gx - 4, y - 6, fill=STRIPE, width=2, capstyle="round")
        # The white chest patch.
        self.canvas.create_oval(x - 22, y - 2, x + 22, y + 30, fill=BELLY, outline="")

        # Draw the front paws.
        self.canvas.create_oval(x - 22 * d + 14, y + 6 - leg_off, x - 2 * d + 14, y + 36 - leg_off, fill=PAW, outline=BODY_DARK, width=1.5)
        self.canvas.create_oval(x + 2 * d + 14, y + 6 + leg_off, x + 22 * d + 14, y + 36 + leg_off, fill=PAW, outline=BODY_DARK, width=1.5)

        # The large head (kept wide relative to the body for the chibi proportions).
        hx, hy = x + d * 30, y - 34
        HR = 37
        self.canvas.create_oval(hx - HR, hy - HR + 2, hx + HR, hy + HR + 2, fill=BODY, outline=BODY_DARK, width=2)
        self.canvas.create_oval(hx - 17, hy + 6, hx + 17, hy + HR + 4, fill=BELLY, outline="")

        # The ears and their pink inner texture.
        self.canvas.create_polygon(hx - 29 * d, hy - 18, hx - 13 * d, hy - 53, hx + 3 * d, hy - 16, fill=BODY, outline=BODY_DARK, smooth=True)
        self.canvas.create_polygon(hx - 21 * d, hy - 25, hx - 13 * d, hy - 44, hx - 4 * d, hy - 21, fill=EAR_IN, outline="", smooth=True)
        self.canvas.create_polygon(hx + 9 * d, hy - 16, hx + 21 * d, hy - 53, hx + 35 * d, hy - 18, fill=BODY, outline=BODY_DARK, smooth=True)
        self.canvas.create_polygon(hx + 13 * d, hy - 21, hx + 21 * d, hy - 44, hx + 27 * d, hy - 25, fill=EAR_IN, outline="", smooth=True)

        # The cute forehead stripes and blush marks.
        for i in range(3):
            self.canvas.create_line(hx - 6 + i * 6 - 3, hy - 32, hx - 10 + i * 6 - 3, hy - 21, fill=STRIPE, width=2, capstyle="round")
        self.canvas.create_oval(hx - 28, hy + 1, hx - 12, hy + 13, fill=BLUSH, outline="")
        self.canvas.create_oval(hx + 12, hy + 1, hx + 28, hy + 13, fill=BLUSH, outline="")

        # Handle whether the eyes are blinking or open.
        blink = blink_override or (self.blink_timer < 6)
        eye_y = hy - 2
        for ex in (hx - 14 * d, hx + 14 * d):
            if blink:
                # If blinking, show only a thin arc (line).
                self.canvas.create_arc(ex - 9, eye_y - 6, ex + 9, eye_y + 6, start=0, extent=180, style="arc", width=2.5, outline="#2a1a10")
            else:
                # If open, draw an anime-style eye with double highlight dots for depth.
                self.canvas.create_oval(ex - 10, eye_y - 12, ex + 10, eye_y + 12, fill="#3a2a1a", outline="")
                self.canvas.create_oval(ex - 7, eye_y - 9, ex + 7, eye_y + 6, fill="#a86a2a", outline="")
                self.canvas.create_oval(ex - 6, eye_y - 9, ex - 1, eye_y - 2, fill="#ffffff", outline="")
                self.canvas.create_oval(ex + 1, eye_y + 1, ex + 4, eye_y + 4, fill="#ffffff", outline="")

        # The small pink nose and the "w"-shaped mouth line.
        nx = hx + d * 18
        self.canvas.create_polygon(nx - 4, hy + 14, nx + 4, hy + 14, nx, hy + 18, fill="#e8869c", outline="")
        self.canvas.create_line(nx, hy + 18, nx - 5 * d, hy + 22, smooth=True, fill="#4a3527", width=1.5)
        self.canvas.create_line(nx, hy + 18, nx + 3 * d, hy + 21, smooth=True, fill="#4a3527", width=1.5)

        # The white cat whiskers.
        for i in range(3):
            yy = hy + 10 + i * 4
            self.canvas.create_line(nx - 2, yy, nx - 34 * d, yy - 5 + i * 3, fill="#ffffff", width=1)
            self.canvas.create_line(nx - 2, yy, nx - 34 * d, yy - 5 + i * 3, fill="#c9c9c9", width=1, dash=(4, 2))

        # Return the top of the head so the speech bubble can be positioned above it.
        return hx, hy - HR

    def animate(self):
        """
        The main game/animation loop, running FPS times per second, reading
        the mouse position and moving the ball and cat, and handling the
        boredom state.
        """
        self.canvas.delete("all")  # Clear everything drawn in the previous frame.
        now = time.time()

        # Get the current ABSOLUTE X and Y mouse position across the ENTIRE
        # virtual screen (i.e. including all monitors). pyautogui returns
        # these coordinates using the same virtual-screen system as Windows
        # (primary monitor top-left = 0,0; monitors to the left/above are negative).
        mx, my = pyautogui.position()

        # The ball glides toward the mouse position with smooth easing (async tracking).
        self.ball_x += (mx - self.ball_x) * settings.BALL_SPEED
        self.ball_y += (my - self.ball_y) * settings.BALL_SPEED

        # Find the cat's distance and direction to the ball using the hypotenuse formula.
        dx = self.ball_x - self.cat_x
        dy = self.ball_y - self.cat_y
        dist = math.hypot(dx, dy)

        moving = dist > settings.STOP_DISTANCE
        if moving:
            # If the cat is far from the ball, it starts running toward it.
            self.cat_x += dx * settings.CAT_SPEED
            self.cat_y += dy * settings.CAT_SPEED
            if abs(dx) > 2:
                self.direction = 1 if dx > 0 else -1  # Turn its head toward the direction it's moving.
            self.leg_phase += 0.35
            self.tail_phase += 0.15

            # The moment the cat moves, it "wakes up"; all boredom counters reset.
            self.stop_start = None
            self.bored_triggered = False
            self.forced_blink_counter = 0
            self.bubble_until = 0.0
        else:
            # If the cat is standing next to the ball, only the tail sways gently.
            self.tail_phase += 0.06
            if self.stop_start is None:
                self.stop_start = now  # Record the moment it started standing still.
            elapsed_stopped = now - self.stop_start

            # If it's been waiting longer than the configured time, it gets bored.
            if elapsed_stopped >= settings.BORED_AFTER_SECONDS and not self.bored_triggered:
                self.bored_triggered = True
                self.forced_blink_counter = settings.FORCED_BLINK_FRAMES  # Blinks in surprise.
                self.bubble_until = now + settings.FORCED_BLINK_FRAMES / settings.FPS + settings.BUBBLE_DURATION
                self.current_bubble_text = random.choice(BUBBLE_TEXTS)  # Pick a line from the pool.

        # Countdown for the forced blink triggered by boredom.
        force_blink_now = self.forced_blink_counter > 0
        if force_blink_now:
            self.forced_blink_counter -= 1

        # The cat's normal, natural random-blink mechanism.
        if not force_blink_now:
            self.blink_timer -= 1
            if self.blink_timer < 0:
                self.blink_timer = random.randint(90, 220)

        # Convert the ABSOLUTE coordinates into canvas-local coordinates
        # relative to the window's (virtual screen's) top-left corner. This
        # way, the cat and ball are drawn at the correct pixel even on a
        # secondary monitor.
        ball_cx, ball_cy = self.ball_x - self.vx, self.ball_y - self.vy
        cat_cx, cat_cy = self.cat_x - self.vx, self.cat_y - self.vy

        # Draw the ball first, then the cat on top of it.
        self.draw_ball(ball_cx, ball_cy)
        head_top_x, head_top_y = self.draw_cat(
            cat_cx, cat_cy, self.direction, moving, blink_override=force_blink_now
        )

        # If the cat is still standing still and the speech duration hasn't ended, show the bubble.
        if (not moving) and self.bored_triggered and not force_blink_now and now < self.bubble_until:
            self.draw_bubble(head_top_x, head_top_y - 6, self.current_bubble_text)

        # Schedule this function to run again based on FPS (roughly every 16.6 ms).
        self.root.after(int(1000 / settings.FPS), self.animate)


if __name__ == "__main__":
    # Launch the application.
    DesktopPet()
