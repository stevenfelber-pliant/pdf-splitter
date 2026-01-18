# PDF Splitter - Automatische Rechnungstrennung

Eine Web-Anwendung zum automatischen Erkennen und Trennen von Rechnungen in PDF-Dateien.

## Features

- 🖼️ **NEU:** Interaktive Vorschau mit Miniaturansichten aller Seiten
- 🎨 **NEU:** Drag & Drop zum Verschieben von Seiten zwischen Gruppen
- ✏️ **NEU:** Gruppen umbenennen, löschen und hinzufügen
- 🔍 Automatische Erkennung von Rechnungen (auch mehrseitig)
- 🎯 Kombinierte Text- und visuelle Analyse
- 📄 Unterstützt mehrseitige Rechnungen
- ⚡ Schnelle Verarbeitung
- 🔒 Datenschutz: Alle Daten bleiben auf Ihrem Computer

## Schnellstart - Browser-Version (empfohlen)

**Keine Installation nötig!** Funktioniert komplett im Browser.

1. Öffnen Sie `browser-app.html` direkt in Ihrem Browser (Doppelklick auf die Datei)
2. Fertig! Sie können sofort PDFs hochladen und teilen

**Vorteile:**
- ✅ Keine Installation erforderlich
- ✅ Funktioniert offline
- ✅ Alle Daten bleiben lokal auf Ihrem Computer
- ✅ Funktioniert auf Windows, Mac und Linux

## Server-Version (für erweiterte Nutzung)

Falls Sie die Python-basierte Server-Version nutzen möchten:

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

### Browser-Version (`browser-app.html`)

1. **Upload**: PDF-Datei per Drag & Drop hochladen oder durch Klicken auswählen
2. **Analyse**: Die Anwendung analysiert automatisch und zeigt **Miniaturansichten aller Seiten**
3. **Vorschau prüfen**: Sehen Sie alle Seiten gruppiert nach erkannten Rechnungen
4. **Anpassen (NEU)**:
   - Seiten per Drag & Drop zwischen Gruppen verschieben
   - Gruppen umbenennen (einfach auf Namen klicken)
   - Gruppen löschen oder neue hinzufügen
5. **Teilen**: Erst NACH der visuellen Kontrolle wird das PDF geteilt
6. **Download**: Einzelne Rechnungen oder alle als ZIP herunterladen

**Hinweis:** Die Browser-Version verarbeitet alles lokal in Ihrem Browser. Es werden keine Daten hochgeladen oder an einen Server gesendet.

**Tipp:** Mit der interaktiven Vorschau haben Sie die volle Kontrolle! Prüfen Sie die Aufteilung visuell und passen Sie sie bei Bedarf an, bevor Sie teilen.

### Server-Version (Web-Interface)

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
├── browser-app.html    # 🌟 Browser-Version (EMPFOHLEN - einfach öffnen!)
├── app.py              # Flask Web-Server (Server-Version)
├── pdf_processor.py    # PDF-Verarbeitung und Splitting (Server-Version)
├── invoice_detector.py # Rechnungserkennung (Server-Version)
├── test_example.py     # Beispiel-Tests
├── requirements.txt    # Python Dependencies (nur für Server-Version)
├── static/             # CSS, JavaScript (Server-Version)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── templates/          # HTML Templates (Server-Version)
│   └── index.html
├── uploads/            # Temporäre Uploads (Server-Version)
└── output/             # Geteilte PDFs (Server-Version)
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

### Browser-Version
- **PDF-Lesen**: PDF.js (Mozilla)
- **PDF-Erstellung**: pdf-lib
- **ZIP-Archiv**: JSZip
- **Frontend**: Vanilla JavaScript, CSS3
- **UI/UX**: Responsive Design mit Drag & Drop

### Server-Version
- **Backend**: Flask (Python Web-Framework)
- **PDF-Verarbeitung**: pypdf, pdfplumber
- **Frontend**: Vanilla JavaScript, CSS3
- **UI/UX**: Responsive Design mit Drag & Drop

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.
