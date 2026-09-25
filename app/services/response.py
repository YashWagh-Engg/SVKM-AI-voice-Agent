from .knowledge import load_responses, load_college_info


def normalize_text(text: str) -> str:
    return text.lower().strip()


# ============================================================
# PROGRAM / BRANCH MATCHING
# ============================================================

PROGRAM_ALIASES = {
    # Engineering
    "computer engineering": "Computer Engineering",
    "computer": "Computer Engineering",

    "data science": "Data Science",
    "cse data science": "Data Science",

    "ai and ml": "AI and ML",
    "ai & ml": "AI and ML",
    "artificial intelligence": "AI and ML",
    "machine learning": "AI and ML",

    "civil engineering": "Civil Engineering",
    "civil": "Civil Engineering",

    "electrical engineering": "Electrical Engineering",
    "electrical": "Electrical Engineering",

    "information technology": "Information Technology",
    "information tech": "Information Technology",
    "it": "Information Technology",

    "mechanical engineering": "Mechanical Engineering",
    "mechanical": "Mechanical Engineering",

    # Postgraduate
    "mca": "Master of Computer Applications",
    "master of computer applications": "Master of Computer Applications",

    "m.tech civil": "M.Tech - Civil Engineering",
    "m tech civil": "M.Tech - Civil Engineering",

    "m.tech computer": "M.Tech - Computer Engineering",
    "m tech computer": "M.Tech - Computer Engineering",

    "m.tech electrical": "M.Tech - Electrical Engineering",
    "m tech electrical": "M.Tech - Electrical Engineering",

    "m.tech it": "M.Tech - Information Technology",
    "m tech it": "M.Tech - Information Technology",

    "m.tech mechanical": "M.Tech - Mechanical Engineering",
    "m tech mechanical": "M.Tech - Mechanical Engineering",

    # Commerce
    "bba": "Bachelor of Business Administration",
    "bachelor of business administration": "Bachelor of Business Administration",

    "bca": "Bachelor of Computer Applications",
    "bachelor of computer applications": "Bachelor of Computer Applications",

    # Pharmacy
    "d.pharm": "Diploma in Pharmacy",
    "d pharm": "Diploma in Pharmacy",
    "diploma in pharmacy": "Diploma in Pharmacy",

    "b.pharm + mba": "Bachelor of Pharmacy + MBA (Pharma Tech)",
    "b pharm + mba": "Bachelor of Pharmacy + MBA (Pharma Tech)",
    "b pharm mba": "Bachelor of Pharmacy + MBA (Pharma Tech)",
    "b.pharm mba": "Bachelor of Pharmacy + MBA (Pharma Tech)",

    "b.pharm": "Bachelor of Pharmacy",
    "b pharm": "Bachelor of Pharmacy",
    "bachelor of pharmacy": "Bachelor of Pharmacy",

    "cosmetic technology": "B.Tech - Cosmetic Technology",
    "b.tech cosmetic technology": "B.Tech - Cosmetic Technology",
    "b tech cosmetic technology": "B.Tech - Cosmetic Technology",

    "m.pharm pharmaceutics": "M.Pharm - Pharmaceutics",
    "m pharm pharmaceutics": "M.Pharm - Pharmaceutics",

    "m.pharm pharmaceutical quality assurance":
        "M.Pharm - Pharmaceutical Quality Assurance",

    "m pharm pharmaceutical quality assurance":
        "M.Pharm - Pharmaceutical Quality Assurance",

    "m.pharm pharmacology": "M.Pharm - Pharmacology",
    "m pharm pharmacology": "M.Pharm - Pharmacology",

    "m.pharm pharmaceutical chemistry": "M.Pharm - Pharmaceutical Chemistry",
    "m pharm pharmaceutical chemistry": "M.Pharm - Pharmaceutical Chemistry",

    "ph.d pharmaceutical sciences": "Ph.D. - Pharmaceutical Sciences",
    "phd pharmaceutical sciences": "Ph.D. - Pharmaceutical Sciences"
}


def detect_program(message: str):
    text = normalize_text(message)

    # Longer phrases first so that
    # "B.Pharm + MBA" is detected before "B.Pharm".
    for alias in sorted(PROGRAM_ALIASES.keys(), key=len, reverse=True):
        if alias in text:
            return PROGRAM_ALIASES[alias]

    return None


# ============================================================
# SEARCH PROGRAM IN COLLEGE INFO
# ============================================================

def find_program(program_name: str):
    data = load_college_info()

    programs = data.get("programs", {})

    for school_programs in programs.values():

        if not isinstance(school_programs, list):
            continue

        for program in school_programs:

            if program.get("name") == program_name:
                return program

    return None


# ============================================================
# PROGRAM INTAKE
# ============================================================

