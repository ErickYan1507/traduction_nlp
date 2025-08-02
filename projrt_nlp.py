import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from transformers import pipeline
from langdetect import detect
from gtts import gTTS
import pygame
import tempfile
import os
from docx import Document
import fitz
from reportlab.pdfgen import canvas
from huggingface_hub import model_info

# === INITIALISATION AUDIO ===
pygame.mixer.init()
audio_path = ""

# === CONFIGURATION APP ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🌍 DOMARIN Translate")
app.geometry("1000x720")

# === LANGUES DISPONIBLES ===
langue_cible_codes = {
    "Français": "fr", "Anglais": "en", "Allemand": "de", "Espagnol": "es",
    "Italien": "it", "Arabe": "ar", "Malgache": "mg", "Portugais": "pt",
    "Chinois": "zh-CN", "Russe": "ru", "Japonais": "ja", "Coréen": "ko",
    "Hindi": "hi", "Turc": "tr", "Ukrainien": "uk", "Grec": "el", "Néerlandais": "nl"
}
langue_cible_var = tk.StringVar(value="Français")

# === VÉRIFICATION DE DISPONIBILITÉ DU MODÈLE ===
def modele_existe(model_name):
    try:
        model_info(model_name)
        return True
    except:
        return False

# === TRADUCTION MULTILINGUE ===
def traduire():
    texte = input_text.get("1.0", "end-1c").strip()
    if not texte:
        return
    try:
        source_lang = detect(texte)
        cible_lang = langue_cible_codes[langue_cible_var.get()]
        if source_lang == cible_lang:
            texte_traduit = texte
        else:
            model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{cible_lang}"
            if not modele_existe(model_name):
                output_text.configure(state="normal")
                output_text.delete("1.0", "end")
                output_text.insert("1.0", f"❌ Modèle indisponible pour : {source_lang} → {cible_lang}")
                output_text.configure(state="disabled")
                return
            traducteur = pipeline("translation", model=model_name)
            blocs = [texte[i:i+450] for i in range(0, len(texte), 450)]
            texte_traduit = ""
            for bloc in blocs:
                res = traducteur(bloc)
                texte_traduit += res[0]['translation_text'] + "\n"
    except Exception as e:
        texte_traduit = f"⚠️ Erreur : {str(e)}"
    output_text.configure(state="normal")
    output_text.delete("1.0", "end")
    output_text.insert("1.0", texte_traduit.strip())
    output_text.configure(state="disabled")

# === IMPORT FICHIER ===
def importer_fichier():
    fichier = filedialog.askopenfilename(filetypes=[("Text", "*.txt"), ("Word", "*.docx"), ("PDF", "*.pdf")])
    if not fichier:
        return
    texte = ""
    try:
        ext = os.path.splitext(fichier)[1].lower()
        if ext == ".txt":
            with open(fichier, "r", encoding="utf-8") as f:
                texte = f.read()
        elif ext == ".docx":
            doc = Document(fichier)
            texte = "\n".join([p.text for p in doc.paragraphs])
        elif ext == ".pdf":
            doc = fitz.open(fichier)
            for page in doc:
                texte += page.get_text()
            doc.close()
    except Exception as e:
        messagebox.showerror("Erreur", str(e))
        return
    input_text.delete("1.0", "end")
    input_text.insert("1.0", texte)

# === EXPORT PDF ===
def exporter_pdf():
    contenu = output_text.get("1.0", "end-1c").strip()
    if not contenu:
        messagebox.showwarning("Vide", "Aucun texte à exporter.")
        return
    fichier = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
    if not fichier:
        return
    try:
        c = canvas.Canvas(fichier, pagesize=(595.27, 841.89))
        c.setFont("Times-Roman", 12)
        y = 800
        for ligne in contenu.split('\n'):
            mots = ligne.split()
            ligne_bloc = ""
            for mot in mots:
                if c.stringWidth(ligne_bloc + mot + " ", "Times-Roman", 12) < 500:
                    ligne_bloc += mot + " "
                else:
                    c.drawString(50, y, ligne_bloc.strip())
                    y -= 18
                    ligne_bloc = mot + " "
                    if y < 50:
                        c.showPage()
                        y = 800
            if ligne_bloc:
                c.drawString(50, y, ligne_bloc.strip())
                y -= 18
        c.save()
        messagebox.showinfo("Succès", "PDF exporté avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# === LECTURE VOCALE ILLIMITÉE AVEC PROTECTION FICHIER ===
def lire_traduction():
    global audio_path
    texte = output_text.get("1.0", "end-1c").strip()
    if not texte:
        messagebox.showwarning("Attention", "Aucun texte à lire.")
        return
    lang_code = langue_cible_codes[langue_cible_var.get()]
    try:
        blocs = [texte[i:i+5000] for i in range(0, len(texte), 5000)]
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, "domarin_temp_audio.mp3")

        # Stopper et décharger l’audio en cours (si existant)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

        # Supprimer ancien fichier si possible
        if os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de supprimer l'ancien audio :\n{str(e)}")
                return

        tts = gTTS(text=" ".join(blocs), lang=lang_code)
        tts.save(audio_path)
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(loops=-1)  # Lecture en boucle
    except Exception as e:
        messagebox.showerror("Erreur audio", str(e))

def pause_audio():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()

def reprendre_audio():
    pygame.mixer.music.unpause()

def stop_audio():
    pygame.mixer.music.stop()

# === INTERFACE UTILISATEUR ===
titre = ctk.CTkLabel(app, text="🌍 DOMARIN TRANSLATE", font=ctk.CTkFont(size=24, weight="bold"))
titre.pack(pady=10)

input_text = ctk.CTkTextbox(app, height=160, font=("Segoe UI", 12))
input_text.pack(padx=20, pady=10, fill="x")

choix_langue = ctk.CTkOptionMenu(app, values=list(langue_cible_codes.keys()), variable=langue_cible_var)
choix_langue.pack(pady=5)

output_text = ctk.CTkTextbox(app, height=160, font=("Segoe UI", 12), state="disabled")
output_text.pack(padx=20, pady=10, fill="x")

# === BOUTONS ===
btn_frame = ctk.CTkFrame(app)
btn_frame.pack(pady=10)

ctk.CTkButton(btn_frame, text="📂 Importer", command=importer_fichier, width=140).grid(row=0, column=0, padx=5)
ctk.CTkButton(btn_frame, text="🌍 Traduire", command=traduire, width=140).grid(row=0, column=1, padx=5)
ctk.CTkButton(btn_frame, text="📄 Exporter PDF", command=exporter_pdf, width=140).grid(row=0, column=2, padx=5)
ctk.CTkButton(btn_frame, text="🔈 Lire", command=lire_traduction, width=140).grid(row=1, column=0, padx=5, pady=5)
ctk.CTkButton(btn_frame, text="⏸ Pause", command=pause_audio, width=140).grid(row=1, column=1, padx=5, pady=5)
ctk.CTkButton(btn_frame, text="▶ Reprendre", command=reprendre_audio, width=140).grid(row=1, column=2, padx=5, pady=5)
ctk.CTkButton(btn_frame, text="⏹ Stop", command=stop_audio, width=140).grid(row=1, column=3, padx=5, pady=5)
ctk.CTkButton(btn_frame, text="❌ Quitter", command=app.destroy, width=140).grid(row=1, column=4, padx=5, pady=5)

# === DÉMARRAGE DE L'APPLICATION ===
app.mainloop()
