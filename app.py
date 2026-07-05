import csv
import json
import os
import tempfile
import uuid
import zipfile
from io import BytesIO, StringIO

import fitz
from flask import Flask, jsonify, request, render_template, send_file, send_from_directory

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "template_config.json")
SIGNATURES_DIR = os.path.join(BASE_DIR, "signatures")
OUT_DIR = os.path.join(BASE_DIR, "certificates")
TEMPLATE_IMAGE = os.path.join(BASE_DIR, "certificate_template.png")
WINDOWS_FONTS = r"C:\Windows\Fonts"

# Landscape A4 dimensions in points
PDF_WIDTH, PDF_HEIGHT = 841.89, 595.28

os.makedirs(SIGNATURES_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# ─── Helpers ───────────────────────────────────────────────────────────

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

_FONT_CACHE = {}

def _get_font(font_name=None):
    if not font_name or font_name not in _FONT_CACHE:
        try:
            fpath = os.path.join(WINDOWS_FONTS, font_name) if font_name else None
            if font_name and os.path.exists(fpath):
                _FONT_CACHE[font_name] = fitz.Font(fontfile=fpath)
            else:
                _FONT_CACHE.setdefault("_default", fitz.Font("hebo"))
        except Exception:
            _FONT_CACHE.setdefault("_default", fitz.Font("hebo"))
    if font_name and font_name in _FONT_CACHE:
        return _FONT_CACHE[font_name]
    return _FONT_CACHE["_default"]

def _hex_to_rgb(hex_color):
    """Convert hex color to (R, G, B) tuple 0-1."""
    h = (hex_color or "#5a4a2e").lstrip("#")
    if len(h) == 3:
        h = h[0] * 2 + h[1] * 2 + h[2] * 2
    r = int(h[0:2], 16) / 255
    g = int(h[2:4], 16) / 255
    b = int(h[4:6], 16) / 255
    return (r, g, b)

def _abs_pt(cfg, w, h):
    """Convert percentage coordinates to PDF points."""
    x = cfg["x_pct"] * w
    y = (1.0 - cfg["y_pct"]) * h
    return x, y

def _draw_text(page, text, cfg, w, h):
    """Draw text centered at the config position using PyMuPDF TextWriter."""
    x, y = _abs_pt(cfg, w, h)
    size = cfg.get("font_size", 32)
    color = _hex_to_rgb(cfg.get("color", "#5a4a2e"))

    font = _get_font(cfg.get("font_name"))
    tw = font.text_length(text, fontsize=size)

    tr = fitz.TextWriter(page.rect)
    tr.color = color
    tr.append(
        fitz.Point(x - tw / 2, y), text,
        font=font, fontsize=size
    )
    tr.write_text(page, overlay=True)

def _draw_signature(page, sig_path, cfg, w, h):
    """Draw signature image centered at config position."""
    if not os.path.exists(sig_path):
        return
    x, y = _abs_pt(cfg, w, h)
    sig_w = cfg.get("width_pct", 0.08) * w
    sig_h = cfg.get("height_pct", None)
    if sig_h is not None:
        sig_h = sig_h * h
        img_rect = fitz.Rect(x - sig_w / 2, y - sig_h / 2, x + sig_w / 2, y + sig_h / 2)
    else:
        img_w, img_h = get_image_dimensions(sig_path)
        aspect = img_h / img_w if img_w else 1.0
        sig_h = sig_w * aspect
        img_rect = fitz.Rect(x - sig_w / 2, y - sig_h / 2, x + sig_w / 2, y + sig_h / 2)
    page.insert_image(img_rect, filename=sig_path)

def _apply_text_and_signatures(page, config, fields_data, extra_texts=None):
    """Apply all text fields and signatures to a page."""
    w, h = PDF_WIDTH, PDF_HEIGHT

    custom_fields = config.get("custom_fields", [])
    extra_texts = extra_texts or []

    for field in custom_fields:
        field_key = field["key"]
        text_value = fields_data.get(field_key, field.get("sample_text", ""))
        if field_key in config and "x_pct" in config[field_key]:
            _draw_text(page, text_value, config[field_key], w, h)

    # Extra text fields (legacy support)
    for i, extra_text in enumerate(config.get("extra_texts", [])):
        text_value = extra_texts[i] if i < len(extra_texts) else extra_text.get("sample_text", "")
        _draw_text(page, text_value, extra_text, w, h)

    sig1_file = config["signature1"].get("file")
    if sig1_file:
        _draw_signature(page, os.path.join(SIGNATURES_DIR, sig1_file), config["signature1"], w, h)
    sig2_file = config["signature2"].get("file")
    if sig2_file:
        _draw_signature(page, os.path.join(SIGNATURES_DIR, sig2_file), config["signature2"], w, h)

    # Extra signatures
    for extra_sig in config.get("extra_signatures", []):
        sig_file = extra_sig.get("file")
        if sig_file:
            _draw_signature(page, os.path.join(SIGNATURES_DIR, sig_file), extra_sig, w, h)

def generate_single_pdf(fields_data, config, extra_texts=None):
    """Generate a single certificate PDF."""
    name = fields_data.get("name", "Certificate Recipient").replace(' ', '_')
    out_path = os.path.join(OUT_DIR, f"{uuid.uuid4().hex[:8]}_{name}.pdf")
    doc = fitz.open()
    page = doc.new_page(width=PDF_WIDTH, height=PDF_HEIGHT)
    page.insert_image(page.rect, filename=TEMPLATE_IMAGE)
    _apply_text_and_signatures(page, config, fields_data, extra_texts)
    doc.save(out_path)
    doc.close()
    return out_path

def generate_preview_png(fields_data, config, extra_texts=None):
    """Generate a PNG preview identical to PDF generation."""
    doc = fitz.open()
    page = doc.new_page(width=PDF_WIDTH, height=PDF_HEIGHT)
    page.insert_image(page.rect, filename=TEMPLATE_IMAGE)
    _apply_text_and_signatures(page, config, fields_data, extra_texts)
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    data = pix.tobytes("png")
    doc.close()
    return data

def get_image_dimensions(path):
    from PIL import Image as PILImage
    with PILImage.open(path) as img:
        return img.size

# ─── Routes ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("landing.html")

@app.route("/editor")
def editor():
    return render_template("editor.html")

@app.route("/single")
def single_cert():
    return render_template("single.html")

@app.route("/bulk")
def bulk():
    return render_template("bulk.html")

@app.route("/api/template-image")
def template_image():
    return send_file(TEMPLATE_IMAGE, mimetype="image/png")

@app.route("/api/preview", methods=["POST"])
def preview():
    """Generate a PNG preview identical to the final PDF."""
    data = request.json
    fields_data = data.get("fields", {})
    extra_texts = data.get("extra_texts", [])
    
    config = load_config()
    if "config" in data:
        for key in ("custom_fields", "signature1", "signature2", "extra_texts", "extra_signatures"):
            if key in data["config"]:
                if key in ("extra_texts", "extra_signatures", "custom_fields"):
                    config[key] = data["config"][key]
                elif key in config:
                    config[key].update(data["config"][key])

    png_data = generate_preview_png(fields_data, config, extra_texts)
    return send_file(BytesIO(png_data), mimetype="image/png")

@app.route("/api/config", methods=["GET"])
def get_config():
    return jsonify(load_config())

@app.route("/api/config", methods=["POST"])
def save_config():
    config = request.json
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    return jsonify({"status": "ok"})

@app.route("/api/fields", methods=["GET"])
def get_fields():
    """Get list of custom fields."""
    config = load_config()
    fields = config.get("custom_fields", [])
    return jsonify({"fields": fields})

@app.route("/api/fields", methods=["POST"])
def save_fields():
    """Save custom fields configuration."""
    data = request.json
    fields = data.get("fields", [])
    
    config = load_config()
    config["custom_fields"] = fields
    
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    
    return jsonify({"status": "ok", "fields": fields})

@app.route("/api/field", methods=["POST"])
def add_field():
    """Add a single custom field."""
    data = request.json
    field = data.get("field")
    
    config = load_config()
    if "custom_fields" not in config:
        config["custom_fields"] = []
    
    config["custom_fields"].append(field)
    
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    
    return jsonify({"status": "ok"})

@app.route("/api/field/<field_key>", methods=["DELETE"])
def delete_field(field_key):
    """Delete a custom field."""
    config = load_config()
    fields = config.get("custom_fields", [])
    config["custom_fields"] = [f for f in fields if f.get("key") != field_key]
    
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    
    return jsonify({"status": "ok"})

@app.route("/signatures/<filename>")
def serve_signature(filename):
    return send_from_directory(SIGNATURES_DIR, filename)

@app.route("/api/upload-signature", methods=["POST"])
def upload_signature():
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400
    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    ext = os.path.splitext(f.filename)[1]
    filename = f"sig_{uuid.uuid4().hex[:8]}{ext}"
    path = os.path.join(SIGNATURES_DIR, filename)
    f.save(path)
    w, h = get_image_dimensions(path)
    return jsonify({"filename": filename, "width": w, "height": h})

@app.route("/api/upload-template", methods=["POST"])
def upload_template():
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400
    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    
    # Save the uploaded template
    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in [".png", ".jpg", ".jpeg"]:
        return jsonify({"error": "Unsupported file type. Use PNG or JPG."}), 400
    
    template_path = os.path.join(BASE_DIR, f"certificate_template{ext}")
    f.save(template_path)
    
    # Update global TEMPLATE_IMAGE variable
    global TEMPLATE_IMAGE
    TEMPLATE_IMAGE = template_path
    
    return jsonify({"status": "ok", "template_path": template_path})

@app.route("/api/delete-signature", methods=["POST"])
def delete_signature():
    data = request.json
    filename = data.get("filename")
    if not filename:
        return jsonify({"error": "No filename"}), 400
    path = os.path.join(SIGNATURES_DIR, filename)
    if os.path.exists(path):
        os.remove(path)
        return jsonify({"status": "ok"})
    return jsonify({"status": "not found"}), 404

@app.route("/api/generate-single", methods=["POST"])
def generate_single():
    data = request.json
    fields_data = data.get("fields", {})
    extra_texts = data.get("extra_texts", [])
    
    if not fields_data.get("name"):
        return jsonify({"error": "Name is required"}), 400
    
    config = load_config()
    pdf_path = generate_single_pdf(fields_data, config, extra_texts)
    name = fields_data.get("name", "Certificate").replace(' ', '_')
    return send_file(pdf_path, mimetype="application/pdf", as_attachment=True,
                     download_name=f"{name}_certificate.pdf")

@app.route("/api/generate-bulk", methods=["POST"])
def generate_bulk():
    data = request.json
    records = data.get("records", [])
    
    if not records:
        return jsonify({"error": "No records provided"}), 400
    
    config = load_config()
    
    zip_buf = tempfile.NamedTemporaryFile(suffix=".zip", delete=False, dir=OUT_DIR)
    zip_buf.close()
    
    with zipfile.ZipFile(zip_buf.name, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, record in enumerate(records, 1):
            record_clean = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in record.items() if v}
            
            # Extract name and other fields
            fields_data = {}
            extra_texts = []
            
            for key, value in record_clean.items():
                if key == "name":
                    fields_data["name"] = value
                elif key.startswith("extra_text_"):
                    # Handle extra_text_1, extra_text_2, etc.
                    idx = int(key.replace("extra_text_", "")) - 1
                    while len(extra_texts) <= idx:
                        extra_texts.append("")
                    extra_texts[idx] = value
                else:
                    # Map other columns to custom fields
                    fields_data[key] = value
            
            if not fields_data.get("name"):
                continue  # Skip records without name
            
            pdf_path = generate_single_pdf(fields_data, config, extra_texts)
            arc_name = f"{i:02d}_{fields_data['name'].replace(' ', '_')}.pdf"
            zf.write(pdf_path, arc_name)
            os.remove(pdf_path)
    
    return send_file(zip_buf.name, mimetype="application/zip",
                     as_attachment=True, download_name="certificates.zip")

if __name__ == "__main__":
    print("Starting Certificate Generator at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
