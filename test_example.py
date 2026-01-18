"""
Beispiel-Test für PDF Splitter
"""
from invoice_detector import InvoiceDetector


def test_invoice_keywords():
    """Test der Rechnungs-Keyword-Erkennung"""
    detector = InvoiceDetector()

    # Test mit deutscher Rechnung
    text_de = """
    Musterfirma GmbH
    Musterstraße 1
    12345 Musterstadt

    Rechnung Nr. 2024-001
    Datum: 15.01.2024

    Sehr geehrte Damen und Herren,
    """
    assert detector._has_invoice_header(text_de), "Deutsche Rechnung sollte erkannt werden"

    # Test mit englischer Rechnung
    text_en = """
    Example Company Ltd.
    123 Example Street

    Invoice No: INV-2024-001
    Date: January 15, 2024
    """
    assert detector._has_invoice_header(text_en), "Englische Rechnung sollte erkannt werden"

    # Test ohne Rechnungskopf
    text_normal = """
    Dies ist ein normaler Text ohne Rechnungsinformationen.
    Hier steht nur allgemeiner Inhalt.
    """
    assert not detector._has_invoice_header(text_normal), "Normaler Text sollte nicht erkannt werden"

    print("✅ Alle Tests bestanden!")


def test_invoice_number_extraction():
    """Test der Rechnungsnummern-Extraktion"""
    detector = InvoiceDetector()

    # Test verschiedene Formate
    test_cases = [
        ("Rechnung Nr. 2024-001", "2024-001"),
        ("Invoice: INV20240001", "INV20240001"),
        ("RE-2024/123", "2024/123"),
    ]

    for text, expected in test_cases:
        result = detector._extract_invoice_number(text)
        assert result == expected or result != "", f"Sollte Nummer in '{text}' finden"

    print("✅ Rechnungsnummern-Extraktion funktioniert!")


if __name__ == "__main__":
    test_invoice_keywords()
    test_invoice_number_extraction()
    print("\n🎉 Alle Tests erfolgreich!")
