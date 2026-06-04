# 🎓 Certificate Generator

A Flask web app for generating certificates from a PNG template with a visual editor, live preview, single certificate creation, and bulk PDF generation.

This project is ideal for training programs, events, workshops, conferences, awards, and any certificate-based use case.

---

## ✨ Features

- 🖱️ **Drag-and-drop editor** for positioning text and signature placeholders
- 🎯 **Custom certificate fields** defined in `template_config.json`
- 🖼️ **Live preview** generated from the same layout logic as the final PDF
- 📄 **Single certificate generation** with form-driven input
- 📦 **Bulk certificate generation** from CSV upload
- 📝 **Flexible CSV mapping** with dynamic field headers
- 🖊️ **Signature image support** with saved placement
- 💾 **JSON configuration** for template layout and fields

---

## 🗂️ Project Structure

```
certificate-generator/
├── app.py                    # Flask app, routes, and PDF generation logic
├── certificate_template.png  # Base certificate template image
├── template_config.json      # Template field positions, font settings, signatures
├── certificates/             # Generated PDF certificates output
├── signatures/               # Signature images referenced by template_config.json
├── templates/                # Flask HTML pages
│   ├── bulk.html
│   ├── editor.html
│   ├── index.html
│   └── single.html
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+

### Installation

```bash
git clone https://github.com/Adith-techie/certificate-generator.git
cd certificate-generator
pip install -r requirements.txt
```

### Run

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🧭 Usage

### 1. Home — `/`

The home page links to the editor, single certificate page, and bulk generation page.

### 2. Template Editor — `/editor`

- Load the certificate template image
- Drag and drop text fields and signature placeholders
- Customize labels, font sizes, and colors
- Save layout changes to `template_config.json`

### 3. Single Certificate — `/single`

- Fill a generated form based on template fields
- Preview the rendered certificate
- Download the final PDF

### 4. Bulk Generation — `/bulk`

- Upload a CSV file containing your certificate data
- Column headers should match the configured field keys
- Download generated certificates as PDF files

---

## ⚙️ How It Works

- `app.py` loads `template_config.json` and reads `certificate_template.png`
- The editor saves field coordinates and formatting to JSON
- Single certificate requests render text and signature images onto a PDF
- Bulk mode reads CSV rows and generates one PDF per row
- Generated files are saved to the `certificates/` folder

---

## 📋 CSV Format Examples

**The first CSV column should be `Name`. Additional columns should match your configured fields.**

### Example for training certificates
```csv
Name,Course,Completion Date
John Smith,Python Basics,2025-06-01
Jane Doe,Machine Learning,2025-06-02
```

### Example for workshop certificates
```csv
Name,Workshop Title,Instructor
Alice Chen,Web Development,Chris Parker
Bob Williams,Cloud Fundamentals,Sara Lee
```

### Example for event certificates
```csv
Name,Organization,Role
Priya Patel,OpenAI Community,Participant
Rahul Kumar,Tech Summit,Speaker
```

---

## 🛠️ Tech Stack

| Layer          | Technology              |
|----------------|-------------------------|
| Backend        | Flask (Python)          |
| PDF Rendering  | PyMuPDF (fitz)          |
| Image Support  | Pillow                  |
| Frontend       | HTML, CSS, JavaScript   |
| Config Storage | JSON                    |

---

## 📄 License

Use and customize this repository freely for certificate generation and event automation.

---

## 🎯 Use Cases

- Graduation and academic certificates
- Training and corporate course completion
- Workshops and bootcamps
- Conference attendance and speaker certificates
- Event awards and appreciation certificates
- Online course completion certificates
- Competition participation and winner certificates

✅ **Any Custom Scenario** — Fully customizable fields and layout

---

## 🔧 Customization

To add or modify fields:

1. Go to `/editor`
2. Customize field names and their positions
3. Save the configuration
4. Fields automatically appear in `/single` and `/bulk` forms
5. Your CSV columns should match the field names

**No code changes required!**
