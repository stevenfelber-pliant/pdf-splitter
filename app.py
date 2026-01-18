"""
Flask Web-Server für PDF Splitter
"""
import os
import uuid
from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from pdf_processor import PDFProcessor
import shutil

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# Erstelle notwendige Verzeichnisse
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

processor = PDFProcessor(output_dir=app.config['OUTPUT_FOLDER'])


@app.route('/')
def index():
    """Haupt-Seite"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload und Analyse einer PDF-Datei"""
    if 'file' not in request.files:
        return jsonify({'error': 'Keine Datei hochgeladen'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Keine Datei ausgewählt'}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Nur PDF-Dateien erlaubt'}), 400

    try:
        # Speichere Datei mit eindeutigem Namen
        unique_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
        file.save(file_path)

        # Analysiere PDF
        analysis = processor.analyze_pdf(file_path)

        return jsonify({
            'success': True,
            'file_id': unique_id,
            'filename': filename,
            'analysis': analysis
        })

    except Exception as e:
        return jsonify({'error': f'Fehler beim Verarbeiten: {str(e)}'}), 500


@app.route('/api/split', methods=['POST'])
def split_pdf():
    """Teilt ein hochgeladenes PDF"""
    data = request.get_json()
    file_id = data.get('file_id')
    filename = data.get('filename')

    if not file_id or not filename:
        return jsonify({'error': 'Fehlende Parameter'}), 400

    try:
        # Finde hochgeladene Datei
        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'],
            f"{file_id}_{secure_filename(filename)}"
        )

        if not os.path.exists(file_path):
            return jsonify({'error': 'Datei nicht gefunden'}), 404

        # Erstelle Output-Verzeichnis für diese Session
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], file_id)
        os.makedirs(output_dir, exist_ok=True)

        # Temporär den Output-Ordner des Processors ändern
        original_output = processor.output_dir
        processor.output_dir = output_dir

        # Teile PDF
        base_name = os.path.splitext(filename)[0]
        results = processor.split_pdf(file_path, output_prefix=base_name)

        # Stelle Original-Output wieder her
        processor.output_dir = original_output

        return jsonify({
            'success': True,
            'results': results,
            'download_id': file_id
        })

    except Exception as e:
        return jsonify({'error': f'Fehler beim Teilen: {str(e)}'}), 500


@app.route('/api/download/<file_id>/<filename>')
def download_file(file_id, filename):
    """Download einer geteilten PDF"""
    try:
        file_path = os.path.join(
            app.config['OUTPUT_FOLDER'],
            file_id,
            secure_filename(filename)
        )

        if not os.path.exists(file_path):
            return jsonify({'error': 'Datei nicht gefunden'}), 404

        return send_file(file_path, as_attachment=True, download_name=filename)

    except Exception as e:
        return jsonify({'error': f'Fehler beim Download: {str(e)}'}), 500


@app.route('/api/download-all/<file_id>')
def download_all(file_id):
    """Download aller geteilten PDFs als ZIP"""
    try:
        import zipfile
        from io import BytesIO

        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], file_id)

        if not os.path.exists(output_dir):
            return jsonify({'error': 'Keine Dateien gefunden'}), 404

        # Erstelle ZIP im Speicher
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filename in os.listdir(output_dir):
                if filename.endswith('.pdf'):
                    file_path = os.path.join(output_dir, filename)
                    zf.write(file_path, filename)

        memory_file.seek(0)

        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'invoices_{file_id}.zip'
        )

    except Exception as e:
        return jsonify({'error': f'Fehler beim Erstellen des ZIP: {str(e)}'}), 500


@app.route('/api/cleanup/<file_id>', methods=['POST'])
def cleanup(file_id):
    """Löscht temporäre Dateien"""
    try:
        # Lösche Upload
        upload_dir = app.config['UPLOAD_FOLDER']
        for filename in os.listdir(upload_dir):
            if filename.startswith(file_id):
                os.remove(os.path.join(upload_dir, filename))

        # Lösche Output
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], file_id)
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'error': f'Fehler beim Aufräumen: {str(e)}'}), 500


if __name__ == '__main__':
    print("🚀 PDF Splitter startet...")
    print("📍 Öffnen Sie http://localhost:5000 im Browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
