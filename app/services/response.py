import re
import unicodedata

from .knowledge import load_responses, load_college_info


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = unicodedata.normalize("NFKC", text)
    text = text.casefold()

    # Normalize common spoken / written separators.
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("/", " ")

    # Keep Unicode letters/numbers and useful program symbols.
    text = re.sub(r"[^\w\s&+.-]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


# ============================================================
# TEXT MATCHING HELPERS
# ============================================================

def contains_any(text: str, terms: list[str]) -> bool:
    """
    Return True if any of the supplied terms appears in the text.
    """
    return any(term in text for term in terms)


# ============================================================
# LOAD ALL PROGRAMS
# ============================================================

def get_all_programs():
    data = load_college_info()
    programs = data.get("programs", {})

    all_programs = []

    for school_key, school_programs in programs.items():

        if not isinstance(school_programs, list):
            continue

        for program in school_programs:

            if not isinstance(program, dict):
                continue

            item = dict(program)
            item["_school_key"] = school_key

            all_programs.append(item)

    return all_programs


# ============================================================
# MANUAL ALIASES
#
# These are speech/STT variations that may not appear in
# college_info.json.
# ============================================================

MANUAL_ALIASES = {

    # ========================================================
    # B.Pharm
    # ========================================================
    "Bachelor of Pharmacy": [
        # English
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
        "b pharm course",
        "b pharmacy course",
        "b pharma course",

        # Marathi / Hindi / Devanagari STT variations
        "बी फार्म",
        "बी फार्मसी",
        "बी फार्मेसी",
        "बी फार्मा",
        "बी फार्मसी कोर्स",
        "बी फार्मेसी कोर्स",

        # Common spoken-English STT variations
        "be pharm",
        "be pharmacy",
        "be pharma",
        "bee pharm",
        "bee pharmacy"
    ],


    # ========================================================
    # D.Pharm
    # ========================================================
    "Diploma in Pharmacy": [
        # English
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
        "d pharma course",

        # Marathi / Hindi / Devanagari
        "डी फार्म",
        "डी फार्मसी",
        "डी फार्मेसी",
        "डी फार्मा",
        "डी फार्मसी कोर्स",
        "डी फार्मेसी कोर्स",

        # Spoken/STT
        "dee pharm",
        "dee pharmacy",
        "de pharm"
    ],


    # ========================================================
    # B.Pharm + MBA
    # ========================================================
    "Bachelor of Pharmacy + MBA (Pharma Tech)": [
        # English
        "b.pharm + mba",
        "b pharm + mba",
        "b-pharm + mba",
        "bpharm + mba",
        "b pharm mba",
        "b.pharm mba",
        "bpharm mba",
        "b pharmacy mba",
        "b-pharmacy mba",
        "b pharma mba",
        "pharmacy plus mba",
        "pharmacy and mba",
        "pharm plus mba",
        "pharm mba",

        # Marathi / Hindi / Devanagari
        "बी फार्म एमबीए",
        "बी फार्मसी एमबीए",
        "बी फार्मेसी एमबीए",
        "फार्मसी प्लस एमबीए",
        "फार्मसी आणि एमबीए",

        # Spoken/STT
        "b pharm and mba",
        "b pharmacy and mba",
        "b pharm plus mba"
    ],


    # ========================================================
    # B.Tech Cosmetic Technology
    # ========================================================
    "B.Tech - Cosmetic Technology": [
        # English
        "b.tech cosmetic",
        "b tech cosmetic",
        "b-tech cosmetic",
        "btech cosmetic",
        "b.tech cosmetic technology",
        "b tech cosmetic technology",
        "btech cosmetic technology",
        "cosmetic technology",
        "cosmetic tech",
        "btech cosmetic tech",

        # Common STT mistakes
        "costology",
        "costology technology",
        "cosmetology",
        "cosmatic",
        "cosmatic technology",
        "b tech costology",
        "b.tech costology",
        "btech costology",
        "b tech cosmetology",
        "b.tech cosmetology",
        "btech cosmetology",
        "b tech cosmatic",
        "b.tech cosmatic",
        "btech cosmatic",

        # Marathi / Devanagari
        "बीटेक कॉस्मेटिक",
        "बी टेक कॉस्मेटिक",
        "बी टेक कॉस्मेटिक टेक्नॉलॉजी",
        "कॉस्मेटिक टेक्नॉलॉजी",
        "कॉस्मेटिक टेक",

        # Hindi
        "बीटेक कॉस्मेटिक टेक्नोलॉजी",
        "कॉस्मेटिक टेक्नोलॉजी"
    ],


    # ========================================================
    # BBA
    # ========================================================
    "Bachelor of Business Administration": [
        "bba",
        "b.b.a",
        "bba course",
        "bba program",
        "business administration",

        # Spoken
        "b b a",
        "bee bee ay",

        # Marathi / Hindi
        "बीबीए",
        "बी बी ए",
        "बीबीए कोर्स",
        "बीबीए प्रोग्राम"
    ],


    # ========================================================
    # BCA
    # ========================================================
    "Bachelor of Computer Applications": [
        "bca",
        "b.c.a",
        "bca course",
        "bca program",
        "computer applications",

        # Spoken
        "b c a",
        "bee see ay",

        # Marathi / Hindi
        "बीसीए",
        "बी सी ए",
        "बीसीए कोर्स"
    ],


    # ========================================================
    # MCA
    # ========================================================
    "Master of Computer Applications": [
        "mca",
        "m.c.a",
        "mca course",
        "mca program",
        "master of computer applications",

        # Spoken
        "m c a",
        "em see ay",

        # Marathi / Hindi
        "एमसीए",
        "एम सी ए",
        "एमसीए कोर्स"
    ],


    # ========================================================
    # COMPUTER ENGINEERING
    # ========================================================
    "Computer Engineering": [
        "computer engineering",
        "computer engg",
        "computer engineering branch",
        "computer branch",

        # Marathi
        "कॉम्प्युटर इंजिनिअरिंग",
        "कॉम्प्युटर इंजीनियरिंग",
        "कॉम्प्युटर शाखा"
    ],


    # ========================================================
    # DATA SCIENCE
    # ========================================================
    "Data Science": [
        "data science",
        "cse data science",
        "computer science data science",
        "computer science and engineering data science",
        "data science engineering",

        # Marathi
        "डेटा सायन्स",
        "डेटा सायन्स इंजिनिअरिंग"
    ],


    # ========================================================
    # AI AND ML
    # ========================================================
    "AI and ML": [
        "ai and ml",
        "ai & ml",
        "ai ml",
        "aiml",
        "artificial intelligence and machine learning",
        "artificial intelligence machine learning",

        # Marathi / Hindi
        "एआय आणि एमएल",
        "एआय एमएल",
        "आर्टिफिशियल इंटेलिजन्स आणि मशीन लर्निंग"
    ],


    # ========================================================
    # CIVIL ENGINEERING
    # ========================================================
    "Civil Engineering": [
        "civil engineering",
        "civil engg",
        "civil",

        # Marathi / Hindi
        "सिव्हिल इंजिनिअरिंग",
        "सिविल इंजीनियरिंग",
        "सिव्हिल"
    ],


    # ========================================================
    # ELECTRICAL ENGINEERING
    # ========================================================
    "Electrical Engineering": [
        "electrical engineering",
        "electrical engg",
        "electrical",

        # Marathi / Hindi
        "इलेक्ट्रिकल इंजिनिअरिंग",
        "इलेक्ट्रिकल इंजीनियरिंग",
        "इलेक्ट्रिकल"
    ],


    # ========================================================
    # INFORMATION TECHNOLOGY
    # ========================================================
    "Information Technology": [
        "information technology",
        "information tech",
        "it engineering",
        "it branch",

        # Marathi / Hindi
        "इन्फॉर्मेशन टेक्नॉलॉजी",
        "इन्फॉर्मेशन टेक्नोलॉजी",
        "आयटी इंजिनिअरिंग",
        "आयटी शाखा"
    ],


    # ========================================================
    # MECHANICAL ENGINEERING
    # ========================================================
    "Mechanical Engineering": [
        "mechanical engineering",
        "mechanical engg",
        "mechanical",

        # Marathi / Hindi
        "मेकॅनिकल इंजिनिअरिंग",
        "मैकेनिकल इंजीनियरिंग",
        "मेकॅनिकल"
    ]
}


# ============================================================
# FIND PROGRAM
# ============================================================

def find_program(message: str):
    """
    Identify a program from English, Hindi, Marathi,
    and common speech/STT variations.

    Matching priority:
    1. Explicit manual aliases
    2. JSON short_name
    3. JSON full name
    4. Cosmetic Technology fallback
    5. B.Pharm fallback
    """

    text = normalize_text(message)

    if not text:
        return None

    programs = get_all_programs()

    # ========================================================
    # 1. MANUAL ALIAS MATCHING
    # ========================================================

    alias_matches = []

    for canonical, aliases in MANUAL_ALIASES.items():

        for alias in aliases:

            alias_normalized = normalize_text(alias)

            if not alias_normalized:
                continue

            # Direct phrase match.
            if alias_normalized in text:
                alias_matches.append(
                    (len(alias_normalized), canonical)
                )

    # Longest / most specific alias first.
    alias_matches.sort(
        key=lambda item: item[0],
        reverse=True
    )

    for _, canonical in alias_matches:

        canonical_normalized = normalize_text(canonical)

        for program in programs:

            name = normalize_text(
                program.get("name", "")
            )

            short_name = normalize_text(
                program.get("short_name", "")
            )

            if canonical_normalized == name:
                return program

            if canonical_normalized == short_name:
                return program

    # ========================================================
    # 2. DIRECT JSON SHORT-NAME MATCHING
    # ========================================================

    for program in programs:

        short_name = normalize_text(
            program.get("short_name", "")
        )

        if short_name and short_name in text:
            return program

    # ========================================================
    # 3. DIRECT JSON FULL-NAME MATCHING
    # ========================================================

    for program in programs:

        name = normalize_text(
            program.get("name", "")
        )

        if name and name in text:
            return program

    # ========================================================
    # 4. COSMETIC TECHNOLOGY FALLBACK
    #
    # STT can produce many variants such as:
    # cosmetic / cosmetology / costology / cosmatic
    # and Marathi speech may contain only
    # "बीटेक कॉस्मेटिक".
    # ========================================================

    cosmetic_indicators = [
        "cosmetic",
        "cosmetology",
        "costology",
        "cosmatic",
        "कॉस्मेटिक",
        "कॉस्मेटिक टेक्नॉलॉजी",
        "कॉस्मेटिक टेक्नोलॉजी",
        "बीटेक कॉस्मेटिक",
        "बी टेक कॉस्मेटिक",
    ]

    if contains_any(text, cosmetic_indicators):

        for program in programs:

            name = normalize_text(
                program.get("name", "")
            )

            short_name = normalize_text(
                program.get("short_name", "")
            )

            if (
                "cosmetic" in name
                or "cosmetic" in short_name
            ):
                return program

    # ========================================================
    # 5. PHARMACY PROGRAM FALLBACKS
    # ========================================================

    if contains_any(text, [
        "बी फार्मसी",
        "बी फार्मेसी",
        "बी फार्म",
        "b.pharm",
        "b pharm",
        "bpharm",
        "b pharmacy",
        "b pharma",
    ]):

        for program in programs:

            name = normalize_text(
                program.get("name", "")
            )

            short_name = normalize_text(
                program.get("short_name", "")
            )

            if (
                "b.pharm" in name
                or "b.pharm" in short_name
                or "b pharmacy" in name
                or "b pharmacy" in short_name
            ):
                return program

    # ========================================================
    # 6. NO MATCH
    # ========================================================

    return None


# ============================================================
# FIND SCHOOL
# ============================================================

def detect_school(message: str):
    text = normalize_text(message)

    if any(term in text for term in [
        "pharmacy",
        "pharma",
        "pharm",
        "फार्मसी",
        "फार्मेसी",
        "pharmacy department",
        "school of pharmacy"
    ]):
        return "school_of_pharmacy_technology_management"

    if any(term in text for term in [
        "commerce",
        "bba",
        "bca",
        "school of commerce",
        "कॉमर्स",
        "वाणिज्य"
    ]):
        return "school_of_commerce"

    if any(term in text for term in [
        "engineering",
        "technology",
        "stme",
        "computer engineering",
        "civil engineering",
        "mechanical engineering",
        "electrical engineering",
        "information technology",
        "data science",
        "ai and ml",
        "ai & ml",
        "इंजिनिअरिंग",
        "इंजीनियरिंग"
    ]):
        return "school_of_technology_management_engineering"

    return None


# ============================================================
# FIND PROGRAMS FOR A SCHOOL
# ============================================================

def get_school_programs(school_key: str):
    data = load_college_info()

    programs = data.get("programs", {})

    school_programs = programs.get(school_key, [])

    if not isinstance(school_programs, list):
        return []

    return school_programs


# ============================================================
# LANGUAGE HELPERS
# ============================================================

def lang_text(language: str, en: str, mr: str, hi: str):
    if language == "mr":
        return mr

    if language == "hi":
        return hi

    return en


# ============================================================
# PROGRAM NAME
# ============================================================

def program_display_name(program: dict):
    return (
        program.get("short_name")
        or program.get("name")
        or "This program"
    )


# ============================================================
# PROGRAM INFORMATION
# ============================================================

def get_program_information(
    message: str,
    language: str = "en"
):

    program = find_program(message)

    if program is None:

        school = detect_school(message)

        if school:
            return get_school_programs_response(
                school,
                language
            )

        responses = load_responses()

        return responses["clarify_program"].get(
            language,
            responses["clarify_program"]["en"]
        )

    name = program_display_name(program)
    full_name = program.get("name", name)
    duration = program.get("duration")
    level = program.get("level")
    current_intake = program.get("current_intake")

    parts = []

    if full_name:
        parts.append(full_name)

    if level:
        parts.append(f"level: {level}")

    if duration:
        parts.append(f"duration: {duration}")

    if current_intake:
        seats = current_intake.get("seats")
        academic_year = current_intake.get("academic_year")

        if seats is not None and academic_year:
            parts.append(
                f"current intake: {seats} seats for {academic_year}"
            )

    summary = ". ".join(parts) + "."

    if language == "mr":
        return f"{full_name} बद्दल माहिती: {summary}"

    if language == "hi":
        return f"{full_name} के बारे में जानकारी: {summary}"

    return f"Here is the available information about {full_name}: {summary}"


# ============================================================
# PROGRAM INTAKE
# ============================================================

def get_program_intake_response(
    message: str,
    language: str = "en"
):

    program = find_program(message)

    if program is None:

        school = detect_school(message)

        if school == "school_of_pharmacy_technology_management":

            return lang_text(
                language,

                "Please tell me the specific Pharmacy program, such as B.Pharm, D.Pharm, B.Pharm plus MBA, or B.Tech Cosmetic Technology.",

                "कृपया विशिष्ट Pharmacy कार्यक्रम सांगा, जसे B.Pharm, D.Pharm, B.Pharm plus MBA किंवा B.Tech Cosmetic Technology.",

                "कृपया विशेष Pharmacy प्रोग्राम बताएं, जैसे B.Pharm, D.Pharm, B.Pharm plus MBA या B.Tech Cosmetic Technology।"
            )

        if school == "school_of_commerce":

            return lang_text(
                language,

                "Please tell me whether you mean BBA or BCA.",

                "कृपया तुम्हाला BBA की BCA यापैकी कोणत्या कार्यक्रमाचा intake हवा आहे ते सांगा.",

                "कृपया बताएं कि आप BBA या BCA में से किस प्रोग्राम का intake पूछ रहे हैं।"
            )

        return lang_text(
            language,

            "Please tell me the specific program for which you want the seat or intake information.",

            "कृपया ज्या विशिष्ट कार्यक्रमाचा intake किंवा जागांची माहिती हवी आहे तो कार्यक्रम सांगा.",

            "कृपया उस विशेष प्रोग्राम का नाम बताएं जिसका intake या सीटों की जानकारी चाहिए।"
        )

    name = program_display_name(program)
    intake = program.get("current_intake")

    # --------------------------------------------------------
    # No fixed intake
    # --------------------------------------------------------

    if not intake:

        if "intake" in program:

            value = program.get("intake")

            return lang_text(
                language,

                f"{name} has an intake described as: {value}.",

                f"{name} साठी intake अशी नमूद आहे: {value}.",

                f"{name} का intake इस प्रकार दिया गया है: {value}।"
            )

        return lang_text(
            language,

            f"A fixed current seat count for {name} is not available in the knowledge base.",

            f"{name} साठी सध्याची निश्चित जागांची संख्या knowledge base मध्ये उपलब्ध नाही.",

            f"{name} के लिए वर्तमान निश्चित सीट संख्या knowledge base में उपलब्ध नहीं है।"
        )

    seats = intake.get("seats")
    academic_year = intake.get("academic_year")
    note = intake.get("note")

    if seats is None:

        return lang_text(
            language,

            f"The current intake for {name} is not specified.",

            f"{name} चा सध्याचा intake निर्दिष्ट केलेला नाही.",

            f"{name} का वर्तमान intake निर्दिष्ट नहीं है।"
        )

    # --------------------------------------------------------
    # Verified current intake
    # --------------------------------------------------------

    if language == "mr":

        answer = (
            f"{name} साठी {academic_year} या शैक्षणिक वर्षात "
            f"{seats} जागांचा intake आहे."
        )

        if note:
            answer += " " + note

        return answer

    if language == "hi":

        answer = (
            f"{name} के लिए {academic_year} शैक्षणिक वर्ष में "
            f"{seats} सीटों का intake है।"
        )

        if note:
            answer += " " + note

        return answer

    answer = (
        f"{name} has an intake of {seats} seats "
        f"for the {academic_year} academic year."
    )

    if note:
        answer += f" {note}"

    return answer


# ============================================================
# PROGRAM DURATION
# ============================================================

def get_program_duration_response(
    message: str,
    language: str = "en"
):

    program = find_program(message)

    if program is None:

        return lang_text(
            language,

            "Please tell me the specific program whose duration you want to know.",

            "कृपया ज्या विशिष्ट कार्यक्रमाचा कालावधी जाणून घ्यायचा आहे तो कार्यक्रम सांगा.",

            "कृपया उस विशेष प्रोग्राम का नाम बताएं जिसकी अवधि आप जानना चाहते हैं।"
        )

    name = program_display_name(program)
    duration = program.get("duration")

    if not duration:

        return lang_text(
            language,

            f"The duration of {name} is not currently available in the knowledge base.",

            f"{name} चा कालावधी सध्या knowledge base मध्ये उपलब्ध नाही.",

            f"{name} की अवधि अभी knowledge base में उपलब्ध नहीं है।"
        )

    return lang_text(
        language,

        f"{name} has a duration of {duration}.",

        f"{name} चा कालावधी {duration} आहे.",

        f"{name} की अवधि {duration} है।"
    )


# ============================================================
# PROGRAM ELIGIBILITY
# ============================================================

def extract_eligibility(program: dict):
    """
    Supports several possible field names without inventing data.
    """

    possible_keys = [
        "eligibility",
        "eligibility_criteria",
        "admission_eligibility",
        "eligibilityCriteria"
    ]

    for key in possible_keys:

        value = program.get(key)

        if value:
            return value

    return None


def format_eligibility(value, language: str):

    if isinstance(value, str):
        return value

    if isinstance(value, list):
        return " ".join(str(item) for item in value)

    if isinstance(value, dict):

        parts = []

        for key, item in value.items():

            if isinstance(item, list):
                item = ", ".join(str(x) for x in item)

            parts.append(
                f"{key}: {item}"
            )

        return "; ".join(parts)

    return str(value)


def get_program_eligibility_response(
    message: str,
    language: str = "en"
):

    program = find_program(message)

    if program is None:

        school = detect_school(message)

        if school:

            programs = get_school_programs(school)

            if programs:
                return lang_text(
                    language,

                    "Please tell me the specific program for which you want eligibility information.",

                    "कृपया ज्या विशिष्ट कार्यक्रमाची पात्रता हवी आहे तो कार्यक्रम सांगा.",

                    "कृपया उस विशेष प्रोग्राम का नाम बताएं जिसकी पात्रता आप जानना चाहते हैं।"
                )

        responses = load_responses()

        return responses["admission_eligibility"].get(
            language,
            responses["admission_eligibility"]["en"]
        )

    name = program_display_name(program)

    eligibility = extract_eligibility(program)

    if not eligibility:

        return lang_text(
            language,

            f"I do not have verified eligibility details for {name} in the current knowledge base.",

            f"{name} साठी सध्याच्या knowledge base मध्ये सत्यापित पात्रता माहिती उपलब्ध नाही.",

            f"{name} के लिए वर्तमान knowledge base में सत्यापित पात्रता जानकारी उपलब्ध नहीं है।"
        )

    formatted = format_eligibility(
        eligibility,
        language
    )

    if language == "mr":
        return f"{name} साठी पात्रता: {formatted}"

    if language == "hi":
        return f"{name} के लिए पात्रता: {formatted}"

    return f"The eligibility for {name} is: {formatted}"


# ============================================================
# SCHOOL PROGRAM LIST
# ============================================================

def get_school_programs_response(
    school_key: str,
    language: str = "en"
):

    programs = get_school_programs(school_key)

    if not programs:
        return lang_text(
            language,

            "I could not verify the programs for that school.",

            "त्या शाळेतील कार्यक्रमांची माहिती सत्यापित करता आली नाही.",

            "मैं उस स्कूल के कार्यक्रमों की जानकारी सत्यापित नहीं कर सका।"
        )

    names = []

    for program in programs:

        name = program.get("short_name") or program.get("name")

        if name:
            names.append(name)

    if language == "mr":
        return "उपलब्ध कार्यक्रम: " + ", ".join(names) + "."

    if language == "hi":
        return "उपलब्ध प्रोग्राम: " + ", ".join(names) + "।"

    return "The available programs are: " + ", ".join(names) + "."


# ============================================================
# ALL ENGINEERING INTAKES
# ============================================================

def get_all_branch_intakes_response(
    language: str = "en"
):

    programs = get_school_programs(
        "school_of_technology_management_engineering"
    )

    results = []

    for program in programs:

        intake = program.get("current_intake")

        if not intake:
            continue

        seats = intake.get("seats")
        year = intake.get("academic_year")

        if seats is None:
            continue

        name = program.get("short_name") or program.get("name")

        results.append(
            f"{name}: {seats} seats ({year})"
        )

    if not results:
        return lang_text(
            language,

            "Current engineering intake information is not available.",

            "सध्याची अभियांत्रिकी intake माहिती उपलब्ध नाही.",

            "वर्तमान इंजीनियरिंग intake जानकारी उपलब्ध नहीं है।"
        )

    if language == "mr":
        return "अभियांत्रिकी कार्यक्रमांचे सध्याचे intake: " + "; ".join(results)

    if language == "hi":
        return "इंजीनियरिंग प्रोग्राम्स का वर्तमान intake: " + "; ".join(results)

    return "The current engineering program intakes are: " + "; ".join(results)


# ============================================================
# ALL PROGRAM INTAKES
# ============================================================

def get_all_program_intakes_response(
    language: str = "en"
):

    programs = get_all_programs()

    results = []

    for program in programs:

        intake = program.get("current_intake")

        if not intake:
            continue

        seats = intake.get("seats")
        year = intake.get("academic_year")

        if seats is None:
            continue

        name = program.get("short_name") or program.get("name")

        results.append(
            f"{name}: {seats} seats ({year})"
        )

    if not results:
        return lang_text(
            language,

            "Current program intake information is not available.",

            "सध्याची कार्यक्रमांची intake माहिती उपलब्ध नाही.",

            "वर्तमान प्रोग्राम intake जानकारी उपलब्ध नहीं है।"
        )

    if language == "mr":
        return "सर्व उपलब्ध कार्यक्रमांचे intake: " + "; ".join(results)

    if language == "hi":
        return "सभी उपलब्ध प्रोग्राम्स का intake: " + "; ".join(results)

    return "The current program intakes are: " + "; ".join(results)


# ============================================================
# MAIN RESPONSE ROUTER
# ============================================================

def get_response(
    intent: str,
    language: str = "en",
    message: str = ""
) -> str:

    # --------------------------------------------------------
    # Dynamic program questions
    # --------------------------------------------------------

    if intent == "program_information":
        return get_program_information(
            message,
            language
        )

    if intent == "program_intake":
        return get_program_intake_response(
            message,
            language
        )

    if intent == "pharmacy_intake":
        return get_program_intake_response(
            message,
            language
        )

    if intent == "program_duration":
        return get_program_duration_response(
            message,
            language
        )

    if intent == "program_eligibility":
        return get_program_eligibility_response(
            message,
            language
        )

    if intent == "pharmacy_programs":
        return get_school_programs_response(
            "school_of_pharmacy_technology_management",
            language
        )

    if intent == "commerce_programs":
        return get_school_programs_response(
            "school_of_commerce",
            language
        )

    if intent == "all_branch_intakes":
        return get_all_branch_intakes_response(
            language
        )

    if intent == "all_program_intakes":
        return get_all_program_intakes_response(
            language
        )

    # --------------------------------------------------------
    # Fixed institutional responses
    # --------------------------------------------------------

    responses = load_responses()

    if intent in responses:

        intent_responses = responses[intent]

        return intent_responses.get(
            language,
            intent_responses.get(
                "en",
                responses["unknown"]["en"]
            )
        )

    return responses["unknown"].get(
        language,
        responses["unknown"]["en"]
    )