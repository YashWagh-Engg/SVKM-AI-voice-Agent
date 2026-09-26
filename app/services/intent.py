import re
import unicodedata


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(text: str) -> str:
    """
    Normalize text coming from ElevenLabs/STT.

    Supports:
    - English
    - Hindi
    - Marathi
    - Devanagari Unicode
    """

    if not text:
        return ""

    text = unicodedata.normalize("NFKC", text)
    text = text.casefold()

    # Normalize common separators.
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Keep Unicode letters/numbers and useful symbols.
    text = re.sub(
        r"[^\w\s\u0900-\u097F&+.-]",
        " ",
        text
    )

    # Normalize repeated whitespace.
    text = re.sub(r"\s+", " ", text).strip()

    return text


def contains_any(text: str, keywords: list[str]) -> bool:
    """
    Returns True if any keyword/phrase exists in text.
    """
    return any(keyword in text for keyword in keywords)


# =========================================================
# MAIN INTENT DETECTOR
# =========================================================

def detect_intent(message: str) -> str:

    text = normalize_text(message)

    if not text:
        return "unknown"

    # =====================================================
    # 1. ALL PROGRAM INTAKES
    # =====================================================

    if contains_any(text, [
        "all programs seats",
        "all program seats",
        "all programs intake",
        "all program intake",
        "all courses seats",
        "all courses intake",

        "सभी प्रोग्राम की सीट",
        "सभी कार्यक्रम की सीट",
        "सर्व कार्यक्रमांच्या जागा",
        "सर्व अभ्यासक्रमांच्या जागा",
        "सर्व कार्यक्रमांचा intake",
        "सर्व कार्यक्रमांची माहिती",
    ]):
        return "all_program_intakes"

    # =====================================================
    # 2. ALL ENGINEERING BRANCH INTAKES
    # =====================================================

    if contains_any(text, [
        "all engineering branches",
        "all engineering branch",
        "all engineering seats",
        "all engineering intake",
        "all branch seats",
        "all branch intake",

        "सभी इंजीनियरिंग शाखाओं की सीट",
        "सभी इंजीनियरिंग शाखाओं का intake",
        "सर्व इंजिनिअरिंग शाखांच्या जागा",
        "सर्व शाखांच्या जागा",
        "सर्व इंजिनिअरिंग शाखांचा intake",
    ]):
        return "all_branch_intakes"

    # =====================================================
    # 3. INTAKE / SEAT QUESTIONS
    #
    # IMPORTANT:
    # Specific programs are checked BEFORE broad
    # Pharmacy / Commerce / Engineering categories.
    # =====================================================

    intake_keywords = [
        "intake",
        "how many seats",
        "how many seat",
        "number of seats",
        "number of seat",
        "seat",
        "seats",
        "capacity",
        "allocated seats",
        "seat allocation",

        "कितनी सीट",
        "कितने सीट",
        "सीट कितनी",
        "सीट्स कितनी",
        "कितनी सीटें",
        "कितने सीटें",

        "जागा किती",
        "जागा",
        "जागा आहेत",
        "किती जागा",
        "किती जागा आहेत",

        "सीट",
        "सीट्स",
        "सीट किती",
        "सीट्स किती",

        "अलोकेटेड सीट",
        "अलोकेटेड सीट्स",
        "प्रवेश क्षमता",

        "kitni seat",
        "kitne seat",
        "seat kitni",
        "seats kitni",
        "kitni seats",
        "kitne seats",
    ]

    if contains_any(text, intake_keywords):

        # -------------------------------------------------
        # 3A. COSMETIC TECHNOLOGY
        #
        # Must come BEFORE broad pharmacy detection because
        # Cosmetic Technology belongs to the Pharmacy school
        # but is a separate program.
        # -------------------------------------------------

        cosmetic_keywords = [
            "b.tech cosmetic",
            "b tech cosmetic",
            "b-tech cosmetic",
            "btech cosmetic",

            "b.tech cosmetic technology",
            "b tech cosmetic technology",
            "btech cosmetic technology",

            "cosmetic technology",
            "cosmetic tech",

            "cosmetology",
            "costology",
            "cosmatic",

            "b tech costology",
            "b.tech costology",
            "btech costology",

            "b tech cosmetology",
            "b.tech cosmetology",
            "btech cosmetology",

            "b tech cosmatic",
            "b.tech cosmatic",
            "btech cosmatic",

            "बीटेक कॉस्मेटिक",
            "बी टेक कॉस्मेटिक",
            "बीटेक कॉस्मेटिक टेक्नॉलॉजी",
            "बी टेक कॉस्मेटिक टेक्नॉलॉजी",
            "बीटेक कॉस्मेटिक टेक्नोलॉजी",
            "बी टेक कॉस्मेटिक टेक्नोलॉजी",

            "कॉस्मेटिक टेक्नॉलॉजी",
            "कॉस्मेटिक टेक्नोलॉजी",
            "कॉस्मेटिक टेक",
        ]

        if contains_any(text, cosmetic_keywords):
            return "program_intake"

        # -------------------------------------------------
        # 3B. B.Pharm
        # -------------------------------------------------

        bpharm_keywords = [
            "b.pharm",
            "b pharm",
            "b-pharm",
            "bpharm",

            "b pharmacy",
            "b-pharmacy",
            "bpharmacy",

            "b pharma",
            "b-pharma",
            "bpharma",

            "बी फार्म",
            "बी फार्मसी",
            "बी फार्मेसी",
            "बी फार्मा",

            "be pharm",
            "be pharmacy",
            "be pharma",
            "bee pharm",
            "bee pharmacy",
        ]

        # -------------------------------------------------
        # 3C. D.Pharm
        # -------------------------------------------------

        dpharm_keywords = [
            "d.pharm",
            "d pharm",
            "d-pharm",
            "dpharm",

            "d pharmacy",
            "d-pharmacy",
            "dpharmacy",

            "d pharma",
            "d-pharma",
            "dpharma",

            "डी फार्म",
            "डी फार्मसी",
            "डी फार्मेसी",
            "डी फार्मा",

            "dee pharm",
            "dee pharmacy",
        ]

        # -------------------------------------------------
        # 3D. B.Pharm + MBA
        # -------------------------------------------------

        bpharm_mba_keywords = [
            "b.pharm + mba",
            "b pharm + mba",
            "b-pharm + mba",
            "bpharm + mba",

            "b.pharm mba",
            "b pharm mba",
            "b-pharm mba",
            "bpharm mba",

            "b pharmacy mba",
            "b-pharmacy mba",
            "b pharma mba",

            "pharmacy plus mba",
            "pharmacy and mba",
            "pharm plus mba",
            "pharm mba",

            "बी फार्म एमबीए",
            "बी फार्मसी एमबीए",
            "बी फार्मेसी एमबीए",
            "फार्मसी प्लस एमबीए",
            "फार्मेसी आणि एमबीए",
        ]

        if contains_any(text, bpharm_mba_keywords):
            return "pharmacy_intake"

        if contains_any(text, bpharm_keywords):
            return "pharmacy_intake"

        if contains_any(text, dpharm_keywords):
            return "pharmacy_intake"

        # -------------------------------------------------
        # 3E. OTHER PHARMACY PROGRAMS
        # -------------------------------------------------

        pharmacy_keywords = [
            "pharmacy",
            "pharma",
            "pharm",

            "m.pharm",
            "m pharm",
            "m-pharm",
            "mpharm",

            "m pharmacy",
            "m-pharmacy",
            "mpharmacy",

            "pharmacy department",
            "school of pharmacy",

            "फार्मसी",
            "फार्मेसी",
            "फार्मसी विभाग",
            "फार्मेसी विभाग",
        ]

        if contains_any(text, pharmacy_keywords):
            return "pharmacy_intake"

        # -------------------------------------------------
        # 3F. COMMERCE PROGRAMS
        # -------------------------------------------------

        commerce_keywords = [
            "bba",
            "b.b.a",
            "b b a",

            "bca",
            "b.c.a",
            "b c a",

            "commerce",
            "school of commerce",

            "बीबीए",
            "बी बी ए",

            "बीसीए",
            "बी सी ए",

            "कॉमर्स",
            "वाणिज्य",
        ]

        if contains_any(text, commerce_keywords):
            return "program_intake"

        # -------------------------------------------------
        # 3G. EVERYTHING ELSE
        # -------------------------------------------------

        return "program_intake"

    # =====================================================
    # 4. ELIGIBILITY
    # =====================================================

    eligibility_keywords = [
        "eligibility",
        "eligible",
        "eligibility criteria",
        "criteria for admission",
        "admission criteria",
        "who can apply",
        "can i apply",
        "qualification required",
        "qualification needed",
        "required qualification",
        "requirements for admission",
        "admission requirement",

        "पात्रता",
        "पात्र कौन",
        "कौन पात्र",
        "प्रवेश पात्रता",
        "प्रवेशासाठी पात्रता",
        "शैक्षणिक पात्रता",
        "अर्हता",
        "प्रवेशाची पात्रता",

        "पात्र कोण आहे",
        "पात्र कोण आहेत",
    ]

    if contains_any(text, eligibility_keywords):
        return "program_eligibility"

    # =====================================================
    # 5. DURATION
    # =====================================================

    duration_keywords = [
        "duration",
        "how many years",
        "how long",
        "years course",
        "course duration",
        "program duration",

        "कितने साल",
        "कितने वर्ष",
        "किती वर्ष",
        "किती वर्षे",
        "कालावधी",
        "अभ्यासक्रम किती वर्ष",
        "कोर्स किती वर्ष",
        "प्रोग्राम किती वर्ष",
    ]

    if contains_any(text, duration_keywords):
        return "program_duration"

    # =====================================================
    # 6. PROGRAM INFORMATION
    # =====================================================

    program_info_keywords = [
        "tell me about",
        "information about",
        "information on",
        "details about",
        "details of",
        "about this program",
        "about this course",
        "program information",
        "course information",

        "what is b pharm",
        "what is b pharmacy",
        "what is bba",
        "what is bca",
        "what is mca",
        "what is d pharm",
        "what is dpharm",
        "what is cosmetic",

        "बद्दल माहिती",
        "बद्दल थोडी माहिती",
        "माहिती द्या",
        "माहिती हवी",
        "माहिती पाहिजे",

        "जानकारी",
        "जानकारी चाहिए",
        "के बारे में",
        "के बारे मे",
        "थोड़ी जानकारी",
        "थोड़ी सी जानकारी",
    ]

    if contains_any(text, program_info_keywords):
        return "program_information"

    # =====================================================
    # 7. PHARMACY SCHOOL / PROGRAM LIST
    # =====================================================

    if contains_any(text, [
        "pharmacy department",
        "pharmacy school",
        "pharmacy programs",
        "pharmacy courses",
        "school of pharmacy",
        "pharmacy department information",

        "फार्मसी विभाग",
        "फार्मेसी विभाग",
        "फार्मसीचे कार्यक्रम",
        "फार्मेसीचे कार्यक्रम",
        "फार्मेसी के कार्यक्रम",
    ]):
        return "pharmacy_programs"

    # =====================================================
    # 8. COMMERCE SCHOOL
    # =====================================================

    if contains_any(text, [
        "school of commerce",
        "commerce school",
        "commerce department",
        "commerce programs",
        "commerce courses",

        "कॉमर्स विभाग",
        "वाणिज्य विभाग",
        "कॉमर्सचे कार्यक्रम",
        "वाणिज्य कार्यक्रम",
    ]):
        return "commerce_programs"

    # =====================================================
    # 9. ENGINEERING BRANCHES
    # =====================================================

    if contains_any(text, [
        "engineering branches",
        "engineering branch",
        "which engineering branches",
        "what engineering branches",
        "branches available",
        "available branches",
        "engineering courses",
        "engineering programs",

        "इंजीनियरिंग शाखा",
        "इंजीनियरिंग शाखाएं",
        "इंजिनिअरिंग शाखा",
        "इंजिनिअरिंगच्या शाखा",
        "इंजिनिअरिंगच्या कोणत्या शाखा",
        "इंजीनियरिंग की शाखाएं",
    ]):
        return "engineering_branches"

    # =====================================================
    # 10. COLLEGE INTRODUCTION
    # =====================================================

    if contains_any(text, [
        "tell me about the college",
        "tell me about the university",
        "about the college",
        "about the university",
        "college information",
        "university information",
        "college introduction",
        "university introduction",
        "college overview",
        "university overview",

        "कॉलेज के बारे में",
        "विश्वविद्यालय के बारे में",
        "महाविद्यालयाबद्दल",
        "विद्यापीठाबद्दल",
        "कॉलेज बद्दल",
        "कॉलेजविषयी",
        "विद्यापीठाविषयी",
    ]):
        return "college_introduction"

    # =====================================================
    # 11. LOCATION
    # =====================================================

    if contains_any(text, [
        "where is the college",
        "where is the university",
        "where is college",
        "where is university",
        "location",
        "located",
        "address",
        "where are you located",

        "कहाँ है",
        "कहां है",
        "पता",
        "स्थान",

        "कुठे आहे",
        "कुठे",
        "पत्ता",
        "ठिकाण",
    ]):
        return "college_location"

    # =====================================================
    # 12. SCHOOLS
    # =====================================================

    if contains_any(text, [
        "schools",
        "school",
        "what schools",
        "which schools",
        "schools available",

        "कितने स्कूल",
        "कौन से स्कूल",

        "शाळा",
        "कोणते स्कूल",
        "कोणत्या शाळा",
    ]):
        return "schools"

    # =====================================================
    # 13. GENERAL PROGRAMS
    # =====================================================

    if contains_any(text, [
        "programs",
        "program",
        "courses",
        "course",
        "what do you offer",
        "what programs",
        "which programs",
        "what courses",
        "available programs",
        "available courses",

        "कोर्स",
        "कोर्सेस",
        "प्रोग्राम",
        "प्रोग्राम्स",
        "अभ्यासक्रम",
        "अभ्यासक्रम कोणते",
    ]):
        return "programs"

    # =====================================================
    # 14. FACILITIES
    # =====================================================

    if contains_any(text, [
        "facilities",
        "facility",
        "campus facilities",
        "campus facility",
        "what facilities",
        "available facilities",

        "सुविधाएं",
        "सुविधा",
        "सुविधा आहेत",
        "सुविधा कोणत्या",
        "कॅम्पसच्या सुविधा",
        "कॅम्पसमध्ये कोणत्या सुविधा",
    ]):
        return "facilities"

    # =====================================================
    # 15. LIBRARY
    # =====================================================

    if contains_any(text, [
        "library",
        "libraries",
        "books",
        "digital library",
        "library resources",

        "ग्रंथालय",
        "पुस्तकालय",
        "लायब्ररी",
        "लायब्ररीबद्दल",
        "लायब्ररी बद्दल",
    ]):
        return "library"

    # =====================================================
    # 16. HOSTEL
    # =====================================================

    if contains_any(text, [
        "hostel",
        "hostels",
        "accommodation",
        "stay",
        "hostel facility",
        "hostel facilities",

        "वसतिगृह",
        "छात्रावास",
        "हॉस्टेल",
        "हॉस्टेल सुविधा",
    ]):
        return "hostel"

    # =====================================================
    # 17. SPORTS
    # =====================================================

    if contains_any(text, [
        "sports",
        "sport facility",
        "sports facilities",
        "playground",
        "games",

        "क्रीडा",
        "खेळ",
        "स्पोर्ट्स",
        "क्रीडा सुविधा",
    ]):
        return "sports"

    # =====================================================
    # 18. PLACEMENTS
    # =====================================================

    if contains_any(text, [
        "placement",
        "placements",
        "job",
        "jobs",
        "career",
        "placement support",
        "placement assistance",

        "नौकरी",
        "प्लेसमेंट",
        "रोजगार",
        "करिअर",
        "नोकरी",
    ]):
        return "placements"

    # =====================================================
    # 19. RESEARCH
    # =====================================================

    if contains_any(text, [
        "research",
        "research facilities",
        "research department",
        "innovation",
        "research work",
        "patent",
        "research grant",

        "संशोधन",
        "अनुसंधान",
        "रिसर्च",
        "संशोधन सुविधा",
        "पेटंट",
    ]):
        return "research"

    # =====================================================
    # 20. CONTACT
    # =====================================================

    if contains_any(text, [
        "contact",
        "contact number",
        "phone number",
        "phone",
        "telephone",
        "email",
        "admission contact",
        "contact details",

        "फोन",
        "मोबाइल नंबर",
        "संपर्क",
        "ईमेल",
        "पत्ता आणि फोन",
    ]):
        return "contact"

    # =====================================================
    # 21. WEBSITE
    # =====================================================

    if contains_any(text, [
        "website",
        "web site",
        "official website",
        "college website",
        "university website",
        "site",

        "वेबसाइट",
        "वेब साइट",
        "आधिकारिक वेबसाइट",
        "कॉलेजची वेबसाइट",
        "विद्यापीठाची वेबसाइट",
    ]):
        return "website"

    # =====================================================
    # 22. UNKNOWN
    # =====================================================

    return "unknown"