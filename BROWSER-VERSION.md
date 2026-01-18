# Browser-Version - Schnellstart

Die einfachste Möglichkeit, PDFs mit Rechnungen zu trennen!

## ✨ Vorteile

- ✅ **Keine Installation** - Einfach HTML-Datei öffnen
- ✅ **Offline-fähig** - Funktioniert ohne Internetverbindung
- ✅ **Datenschutz** - Alle Daten bleiben auf Ihrem Computer
- ✅ **Plattformunabhängig** - Windows, Mac, Linux
- ✅ **Keine Programmierung** - Sofort einsatzbereit

## 🚀 So starten Sie

1. **Datei öffnen**
   - Doppelklicken Sie auf `browser-app.html`
   - ODER: Rechtsklick → "Öffnen mit" → Ihr Browser

2. **PDF hochladen**
   - Ziehen Sie eine PDF-Datei in das Fenster (Drag & Drop)
   - ODER: Klicken Sie auf das Upload-Feld

3. **Rechnungen werden automatisch erkannt**
   - Die App zeigt alle erkannten Rechnungen an
   - Mit Seitenzahlen und erkannten Rechnungsnummern

4. **PDF teilen**
   - Klicken Sie auf "PDF jetzt teilen"
   - Warten Sie kurz auf die Verarbeitung

5. **Downloads**
   - Laden Sie einzelne PDFs herunter
   - ODER: Alle als ZIP-Archiv herunterladen

## 🔍 Was wird erkannt?

Die App erkennt Rechnungen automatisch anhand von:

- **Schlüsselwörtern**: "Rechnung", "Invoice", "Rechnungsnummer", etc.
- **Nummernmustern**: "2024-001", "RE-12345", "INV20240001", etc.
- **Leerseiten**: Werden als Trenner zwischen Dokumenten erkannt
- **Mehrsprachig**: Deutsch, Englisch, Französisch

## 📊 Mehrseitige Rechnungen

Die App gruppiert zusammengehörige Seiten automatisch:

- Eine Rechnung kann beliebig viele Seiten umfassen
- Fortsetzungsseiten werden automatisch erkannt
- Leerseiten trennen verschiedene Rechnungen

## 💡 Tipps

### Beste Ergebnisse erzielen:

1. **Rechnungsnummern**: Stellen Sie sicher, dass jede Rechnung eine Nummer hat
2. **Leerseiten**: Fügen Sie zwischen Rechnungen eine Leerseite ein (optional)
3. **Qualität**: Verwenden Sie gut lesbare PDFs (keine Scans mit schlechter Qualität)

### Browser-Kompatibilität:

Die App funktioniert am besten mit modernen Browsern:
- ✅ Chrome / Chromium (empfohlen)
- ✅ Firefox
- ✅ Edge
- ✅ Safari
- ⚠️ Internet Explorer wird NICHT unterstützt

## ⚙️ Technische Details

Die App verwendet folgende Bibliotheken (werden automatisch geladen):

- **PDF.js**: Zum Lesen und Analysieren von PDFs
- **pdf-lib**: Zum Erstellen neuer PDFs
- **JSZip**: Zum Erstellen von ZIP-Archiven

Alle werden über CDN geladen - Sie benötigen beim ersten Start eine Internetverbindung.

## 🔒 Datenschutz

**100% Privat und sicher:**

- Alle PDFs werden NUR in Ihrem Browser verarbeitet
- Es werden KEINE Daten an einen Server gesendet
- Es werden KEINE Daten gespeichert (außer Ihre Downloads)
- Der Code ist Open Source - Sie können ihn überprüfen

## 🆘 Probleme?

### PDF wird nicht erkannt
- Prüfen Sie, ob die Datei wirklich ein PDF ist
- Versuchen Sie, das PDF zu reparieren oder neu zu speichern

### Rechnungen werden nicht korrekt erkannt
- Fügen Sie Leerseiten zwischen Rechnungen ein
- Stellen Sie sicher, dass Rechnungsnummern vorhanden sind

### Browser-Fehler
- Aktualisieren Sie Ihren Browser auf die neueste Version
- Versuchen Sie einen anderen Browser
- Öffnen Sie die Browser-Konsole (F12) für Fehlermeldungen

### Zu große PDFs
- Die Browser-Version kann große PDFs (>100MB) verlangsamen
- Für sehr große Dateien nutzen Sie die Server-Version

## 📝 Beispiel-Workflow

```
1. Öffne browser-app.html
   ↓
2. Lade "rechnungen_2024.pdf" hoch
   ↓
3. App erkennt: 15 Rechnungen (je 1-3 Seiten)
   ↓
4. Klicke "PDF teilen"
   ↓
5. Lade alle als ZIP herunter
   ↓
6. Fertig! 15 einzelne PDF-Dateien
```

## 🎯 Nächste Schritte

- Testen Sie die App mit Ihren eigenen PDFs
- Bei Problemen: Siehe Troubleshooting oben
- Für erweiterte Funktionen: Nutzen Sie die Server-Version (siehe README.md)

---

**Viel Erfolg beim Trennen Ihrer Rechnungen!** 🎉