def get_program_intake_response(
    message: str,
    language: str = "en"
):
    program_name = detect_program(message)

    # No specific program mentioned
    if program_name is None:

        messages = {
            "en": (
                "Please tell me the specific program you are asking about, "
                "such as B.Pharm, D.Pharm, BBA, BCA, or Computer Engineering."
            ),
            "mr": (
                "कृपया तुम्ही कोणत्या विशिष्ट कार्यक्रमाबद्दल विचारत आहात "
                "ते सांगा, जसे B.Pharm, D.Pharm, BBA, BCA किंवा Computer Engineering."
            ),
            "hi": (
                "कृपया बताएं कि आप किस विशेष प्रोग्राम के बारे में पूछ रहे हैं, "
                "जैसे B.Pharm, D.Pharm, BBA, BCA या Computer Engineering।"
            )
        }

        return messages.get(language, messages["en"])

    program = find_program(program_name)

    if program is None:

        messages = {
            "en": "I could not verify the intake for that program.",
            "mr": "त्या कार्यक्रमाचा intake मी सत्यापित करू शकलो नाही.",
            "hi": "मैं उस प्रोग्राम का intake सत्यापित नहीं कर सका।"
        }

        return messages.get(language, messages["en"])

    current_intake = program.get("current_intake")

    if not current_intake:

        messages = {
            "en": (
                f"{program_name} does not have a fixed seat count listed. "
                "The intake is based on supervisor availability."
            ),
            "mr": (
                f"{program_name} साठी निश्चित जागांची संख्या दिलेली नाही. "
                "Intake supervisor availability नुसार आहे."
            ),
            "hi": (
                f"{program_name} के लिए निश्चित सीट संख्या सूचीबद्ध नहीं है। "
                "Intake supervisor availability के अनुसार है।"
            )
        }

        return messages.get(language, messages["en"])

    seats = current_intake.get("seats")
    academic_year = current_intake.get("academic_year")

    if seats is None:

        messages = {
            "en": f"The intake for {program_name} is not currently specified.",
            "mr": f"{program_name} चा intake सध्या निर्दिष्ट केलेला नाही.",
            "hi": f"{program_name} का intake अभी निर्दिष्ट नहीं है।"
        }

        return messages.get(language, messages["en"])

    if language == "mr":
        return (
            f"{program_name} साठी {academic_year} या शैक्षणिक वर्षात "
            f"{seats} जागांचा intake आहे."
        )

    if language == "hi":
        return (
            f"{program_name} के लिए {academic_year} शैक्षणिक वर्ष में "
            f"{seats} सीटों का intake है।"
        )

    return (
        f"{program_name} has an intake of {seats} seats "
        f"for the {academic_year} academic year."
    )


# ============================================================
# PHARMACY INTAKE
# ============================================================

def get_pharmacy_intake_response(
    message: str,
    language: str = "en"
):
    return get_program_intake_response(message, language)


# ============================================================
# ALL BRANCH / PROGRAM INTAKES
# ============================================================

def get_all_branch_intakes_response(
    language: str = "en"
):
    data = load_college_info()
    programs = data.get("programs", {})

    result = []

    for school_programs in programs.values():

        if not isinstance(school_programs, list):
            continue

        for program in school_programs:

            current_intake = program.get("current_intake")

            if not current_intake:
                continue

            seats = current_intake.get("seats")
            academic_year = current_intake.get("academic_year")

            if seats is None:
                continue

            result.append(
                f"{program.get('short_name', program.get('name'))}: "
                f"{seats} seats ({academic_year})"
            )

    if language == "mr":
        return "उपलब्ध कार्यक्रमांचे सध्याचे intake: " + "; ".join(result)

    if language == "hi":
        return "उपलब्ध प्रोग्राम्स का वर्तमान intake: " + "; ".join(result)

    return "The current program intakes are: " + "; ".join(result)


# ============================================================
# MAIN RESPONSE ROUTER
# ============================================================

def get_response(
    intent: str,
    language: str = "en",
    message: str = ""
) -> str:

    if intent == "branch_intake":
        return get_program_intake_response(message, language)

    if intent == "program_intake":
        return get_program_intake_response(message, language)

    if intent == "pharmacy_intake":
        return get_pharmacy_intake_response(message, language)

    if intent == "all_branch_intakes":
        return get_all_branch_intakes_response(language)

    responses = load_responses()

    if intent in responses:

        intent_responses = responses[intent]

        return intent_responses.get(
            language,
            intent_responses.get(
                "en",
                get_unknown_response(language)
            )
        )

    return get_unknown_response(language)


# ============================================================
# UNKNOWN
# ============================================================

def get_unknown_response(language: str) -> str:

    messages = {

        "en": (
            "Sorry, I don't have information about that. "
            "You can ask me about the university, courses, branches, "
            "facilities, hostel, library, placements, or contact information."
        ),

        "mr": (
            "क्षमस्व, माझ्याकडे या प्रश्नाबद्दल माहिती उपलब्ध नाही. "
            "आपण विद्यापीठ, अभ्यासक्रम, शाखा, सुविधा, वसतिगृह, "
            "ग्रंथालय, प्लेसमेंट किंवा संपर्काबद्दल विचारू शकता."
        ),

        "hi": (
            "क्षमा कीजिए, मेरे पास इस प्रश्न के बारे में जानकारी उपलब्ध नहीं है। "
            "आप विश्वविद्यालय, प्रोग्राम, शाखाओं, सुविधाओं, छात्रावास, "
            "पुस्तकालय, प्लेसमेंट या संपर्क जानकारी के बारे में पूछ सकते हैं।"
        )
    }

    return messages.get(language, messages["en"])