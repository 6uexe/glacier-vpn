import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests
import math

# GLACIER VPN - VERSION PUBLIQUE
# Version de démonstration : aucun tunnel VPN personnel inclus.

COUNTRIES = ["🇺🇸 États-Unis", "🇨🇭 Suisse"]
selected_country = COUNTRIES[0]

BG = "#101820"
PANEL = "#1a2938"
BLUE = "#2878d0"
RED = "#ff6262"
MUTED = "#8294a8"


def animate_circle():
    canvas.delete("all")
    canvas.create_oval(
        8, 8, 62, 62, outline=RED, width=5
    )
    canvas.create_text(
        35, 35, text="×", fill=RED,
        font=("Segoe UI", 25, "bold")
    )
    root.after(70, animate_circle)


def select_country(event=None):
    global selected_country
    selected_country = country_box.get()
    selected_label.config(text=selected_country)


def connect():
    messagebox.showinfo(
        "Glacier VPN",
        "Version publique de démonstration.\n\n"
        "Aucun serveur VPN public n'est encore configuré. "
        "Aucune connexion ne sera démarrée."
    )


def disconnect():
    messagebox.showinfo(
        "Glacier VPN",
        "Aucun tunnel VPN n'a été démarré."
    )


def get_ip_info():
    try:
        response = requests.get(
            "https://ipapi.co/json/", timeout=8
        )
        response.raise_for_status()
        data = response.json()

        ip = data.get("ip") or "Indisponible"
        city = data.get("city") or ""
        country = data.get("country_name") or ""
        location = ", ".join(
            part for part in (city, country) if part
        ) or "Indisponible"

        root.after(
            0, lambda: ip_label.config(text=ip)
        )
        root.after(
            0, lambda: location_label.config(text=location)
        )

    except Exception:
        root.after(
            0, lambda: ip_label.config(text="Indisponible")
        )
        root.after(
            0,
            lambda: location_label.config(
                text="Vérification impossible"
            )
        )


def refresh_ip():
    threading.Thread(
        target=get_ip_info, daemon=True
    ).start()


root = tk.Tk()
root.title("Glacier VPN - Version publique")
root.geometry("720x590")
root.configure(bg=BG)
root.resizable(False, False)

tk.Label(
    root, text="GLACIER VPN",
    font=("Segoe UI", 27, "bold"),
    bg=BG, fg="white"
).pack(pady=(22, 3))

tk.Label(
    root, text="YOUR CONNECTION. YOUR CONTROL.",
    font=("Segoe UI", 9),
    bg=BG, fg=MUTED
).pack(pady=(0, 20))

panel = tk.Frame(
    root, bg=PANEL, padx=30, pady=25
)
panel.pack(
    fill="both", expand=True, padx=35, pady=5
)

tk.Label(
    panel, text="CHOISIS TON PAYS",
    font=("Segoe UI", 11, "bold"),
    bg=PANEL, fg="white"
).pack(anchor="w")

country_box = ttk.Combobox(
    panel, values=COUNTRIES,
    state="readonly",
    font=("Segoe UI", 12),
    width=30
)
country_box.pack(anchor="w", pady=12)
country_box.set(selected_country)
country_box.bind(
    "<<ComboboxSelected>>", select_country
)

tk.Label(
    panel, text="PAYS SÉLECTIONNÉ",
    font=("Segoe UI", 9),
    bg=PANEL, fg=MUTED
).pack(anchor="w", pady=(8, 2))

selected_label = tk.Label(
    panel, text=selected_country,
    font=("Segoe UI", 13, "bold"),
    bg=PANEL, fg="white"
)
selected_label.pack(anchor="w")

status_frame = tk.Frame(panel, bg=PANEL)
status_frame.pack(anchor="w", pady=(18, 5))

canvas = tk.Canvas(
    status_frame, width=70, height=70,
    bg=PANEL, highlightthickness=0
)
canvas.pack(side="left", padx=(0, 15))

status_text_frame = tk.Frame(
    status_frame, bg=PANEL
)
status_text_frame.pack(side="left")

tk.Label(
    status_text_frame,
    text="ÉTAT DE LA CONNEXION",
    font=("Segoe UI", 9),
    bg=PANEL, fg=MUTED
).pack(anchor="w")

tk.Label(
    status_text_frame,
    text="DÉMONSTRATION — NON CONNECTÉ",
    font=("Segoe UI", 12, "bold"),
    bg=PANEL, fg="#f0c45c"
).pack(anchor="w", pady=4)

tk.Label(
    panel, text="PAYS CONNECTÉ",
    font=("Segoe UI", 9),
    bg=PANEL, fg=MUTED
).pack(anchor="w", pady=(12, 2))

tk.Label(
    panel, text="Aucun — serveur non configuré",
    font=("Segoe UI", 11),
    bg=PANEL, fg="white"
).pack(anchor="w")

buttons = tk.Frame(panel, bg=PANEL)
buttons.pack(anchor="w", pady=18)

tk.Button(
    buttons, text="SE CONNECTER",
    command=connect,
    font=("Segoe UI", 11, "bold"),
    bg=BLUE, fg="white",
    relief="flat", padx=20, pady=12
).pack(side="left", padx=(0, 10))

tk.Button(
    buttons, text="DÉCONNECTER",
    command=disconnect,
    font=("Segoe UI", 11, "bold"),
    bg="#34485b", fg="white",
    relief="flat", padx=20, pady=12
).pack(side="left")

tk.Label(
    panel, text="IP PUBLIQUE",
    font=("Segoe UI", 9),
    bg=PANEL, fg=MUTED
).pack(anchor="w")

ip_label = tk.Label(
    panel, text="En attente...",
    font=("Segoe UI", 11),
    bg=PANEL, fg="white"
)
ip_label.pack(anchor="w", pady=(2, 8))

tk.Label(
    panel, text="LOCALISATION IP",
    font=("Segoe UI", 9),
    bg=PANEL, fg=MUTED
).pack(anchor="w")

location_label = tk.Label(
    panel, text="En attente...",
    font=("Segoe UI", 11),
    bg=PANEL, fg="white"
)
location_label.pack(anchor="w", pady=(2, 0))

tk.Label(
    root,
    text="Glacier VPN • Version publique de démonstration",
    font=("Segoe UI", 9),
    bg=BG, fg="#60758a"
).pack(pady=9)

animate_circle()
refresh_ip()
root.mainloop()