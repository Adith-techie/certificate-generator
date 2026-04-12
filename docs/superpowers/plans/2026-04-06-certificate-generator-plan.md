# Certificate Generator Web App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A Flask web app for generating PDF certificates from a template, with drag-and-drop placeholder positioning and both single + bulk generation.

**Architecture:** Flask dev server with vanilla JS frontend. Template editor renders the PDF as a background image with draggable placeholder overlays; coordinates are saved as percentages to `template_config.json`. Single and bulk generation use reportlab to draw text/signatures at saved coordinates onto the template PDF.

**Tech Stack:** Flask, reportlab, pdf2image, Pillow, vanilla JS, HTML/CSS

---

## File Structure

| File | Responsibility |
|------|---------------|
| `app.py` | Flask server, all routes and API endpoints |
| `templates/index.html` | Dashboard page with navigation |
| `templates/editor.html` | Template editor with drag-and-drop |
| `templates/single.html` | Single certificate entry form + preview |
| `templates/bulk.html` | CSV upload and bulk generation |
| `template_config.json` | Saved coordinates and sizes for all placeholders |
| `static/js/drag.js` | Drag-and-drop logic for placeholder markers |
| `static/js/editor.js` | Editor UI logic, config save/load |
| `static/js/shared.js` | Shared utilities (API calls, preview fetching) |
| `static/css/style.css` | Global styles |
| `static/css/editor.css` | Editor-specific styles |
| `signatures/` | Uploaded signature image files |
| `certificates/` | Output directory for generated PDFs (already exists) |
| `participants_clean.csv` | Input data (already exists) |

---
