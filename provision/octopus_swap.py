import logging
from pwnagotchi.plugins import Plugin
from PIL import Image

# -------------------------------
# Where to draw the composite image
# -------------------------------
IMG_X = 4
IMG_Y = 34
IMG_W = 118
IMG_H = 68

# -------------------------------
# Image paths
# -------------------------------
IMG_DIR = "/usr/local/share/pwnagotchi/custom-assets/faces/octopus_images"

IMAGE_PATHS = {
    "look_r": f"{IMG_DIR}/octopus_look_r.png",
    "look_l": f"{IMG_DIR}/octopus_look_l.png",
    "look_r_happy": f"{IMG_DIR}/octopus_look_r_happy.png",
    "look_l_happy": f"{IMG_DIR}/octopus_look_l_happy.png",
    "sleep": f"{IMG_DIR}/octopus_sleep.png",
    "awake": f"{IMG_DIR}/octopus_awake.png",
    "bored": f"{IMG_DIR}/octopus_bored.png",
    "intense": f"{IMG_DIR}/octopus_intense.png",
    "cool": f"{IMG_DIR}/octopus_cool.png",
    "happy": f"{IMG_DIR}/octopus_happy.png",
    "excited": f"{IMG_DIR}/octopus_excited.png",
    "grateful": f"{IMG_DIR}/octopus_grateful.png",
    "motivated": f"{IMG_DIR}/octopus_motivated.png",
    "demotivated": f"{IMG_DIR}/octopus_demotivated.png",
    "smart": f"{IMG_DIR}/octopus_smart.png",
    "lonely": f"{IMG_DIR}/octopus_lonely.png",
    "sad": f"{IMG_DIR}/octopus_sad.png",
    "angry": f"{IMG_DIR}/octopus_angry.png",
    "friend": f"{IMG_DIR}/octopus_friend.png",
    "broken": f"{IMG_DIR}/octopus_broken.png",
    "debug": f"{IMG_DIR}/octopus_debug.png",
    "upload": f"{IMG_DIR}/octopus_upload.png",
}

# ---------------------
# Default face strings
# ---------------------
FACES = {
    "look_r": ["( ⚆_⚆)"],
    "look_l": ["(☉_☉ )"],
    "look_r_happy": ["( ◕‿◕)", "( ≧◡≦)"],
    "look_l_happy": ["(◕‿◕ )", "(≧◡≦ )"],
    "sleep": ["(⇀‿‿↼)", "(≖‿‿≖)", "(－_－)"],
    "awake": ["(◕‿‿◕)"],
    "bored": ["(-__-)", "(—__—)"],
    "intense": ["(°▃▃°)", "(°ロ°)"],
    "cool": ["(⌐■_■)", "(단__단)"],
    "happy": ["(•‿‿•)", "(^‿‿^)", "(^◡◡^)"],
    "excited": ["(ᵔ◡◡ᵔ)", "(✜‿‿✜)"],
    "grateful": ["(^‿‿^)"],
    "motivated": ["(☼‿‿☼)"],
    "demotivated": ["(≖__≖)"],
    "smart": ["(✜‿‿✜)"],
    "lonely": ["(ب__ب)"],
    "sad": ["(╥☁╥ )"],
    "angry": ["(-_-')", "(⇀__⇀)", "(`___´)"],
    "friend": ["(♥‿‿♥)", "(♡‿‿♡)", "(♥‿♥ )", "(♥ω♥ )"],
    "broken": ["(☓‿‿☓)"],
    "debug": ["(#__#)"],
    "upload": ["(1__0)", "(1__1)", "(0__1)"],
}


class octopus_swap(Plugin):
    __author__ = "H-T8"
    __version__ = "0.1.0"
    __description__ = "Replace Pwnagotchi face with precomposed octopus emotion images"

    def on_loaded(self):
        self.images = {}
        self.face_to_key = {}
        self.last_face_line = ""
        self.current_key = "awake"  # fallback state if unknown
        self._render_hooked = False
        self._warned_missing = set()
        logging.info("[octopus_swap] loaded")

    def on_ui_setup(self, ui):
        for key, faces in FACES.items():
            for f in faces:
                self.face_to_key[f] = key

        for key, path in IMAGE_PATHS.items():
            self.images[key] = self._load_img(key, path)

        try:
            ui.on_render(self._after_render)
            self._render_hooked = True
            logging.info("[octopus_swap] registered ui.on_render hook")
        except Exception as e:
            self._render_hooked = False
            logging.exception("[octopus_swap] ui.on_render not available: %s", e)

    def _load_img(self, key: str, path: str):
        try:
            img = Image.open(path).convert("L")
            img = img.resize((IMG_W, IMG_H))
            img = img.convert("1")  # 1-bit for e-ink
            logging.info("[octopus_swap] loaded %-12s %s", key, path)
            return img
        except Exception as e:
            logging.exception(
                "[octopus_swap] failed to load %-12s %s: %s", key, path, e
            )
            return None

    def _face_to_text(self, face_obj):
        if face_obj is None:
            return ""
        if isinstance(face_obj, str):
            return face_obj
        for attr in ("value", "text", "label", "content"):
            if hasattr(face_obj, attr):
                try:
                    return str(getattr(face_obj, attr))
                except Exception:
                    pass
        try:
            return str(face_obj)
        except Exception:
            return ""

    def on_ui_update(self, ui):
        raw_face = ui.get("face")
        face_text = self._face_to_text(raw_face).strip()
        if face_text:
            self.last_face_line = face_text.splitlines()[0]

        ui.set("face", "")

        picked = self.face_to_key.get(self.last_face_line)
        if picked:
            self.current_key = picked

    def _after_render(self, canvas):
        key = self.current_key or "awake"

        img = self.images.get(key)
        if img is None:
            img = self.images.get("awake")
            if img is None:
                return

            if key not in self._warned_missing:
                logging.warning(
                    "[octopus_swap] no image for key=%s yet; falling back to awake", key
                )
                self._warned_missing.add(key)

        try:
            canvas.paste(img, (IMG_X, IMG_Y))
        except Exception as e:
            logging.exception("[octopus_swap] paste failed: %s", e)
