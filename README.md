# PDF Splitter - Automatische Rechnungstrennung

Eine Web-Anwendung zum automatischen Erkennen und Trennen von Rechnungen in PDF-Dateien.

## Features

- 🔍 Automatische Erkennung von Rechnungen (auch mehrseitig)
- 🎯 Kombinierte Text- und visuelle Analyse
- 🌐 Web-Interface mit Drag & Drop
- 📄 Unterstützt mehrseitige Rechnungen
- ⚡ Schnelle Verarbeitung

## Installation

1. Repository klonen:
```bash
git clone <repository-url>
cd pdf-splitter
```

2. Dependencies installieren:
```bash
pip install -r requirements.txt
```

3. Anwendung starten:
```bash
python app.py
```

4. Browser öffnen: http://localhost:5000

## Verwendung

### Web-Interface

1. **Upload**: PDF-Datei per Drag & Drop hochladen oder durch Klicken auswählen
2. **Analyse**: Die Anwendung analysiert automatisch das PDF und zeigt erkannte Rechnungen an
3. **Teilen**: Mit einem Klick wird das PDF in separate Dateien geteilt
4. **Download**: Einzelne Rechnungen oder alle als ZIP herunterladen

### Programmierung

```python
from pdf_processor import PDFProcessor

# Processor erstellen
processor = PDFProcessor(output_dir="output")

# PDF analysieren (ohne zu teilen)
analysis = processor.analyze_pdf("rechnungen.pdf")
print(f"Erkannte Rechnungen: {analysis['detected_invoices']}")

# PDF teilen
results = processor.split_pdf("rechnungen.pdf", output_prefix="rechnung")
for result in results:
    print(f"Erstellt: {result['output_file']}")
```

### Tests ausführen

```bash
python test_example.py
```

## Funktionsweise

Die Anwendung nutzt zwei Erkennungsmethoden:

1. **Text-Analyse**: Erkennt Rechnungskopfzeilen, Rechnungsnummern und Schlüsselwörter
2. **Visuelle Analyse**: Erkennt Leerseiten und große Abstände zwischen Dokumenten

## Projekt-Struktur

```
pdf-splitter/
├── app.py              # Flask Web-Server
├── pdf_processor.py    # PDF-Verarbeitung und Splitting
├── invoice_detector.py # Rechnungserkennung
├── test_example.py     # Beispiel-Tests
├── requirements.txt    # Python Dependencies
├── static/             # CSS, JavaScript
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── templates/          # HTML Templates
│   └── index.html
├── uploads/            # Temporäre Uploads (wird automatisch erstellt)
└── output/             # Geteilte PDFs (wird automatisch erstellt)
```

## Erkennungsmethoden

Die Anwendung verwendet intelligente Kombinationen mehrerer Erkennungsmethoden:

### Text-basierte Erkennung
- Sucht nach Schlüsselwörtern: "Rechnung", "Invoice", "Rechnungsnummer", etc.
- Erkennt typische Rechnungsnummern-Muster (z.B. "2024-001", "RE20240001")
- Funktioniert mit deutschen und englischen Rechnungen

### Visuelle Erkennung
- Erkennt Leerseiten als Trenner zwischen Dokumenten
- Analysiert Textdichte auf Seiten
- Identifiziert große Abstände zwischen Dokumenten

### Mehrseitige Rechnungen
- Gruppiert zusammengehörige Seiten automatisch
- Eine Rechnung kann beliebig viele Seiten umfassen
- Nutzt Kontext-Informationen zur korrekten Gruppierung

## Technologie-Stack

- **Backend**: Flask (Python Web-Framework)
- **PDF-Verarbeitung**: pypdf, pdfplumber
- **Frontend**: Vanilla JavaScript, CSS3
- **UI/UX**: Responsive Design mit Drag & Drop

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.
