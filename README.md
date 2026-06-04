# 🎓 Certificate Generator

A **universal** Flask web app for generating PDF certificates from a custom template — with a **drag-and-drop visual editor**, **customizable fields**, **single certificate preview**, and **bulk generation** from CSV.

Perfect for **colleges, corporate training, workshops, conferences, events, and any certification need**.

---

## ✨ Features

- 🖱️ **Drag-and-drop editor** — visually position any fields and signatures on the certificate template
- 🎯 **Customizable fields** — define your own certificate fields (Name, Organization, Role, Department, Award, etc.)
- 🔤 **Font & color controls** — adjust font size, style, and color per field
- 📄 **Single generation** — fill a form, instantly preview and download one certificate
- 📦 **Bulk generation** — upload a CSV with any column headers and download all certificates as a ZIP
- 📐 **Percentage-based coordinates** — positions stored as `%` of page dimensions, resolution independent
- 🖼️ **Live preview** — see changes instantly in the editor
- 🚀 **No code changes needed** — fully generic, works for any use case

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

> **Note:** No system dependencies required! PyMuPDF handles all PDF operations.
 
### Installation
 
```bash
git clone https://github.com/Adith-techie/certificate-generator.git
cd certificate-generator
pip install -r requirements.txt
```
 
**`requirements.txt`**
```
Flask==3.1.0
PyMuPDF==1.24.0
Pillow==11.2.1
```
 
### Run
 
```bash
python app.py
```
 
Open [http://localhost:5000](http://localhost:5000) in your browser.
 
---

## 🧭 Usage

### 1. Template Editor — `/editor`

- The certificate template PNG is displayed as a background
- Drag placeholders to position them on the template
- Customize field names and labels (Name, Organization, Role, Department, Award, etc.)
- Adjust font size, color, and font per field
- Upload images for signature placeholders
- Click **Save** — coordinates are written to `template_config.json`

### 2. Single Certificate — `/single`

- Form fields are **automatically generated** based on your template configuration
- Fill in the details and preview the certificate
- Download as a PDF

### 3. Bulk Generation — `/bulk`

- Upload a CSV file with **any column headers** (first column must be "Name")
- Or paste CSV data directly into the text area
- Column headers match your certificate fields
- All certificates are packaged and downloaded as a `.zip`

---

## ⚙️ How It Works

```
template_config.json
  └─ {custom_fields: [...], field_configs: {...}}
       │
       ▼
  app.py  (PyMuPDF - fitz)
       │
       ├─ Loads custom field definitions
       ├─ Maps CSV columns to fields
       ├─ Converts % coordinates → absolute positions
       ├─ Draws text fields at saved positions
       ├─ Draws signature images at saved positions
       └─ Generates PDF certificate
```

**Fully Generic:**
- No hardcoded field names (Department, Year, etc.)
- Field names defined in `template_config.json`
- CSV columns automatically matched to template fields
- Works for any use case without code changes

---

## 📋 CSV Format Examples

**First column MUST be "Name". All other columns are flexible based on your certificate fields.**

### 📚 For College/University Certificates:
```csv
Name,Department,Year of Study
Adith,Computer Science,3rd Year
Jane Doe,Electronics,2nd Year
```

### 💼 For Corporate Training:
```csv
Name,Company,Course,Completion Date
John Smith,TechCorp Inc,Advanced Python,2024-06-01
Sarah Johnson,DataSoft,Machine Learning,2024-06-02
```

### 🎓 For Workshops:
```csv
Name,Workshop Title,Level,Attendance Hours
Alice Chen,Web Development Bootcamp,Advanced,40
Bob Williams,Cloud Computing,Intermediate,30
```

### 🎤 For Conferences:
```csv
Name,Company,Session Attended,Date
Dr. Emma Wilson,University ABC,AI Trends in 2024,2024-05-15
Prof. James Lee,Research Institute,Ethics in ML,2024-05-16
```

### 🎖️ For General Events:
```csv
Name,Organization,Role,Date
Recipient Name,Your Organization,Achievement Title,2024-06-04
```

**👉 Customize field names to match your certificate template configuration!**

---

## 🛠️ Tech Stack

| Layer       | Technology                    |
|-------------|-------------------------------|
| Backend     | Flask (Python)                |
| PDF Engine  | PyMuPDF (fitz)                |
| Image Handling | Pillow                    |
| Frontend    | Vanilla JS, HTML, CSS         |
| Storage     | JSON config, local filesystem |

---

## 📄 License

This project is provided as-is for general use. Feel free to customize and use for your certificate generation needs.

---

## 🎯 Use Cases

✅ **College & University** — Graduation, course completion, achievement certificates  
✅ **Corporate Training** — Employee training completion, certification courses  
✅ **Workshops & Bootcamps** — Participation, skill level, completion certificates  
✅ **Conferences** — Attendance, speaker, session participation certificates  
✅ **Events** — Award, appreciation, participation certificates  
✅ **Online Learning** — Course completion, badge certificates  
✅ **Competitions** — Winner, participant, finalist certificates  
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
