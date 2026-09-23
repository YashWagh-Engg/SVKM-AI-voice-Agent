def detect_language(text: str) -> str:
    """
    Basic language detection for English, Marathi and Hindi.
    Marathi/Hindi both use Devanagari, so common Marathi words
    are checked first.
    """

    text = text.lower().strip()

    marathi_words = [
        "कुठे", "आहे", "आहेत", "महाविद्यालय", "विद्यापीठ",
        "शाखा", "माहिती", "कसे", "काय", "मध्ये", "पासून",
        "उपलब्ध", "वसतिगृह", "ग्रंथालय"
    ]

    hindi_words = [
        "कहाँ", "है", "हैं", "कॉलेज", "विश्वविद्यालय",
        "शाखा", "जानकारी", "कैसे", "क्या", "में",
        "उपलब्ध", "छात्रावास", "पुस्तकालय"
    ]

    if any(word in text for word in marathi_words):
        return "mr"

    if any(word in text for word in hindi_words):
        return "hi"

    return "en"