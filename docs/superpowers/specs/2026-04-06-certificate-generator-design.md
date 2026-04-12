# Certificate Generator Web App - Design Spec

## Summary
Flask web app for generating PDF certificates from a template, with drag-and-drop placeholder positioning and both single + bulk generation.

## Components

### Template Editor (`/editor`)
- Renders template PDF as scaled image overlay
- Draggable placeholder boxes for: Name, Department, Year, Signature 1, Signature 2
- Each placeholder has font-size control
- Signature placeholders show uploaded images with configurable size
- Saves coordinates as percentages to `template_config.json`

### Single Certificate Gen (`/single`)
- Form: name, department, year
- Preview in iframe, download link

### Bulk Generation (`/bulk`)
- CSV upload or use existing `participants_clean.csv`
- Generate all as ZIP download

### PDF Generation (reportlab)
- Reads `template_config.json` for absolute coordinates (convert from percentages)
- Draws text at saved positions
- Draws signature images at saved positions and sizes
- Background: template PDF rendered onto new canvas

### Data
- `template_config.json`: `{field: {x_pct, y_pct, font_size, width_pct}}`
- Signatures stored in `signatures/`, referenced by filename in config
- No database needed

## Key Decisions
- Approach: Flask + vanilla JS (no build step, fast hackathon iteration)
- PDF as background: rendered to PNG for preview via pdf2image
- Coordinates stored as percentages of full dimensions for zoom independence
- Existing `participants_clean.csv` format preserved
