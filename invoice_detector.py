"""
Rechnungserkennung mit kombinierter Text- und visueller Analyse
"""
import re
from typing import List, Tuple
import pdfplumber


class InvoiceDetector:
    """Erkennt Rechnungsgrenzen in PDF-Dokumenten"""

    # Typische Rechnungs-Schlüsselwörter (Deutsch)
    INVOICE_KEYWORDS = [
        r'rechnung\s*nr',
        r'invoice\s*no',
        r'rechnungsnummer',
        r're\.\s*nr',
        r'beleg\s*nr',
        r'belegnummer',
        r'faktura',
    ]

    # Muster für Rechnungsnummern
    INVOICE_NUMBER_PATTERNS = [
        r'\b\d{4,}[-/]\d+\b',  # z.B. 2024/001, 2024-001
        r'\bRE[-_]?\d{4,}\b',  # z.B. RE2024001
        r'\b[A-Z]{2,}\d{4,}\b',  # z.B. INV20240001
    ]

    def __init__(self, min_text_threshold: int = 50, blank_page_threshold: int = 20):
        """
        Args:
            min_text_threshold: Mindestanzahl Zeichen für eine Seite mit Inhalt
            blank_page_threshold: Max. Zeichen für eine "leere" Seite
        """
        self.min_text_threshold = min_text_threshold
        self.blank_page_threshold = blank_page_threshold

    def detect_invoices(self, pdf_path: str) -> List[Tuple[int, int]]:
        """
        Erkennt Rechnungsgrenzen im PDF

        Returns:
            Liste von (start_page, end_page) Tupeln (0-basiert)
        """
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            invoice_starts = self._find_invoice_starts(pdf)

            # Wenn keine Rechnungen erkannt wurden, behandle alles als eine Rechnung
            if not invoice_starts:
                return [(0, total_pages - 1)]

            # Erstelle Bereiche: von start bis zum nächsten start - 1
            invoices = []
            for i, start in enumerate(invoice_starts):
                if i < len(invoice_starts) - 1:
                    end = invoice_starts[i + 1] - 1
                else:
                    end = total_pages - 1
                invoices.append((start, end))

            return invoices

    def _find_invoice_starts(self, pdf) -> List[int]:
        """Findet Start-Seiten von Rechnungen"""
        starts = []

        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text() or ""

            # Methode 1: Text-basierte Erkennung
            if self._has_invoice_header(text):
                starts.append(page_num)
                continue

            # Methode 2: Visuelle Erkennung - Leerseite davor
            if page_num > 0 and self._is_likely_start_after_blank(pdf, page_num):
                starts.append(page_num)

        # Erste Seite ist immer ein Start (wenn nicht schon erkannt)
        if 0 not in starts and len(pdf.pages) > 0:
            starts.insert(0, 0)

        return sorted(starts)

    def _has_invoice_header(self, text: str) -> bool:
        """Prüft ob Text einen Rechnungskopf enthält"""
        text_lower = text.lower()

        # Suche nach Rechnungs-Schlüsselwörtern
        for keyword_pattern in self.INVOICE_KEYWORDS:
            if re.search(keyword_pattern, text_lower):
                return True

        # Suche nach Rechnungsnummern-Mustern
        for number_pattern in self.INVOICE_NUMBER_PATTERNS:
            if re.search(number_pattern, text, re.IGNORECASE):
                return True

        return False

    def _is_likely_start_after_blank(self, pdf, page_num: int) -> bool:
        """Prüft ob eine Seite wahrscheinlich nach einer Leerseite startet"""
        if page_num == 0:
            return False

        # Prüfe vorherige Seite
        prev_page = pdf.pages[page_num - 1]
        prev_text = prev_page.extract_text() or ""

        # Aktuelle Seite
        curr_page = pdf.pages[page_num]
        curr_text = curr_page.extract_text() or ""

        # Wenn vorherige Seite fast leer und aktuelle hat viel Inhalt
        prev_is_blank = len(prev_text.strip()) < self.blank_page_threshold
        curr_has_content = len(curr_text.strip()) > self.min_text_threshold

        return prev_is_blank and curr_has_content

    def get_invoice_info(self, pdf_path: str, page_num: int) -> dict:
        """Extrahiert Informationen über eine Rechnung von einer bestimmten Seite"""
        with pdfplumber.open(pdf_path) as pdf:
            if page_num >= len(pdf.pages):
                return {}

            page = pdf.pages[page_num]
            text = page.extract_text() or ""

            info = {
                'has_invoice_header': self._has_invoice_header(text),
                'invoice_number': self._extract_invoice_number(text),
                'page': page_num + 1  # 1-basiert für Anzeige
            }

            return info

    def _extract_invoice_number(self, text: str) -> str:
        """Versucht die Rechnungsnummer zu extrahieren"""
        for pattern in self.INVOICE_NUMBER_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)

        # Fallback: Suche nach "Rechnung" + Nummer
        match = re.search(r'(?:rechnung|invoice).*?(\d{4,}[-/]?\d*)', text, re.IGNORECASE)
        if match:
            return match.group(1)

        return ""
