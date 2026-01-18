"""
PDF-Verarbeitung und Splitting-Funktionalität
"""
import os
from typing import List, Tuple
from pypdf import PdfReader, PdfWriter
from invoice_detector import InvoiceDetector


class PDFProcessor:
    """Verarbeitet und teilt PDF-Dateien nach Rechnungen"""

    def __init__(self, output_dir: str = "output"):
        """
        Args:
            output_dir: Verzeichnis für geteilte PDFs
        """
        self.output_dir = output_dir
        self.detector = InvoiceDetector()
        os.makedirs(output_dir, exist_ok=True)

    def split_pdf(self, pdf_path: str, output_prefix: str = "invoice") -> List[dict]:
        """
        Teilt ein PDF nach erkannten Rechnungen

        Args:
            pdf_path: Pfad zum Input-PDF
            output_prefix: Präfix für Output-Dateien

        Returns:
            Liste von Dicts mit Informationen über geteilte PDFs
        """
        # Erkenne Rechnungsgrenzen
        invoices = self.detector.detect_invoices(pdf_path)

        # Teile PDF
        results = []
        for idx, (start_page, end_page) in enumerate(invoices, 1):
            output_path = self._split_pages(
                pdf_path,
                start_page,
                end_page,
                f"{output_prefix}_{idx:03d}.pdf"
            )

            # Extrahiere Informationen über die erste Seite
            invoice_info = self.detector.get_invoice_info(pdf_path, start_page)

            results.append({
                'invoice_number': idx,
                'output_file': os.path.basename(output_path),
                'output_path': output_path,
                'start_page': start_page + 1,  # 1-basiert für Anzeige
                'end_page': end_page + 1,
                'page_count': end_page - start_page + 1,
                'detected_invoice_number': invoice_info.get('invoice_number', ''),
                'has_header': invoice_info.get('has_invoice_header', False)
            })

        return results

    def _split_pages(self, input_path: str, start_page: int, end_page: int, output_filename: str) -> str:
        """
        Extrahiert Seiten aus einem PDF

        Args:
            input_path: Input PDF
            start_page: Start-Seite (0-basiert)
            end_page: End-Seite (0-basiert, inklusiv)
            output_filename: Name der Output-Datei

        Returns:
            Pfad zur erstellten Datei
        """
        reader = PdfReader(input_path)
        writer = PdfWriter()

        # Füge Seiten hinzu
        for page_num in range(start_page, end_page + 1):
            if page_num < len(reader.pages):
                writer.add_page(reader.pages[page_num])

        # Speichere Output
        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        return output_path

    def get_pdf_info(self, pdf_path: str) -> dict:
        """Gibt Informationen über ein PDF zurück"""
        reader = PdfReader(pdf_path)
        invoices = self.detector.detect_invoices(pdf_path)

        return {
            'total_pages': len(reader.pages),
            'detected_invoices': len(invoices),
            'invoice_ranges': [
                {
                    'start': start + 1,
                    'end': end + 1,
                    'pages': end - start + 1
                }
                for start, end in invoices
            ]
        }

    def analyze_pdf(self, pdf_path: str) -> dict:
        """
        Analysiert ein PDF und gibt detaillierte Informationen zurück
        (ohne es zu teilen)
        """
        info = self.get_pdf_info(pdf_path)

        # Füge detaillierte Informationen über jede erkannte Rechnung hinzu
        invoices_detail = []
        for idx, invoice_range in enumerate(info['invoice_ranges'], 1):
            # Info von der ersten Seite der Rechnung
            first_page = invoice_range['start'] - 1  # Zurück zu 0-basiert
            invoice_info = self.detector.get_invoice_info(pdf_path, first_page)

            invoices_detail.append({
                'number': idx,
                'start_page': invoice_range['start'],
                'end_page': invoice_range['end'],
                'page_count': invoice_range['pages'],
                'detected_invoice_number': invoice_info.get('invoice_number', ''),
                'has_invoice_header': invoice_info.get('has_invoice_header', False)
            })

        return {
            'total_pages': info['total_pages'],
            'detected_invoices': info['detected_invoices'],
            'invoices': invoices_detail
        }
