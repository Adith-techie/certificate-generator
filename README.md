# 🎓 Certificate Generator

A Flask web app for generating PDF certificates from a template — with a **drag-and-drop visual editor**, **single certificate preview**, and **bulk generation** from CSV.


---

## ✨ Features

- 🖱️ **Drag-and-drop editor** — visually position Name, Department, Year, and Signature placeholders directly over the certificate template
- 🔤 **Font-size controls** per placeholder; signature placeholders show actual uploaded images
- 📄 **Single generation** — fill a form, instantly preview and download one certificate
- 📦 **Bulk generation** — upload a CSV (or use the existing `participants_clean.csv`) and download all certificates as a ZIP
- 📐 **Percentage-based coordinates** — positions stored as `%` of page dimensions, zoom and resolution independent
- 🖼️ **Live PDF preview** — template PDF rendered as a PNG background in the editor via `pdf2image`

---

## 🗂️ Project Structure

```
certificate/
├── app.py                    # Flask server — all routes and API endpoints
├── template_config.json      # Saved placeholder coordinates and font sizes
├── participants_clean.csv    # Participant data for bulk generation
├── templates/
│   ├── index.html            # Dashboard with navigation
│   ├── editor.html           # Drag-and-drop template editor
│   ├── single.html           # Single certificate form + preview
│   └── bulk.html             # CSV upload and bulk generation
├── static/
│   ├── js/
│   │   ├── drag.js           # Drag-and-drop logic for placeholders
│   │   ├── editor.js         # Editor UI — config save/load
│   │   └── shared.js         # Shared utilities (API calls, preview fetching)
│   └── css/
│       ├── style.css         # Global styles
│       └── editor.css        # Editor-specific styles
├── signatures/               # Uploaded signature image files
└── certificates/             # Output directory for generated PDFs
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- `poppler` (required by `pdf2image`)
  - **Ubuntu/Debian:** `sudo apt install poppler-utils`
  - **macOS:** `brew install poppler`
  - **Windows:** [Download poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases)

### Installation

```bash
git clone https://github.com/Adith-techie/certificate.git
cd certificate
pip install -r requirements.txt
```

**`requirements.txt`**
```
flask
reportlab
pdf2image
Pillow
```

### Run

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🧭 Usage

### 1. Template Editor — `/editor`

- The certificate template PDF is rendered as a background image.
- Drag placeholders (Name, Department, Year, Signature 1, Signature 2) to the desired positions.
- Adjust font size per text field; upload images for signature placeholders.
- Click **Save** — coordinates are written to `template_config.json` as percentages.

### 2. Single Certificate — `/single`

- Fill in Name, Department, and Year.
- Preview the certificate live in the browser.
- Download as a PDF.

### 3. Bulk Generation — `/bulk`

- Upload a CSV **or** use the existing `participants_clean.csv`.
- Expected columns: `Name`, `Department`, `Year`
- Click **Generate** — all certificates are packaged and downloaded as a `.zip`.

---

## ⚙️ How It Works

```
template_config.json
  └─ {field: {x_pct, y_pct, font_size, width_pct}}
        │
        ▼
  app.py  (reportlab)
        │
        ├─ Renders template PDF as canvas background
        ├─ Converts % coordinates → absolute pixel positions
        ├─ Draws text fields at saved positions
        └─ Draws signature images at saved positions & sizes
```

---

## 📋 CSV Format

```csv
Name,Department,Year
Adith,Computer Science,3rd Year
Jane Doe,Electronics,2nd Year
```

---

## 🛠️ Tech Stack

| Layer       | Technology                    |
|-------------|-------------------------------|
| Backend     | Flask (Python)                |
| PDF Engine  | ReportLab                     |
| PDF Preview | pdf2image + Pillow            |
| Frontend    | Vanilla JS, HTML, CSS         |
| Storage     | JSON config, local filesystem |

---

## 📄 License

This project is for internal use . Not licensed for redistribution.

---
