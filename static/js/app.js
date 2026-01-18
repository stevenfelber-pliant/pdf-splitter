// PDF Splitter - Client-side JavaScript

class PDFSplitter {
    constructor() {
        this.fileData = null;
        this.initElements();
        this.attachEventListeners();
    }

    initElements() {
        // Upload elements
        this.dropZone = document.getElementById('drop-zone');
        this.fileInput = document.getElementById('file-input');

        // Sections
        this.uploadSection = document.getElementById('upload-section');
        this.analysisSection = document.getElementById('analysis-section');
        this.resultsSection = document.getElementById('results-section');
        this.loading = document.getElementById('loading');

        // Buttons
        this.splitBtn = document.getElementById('split-btn');
        this.cancelBtn = document.getElementById('cancel-btn');
        this.downloadAllBtn = document.getElementById('download-all-btn');
        this.newFileBtn = document.getElementById('new-file-btn');
    }

    attachEventListeners() {
        // Drop zone
        this.dropZone.addEventListener('click', () => this.fileInput.click());
        this.dropZone.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.dropZone.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.dropZone.addEventListener('drop', (e) => this.handleDrop(e));

        // File input
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));

        // Buttons
        this.splitBtn.addEventListener('click', () => this.splitPDF());
        this.cancelBtn.addEventListener('click', () => this.reset());
        this.downloadAllBtn.addEventListener('click', () => this.downloadAll());
        this.newFileBtn.addEventListener('click', () => this.reset());
    }

    handleDragOver(e) {
        e.preventDefault();
        this.dropZone.classList.add('drag-over');
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.dropZone.classList.remove('drag-over');
    }

    handleDrop(e) {
        e.preventDefault();
        this.dropZone.classList.remove('drag-over');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    async processFile(file) {
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            alert('Bitte wählen Sie eine PDF-Datei aus.');
            return;
        }

        this.showLoading('Analysiere PDF...');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                this.fileData = data;
                this.showAnalysis(data);
            } else {
                alert('Fehler: ' + data.error);
                this.hideLoading();
            }
        } catch (error) {
            alert('Fehler beim Upload: ' + error.message);
            this.hideLoading();
        }
    }

    showAnalysis(data) {
        this.hideLoading();
        this.uploadSection.classList.add('hidden');
        this.analysisSection.classList.remove('hidden');

        // Zeige Dateiinformationen
        document.getElementById('file-name').textContent = data.filename;
        document.getElementById('total-pages').textContent = data.analysis.total_pages;
        document.getElementById('detected-invoices').textContent = data.analysis.detected_invoices;

        // Zeige erkannte Rechnungen
        const invoiceList = document.getElementById('invoice-list');
        invoiceList.innerHTML = '';

        data.analysis.invoices.forEach((invoice, index) => {
            const item = document.createElement('div');
            item.className = 'invoice-item';

            let invoiceNumber = invoice.detected_invoice_number
                ? `Rechnung ${invoice.detected_invoice_number}`
                : `Rechnung #${invoice.number}`;

            item.innerHTML = `
                <div class="invoice-header">
                    <span class="invoice-number">${invoiceNumber}</span>
                    <span class="invoice-badge">${invoice.page_count} Seite(n)</span>
                </div>
                <div class="invoice-details">
                    <div class="invoice-detail-item">
                        📄 Seiten ${invoice.start_page} - ${invoice.end_page}
                    </div>
                    ${invoice.has_invoice_header ?
                        '<div class="invoice-detail-item">✅ Rechnungskopf erkannt</div>' :
                        '<div class="invoice-detail-item">ℹ️ Kein Rechnungskopf erkannt</div>'
                    }
                </div>
            `;

            invoiceList.appendChild(item);
        });
    }

    async splitPDF() {
        if (!this.fileData) return;

        this.showLoading('Teile PDF...');

        try {
            const response = await fetch('/api/split', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    file_id: this.fileData.file_id,
                    filename: this.fileData.filename
                })
            });

            const data = await response.json();

            if (data.success) {
                this.showResults(data);
            } else {
                alert('Fehler: ' + data.error);
                this.hideLoading();
            }
        } catch (error) {
            alert('Fehler beim Teilen: ' + error.message);
            this.hideLoading();
        }
    }

    showResults(data) {
        this.hideLoading();
        this.analysisSection.classList.add('hidden');
        this.resultsSection.classList.remove('hidden');

        const resultsList = document.getElementById('results-list');
        resultsList.innerHTML = '';

        data.results.forEach((result) => {
            const item = document.createElement('div');
            item.className = 'result-item';

            let displayName = result.detected_invoice_number
                ? `Rechnung ${result.detected_invoice_number}`
                : `Rechnung #${result.invoice_number}`;

            item.innerHTML = `
                <div class="result-info">
                    <h3>${displayName}</h3>
                    <p>${result.output_file} (${result.page_count} Seite(n))</p>
                </div>
                <div class="result-actions">
                    <button class="btn btn-small btn-success" onclick="app.downloadFile('${data.download_id}', '${result.output_file}')">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                            <polyline points="7 10 12 15 17 10"></polyline>
                            <line x1="12" y1="15" x2="12" y2="3"></line>
                        </svg>
                        Download
                    </button>
                </div>
            `;

            resultsList.appendChild(item);
        });

        this.downloadId = data.download_id;
    }

    downloadFile(downloadId, filename) {
        window.location.href = `/api/download/${downloadId}/${filename}`;
    }

    downloadAll() {
        if (this.downloadId) {
            window.location.href = `/api/download-all/${this.downloadId}`;
        }
    }

    async reset() {
        // Cleanup
        if (this.fileData) {
            try {
                await fetch(`/api/cleanup/${this.fileData.file_id}`, {
                    method: 'POST'
                });
            } catch (error) {
                console.error('Cleanup error:', error);
            }
        }

        // Reset state
        this.fileData = null;
        this.downloadId = null;
        this.fileInput.value = '';

        // Show upload section
        this.uploadSection.classList.remove('hidden');
        this.analysisSection.classList.add('hidden');
        this.resultsSection.classList.add('hidden');
        this.hideLoading();
    }

    showLoading(text) {
        document.getElementById('loading-text').textContent = text;
        this.loading.classList.remove('hidden');
    }

    hideLoading() {
        this.loading.classList.add('hidden');
    }
}

// Initialize app
const app = new PDFSplitter();
