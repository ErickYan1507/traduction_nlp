
# 🌍 DOMARIN Translate

**DOMARIN Translate** est une application de **traduction multilingue intelligente**, moderne et accessible, conçue pour traduire des documents ou du texte libre depuis une interface graphique conviviale.  
Elle intègre également la **lecture vocale multilingue**, l’import/export de fichiers, et la génération de fichiers PDF.

---

## 🎯 Fonctionnalités principales

| Fonctionnalité            | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| ✅ Traduction automatique | Détection de la langue source + choix de langue cible                       |
| 📂 Importation            | Prise en charge de `.txt`, `.docx`, `.pdf`                                  |
| 📄 Export PDF             | Génère un document PDF lisible avec mise en page                           |
| 🔊 Lecture vocale         | Lecture du texte traduit avec synthèse vocale multilingue (`gTTS`)         |
| ⏸▶⏹ Contrôles audio       | Boutons pour mettre en pause, reprendre ou arrêter la lecture vocale        |
| 🖥️ Interface moderne      | Application GUI stylisée avec `customtkinter` (mode sombre activé)          |

---

## 🛠️ Technologies utilisées

| Outil / Librairie     | Version recommandée | Rôle                                          |
|-----------------------|----------------------|-----------------------------------------------|
| Python                | 3.10+                | Langage principal                             |
| Transformers          | 4.x                 | Traduction via Hugging Face models             |
| SentencePiece         | ≥ 0.1.95             | Tokenisation NLP                              |
| gTTS                  | ≥ 2.3                | Synthèse vocale multilingue (Google Text-to-Speech) |
| pygame                | ≥ 2.0                | Contrôle de l’audio (.mp3)                    |
| langdetect            | ≥ 1.0.9              | Détection automatique de la langue source     |
| customtkinter         | ≥ 5.2                | Interface graphique moderne                   |
| python-docx           | ≥ 0.8.11             | Lecture des fichiers Word                     |
| PyMuPDF (`fitz`)      | ≥ 1.20               | Extraction de texte depuis les PDF            |
| reportlab             | ≥ 3.6                | Génération de PDF avec mise en page           |
| huggingface-hub       | ≥ 0.16               | Vérification de l'existence des modèles HF    |

---

## 🚀 Installation rapide

### 1. Clonez ou téléchargez ce dépôt :

```bash
git clone https://github.com/votre-utilisateur/domarin-translate.git
cd domarin-translate
```

### 2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

Ou installez-les manuellement :

```bash
pip install customtkinter transformers sentencepiece torch langdetect gTTS pygame python-docx pymupdf reportlab huggingface_hub
```

### 3. Lancez l’application :

```bash
python DOMARIN_Traducteur_Final.py
```

---

## 📷 Capture d’écran

---

## 🧠 Fonctionnement de la traduction

1. L’utilisateur entre un texte ou importe un fichier.
2. L’application détecte automatiquement la langue source (ex : Anglais).
3. Elle vérifie si le modèle de traduction vers la langue cible (ex : Français) existe.
4. Si oui, elle traduit le texte bloc par bloc (max 450 caractères).
5. L’utilisateur peut écouter, enregistrer en PDF ou continuer à traduire.

---

## 🔁 Limitations & évolutions possibles

- 📡 Certaines paires de langues ne sont pas disponibles sur Hugging Face.
- 💡 La détection automatique n'est pas parfaite pour les petits textes.
- 🔜 Fonctionnalités envisagées :
  - Historique des traductions
  - Mode clair/sombre dynamique
  - Enregistrement audio + génération MP3/PDF simultanée
  - Conversion `.exe` multiplateforme

---

## 🧑‍💻 Auteur

Développé par **Aina Erick Andrianavalona**  
Projet DOMARIN – 2025  
Mention : Informatique – Science des Données & IA

---

## 📄 Licence

Ce projet est distribué sous la licence MIT. Voir le fichier `LICENSE` pour plus de détails.
