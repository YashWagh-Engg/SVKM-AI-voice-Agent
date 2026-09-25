def detect_intent(message: str) -> str:
    text = message.lower().strip()

    # ---------------------------------------------------------
    # INTAKE / SEAT QUESTIONS
    # ---------------------------------------------------------

    intake_keywords = [
        "intake",
        "how many seats",
        "how many seat",
        "seat",
        "seats",
        "capacity",
        "कितनी सीट",
        "कितने सीट",
        "जागा",
        "जागा किती",
        "सीट",
        "सीट्स"
    ]

    if any(keyword in text for keyword in intake_keywords):

        # All-branch / all-program requests
        if (
            "all branch" in text
            or "all branches" in text
            or "all program" in text
            or "all programs" in text
            or "all courses" in text
            or "सभी शाखा" in text
            or "सभी प्रोग्राम" in text
            or "सर्व शाखा" in text
            or "सर्व कार्यक्रम" in text
        ):
            return "all_branch_intakes"

        # Pharmacy-specific intake
        pharmacy_keywords = [
            "pharmacy",
            "pharma",
            "d.pharm",
            "d pharm",
            "b.pharm",
            "b pharm",
            "b.pharm + mba",
            "b pharm mba",
            "pharm d",
            "m.pharm",
            "m pharm",
            "cosmetic technology",
            "pharmaceutical"
        ]

        if any(keyword in text for keyword in pharmacy_keywords):
            return "pharmacy_intake"

        # Commerce-specific intake
        commerce_keywords = [
            "bba",
            "bca",
            "commerce",
            "school of commerce"
        ]

        if any(keyword in text for keyword in commerce_keywords):
            return "program_intake"

        # General program / postgraduate intake
        program_keywords = [
            "mca",
            "m.tech",
            "m tech",
            "computer engineering",
            "data science",
            "ai and ml",
            "ai & ml",
            "artificial intelligence",
            "machine learning",
            "civil engineering",
            "electrical engineering",
            "information technology",
            "information tech",
            "mechanical engineering",
            "mechanical"
        ]

        if any(keyword in text for keyword in program_keywords):
            return "program_intake"

        # If only "seat/intake" was asked without identifying a program
        return "program_intake"

    # ---------------------------------------------------------
    # LOCATION
    # ---------------------------------------------------------

    if any(keyword in text for keyword in [
        "where is the college",
        "where is the university",
        "location",
        "located",
        "address",
        "कहाँ",
        "कहां",
        "पता",
        "स्थान",
        "कुठे",
        "ठिकाण"
    ]):
        return "college_location"

    # ---------------------------------------------------------
    # ENGINEERING BRANCHES
    # ---------------------------------------------------------

    if any(keyword in text for keyword in [
        "engineering branches",
        "engineering branch",
        "branches",
        "branch",
        "शाखाएं",
        "शाखा",
        "शाखा",
        "शाखा"
    ]):
        return "engineering_branches"

    # ---------------------------------------------------------
    # COLLEGE INTRODUCTION
    # ---------------------------------------------------------

    if any(keyword in text for keyword in [
        "tell me about the college",
        "tell me about the university",
        "about the college",
        "about the university",
        "college information",
        "university information",
        "college introduction",
        "university introduction",
        "कॉलेज के बारे में",
        "विश्वविद्यालय के बारे में",
        "महाविद्यालयाबद्दल",
        "विद्यापीठाबद्दल"
    ]):
        return "college_introduction"

    # ---------------------------------------------------------
    # SCHOOLS
    # ---------------------------------------------------------

    if any(keyword in text for keyword in [
        "schools",
        "school",
        "what schools",
        "which schools",
        "school of commerce",
        "school of pharmacy",
        "school of technology",
        "कितने स्कूल",
        "कौन से स्कूल",
        "शाळा",
        "कोणते स्कूल"
    ]):
        return "schools"

    # ---------------------------------------------------------
    # PROGRAMS
    # ---------------------------------------------------------

    if any(keyword in text for keyword in [
        "courses",
        "course",
        "programs",
        "program",
        "what do you offer",
        "what programs",
        "which programs",
        "what courses",
        "कोर्स",
        "पाठ्यक्रम",
        "अभ्यासक्रम"
    ]):
        return "programs"

    # ---------------------------------------------------------
    # FACILITIES
    # ---------------------------------------------------------

    if any(keyword in text for keyword in [
        "facilities",
        "facility",
        "campus facilities",
        "campus",
        "सुविधाएं",
        "सुविधा",
        "सुविधा आहेत",
        "सुविधा आहेत का"
    ]):
        return "facilities"

    # ---------------------------------------------------------
    # HOSTEL
    # ---------------------------------------------------------

    if any(keyword in text for keyword in [
        "hostel",
        "accommodation",
        "stay",
        "वसतिगृह",
        "छात्रावास"
    ]):
        return "hostel"

    # ---------------------------------------------------------
    # LIBRARY
    # ---------------------------------------------------------

    if any(keyword in text for keyword in [
        "library",
        "books",
        "ग्रंथालय",
        "पुस्तकालय"
    ]):
        return "library"

    # ---------------------------------------------------------
    # SPORTS
    # ---------------------------------------------------------

    if any(keyword in text for keyword in [
        "sports",
        "playground",
        "games",
        "क्रीड़ा",
        "खेल"
    ]):
        return "sports"

    # ---------------------------------------------------------
    # PLACEMENTS
    # ---------------------------------------------------------

    if any(keyword in text for keyword in [
        "placement",
        "placements",
        "job",
        "jobs",
        "career",
        "नौकरी",
        "प्लेसमेंट",
        "रोजगार"
    ]):
        return "placements"

    # ---------------------------------------------------------
    # RESEARCH
    # ---------------------------------------------------------

    if any(keyword in text for keyword in [
        "research",
        "innovation",
        "research facilities",
        "संशोधन",
        "अनुसंधान"
    ]):
        return "research"

    # ---------------------------------------------------------
    # CONTACT
    # ---------------------------------------------------------

    if any(keyword in text for keyword in [
        "contact",
        "phone number",
        "telephone",
        "email",
        "फोन",
        "संपर्क",
        "ईमेल"
    ]):
        return "contact"

    # ---------------------------------------------------------
    # WEBSITE
    # ---------------------------------------------------------

    if any(keyword in text for keyword in [
        "website",
        "web site",
        "official website",
        "वेबसाइट"
    ]):
        return "website"

    return "unknown"