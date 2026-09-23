from .knowledge import load_responses

from .knowledge import load_responses, load_college_info


BRANCHES = {
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
    "mechanical": "Mechanical Engineering"
}


BRANCH_INTAKES = {
    "Computer Engineering": 180,
    "Data Science": 120,
    "AI and ML": 60,
    "Civil Engineering": 60,
    "Electrical Engineering": 60,
    "Information Technology": 60,
    "Mechanical Engineering": 60
}


def detect_branch(message: str):
    text = message.lower().strip()

    # Check longer names first
    for keyword in sorted(BRANCHES.keys(), key=len, reverse=True):
        if keyword in text:
            return BRANCHES[keyword]

    return None


def get_branch_intake_response(message: str, language: str = "en"):
    branch = detect_branch(message)

    if branch is None:
        responses = {
            "en": "Please tell me the engineering branch you are asking about.",
            "mr": "कृपया तुम्ही कोणत्या अभियांत्रिकी शाखेबद्दल विचारत आहात ते सांगा.",
            "hi": "कृपया बताएं कि आप किस इंजीनियरिंग ब्रांच के बारे में पूछ रहे हैं।"
        }

        return responses.get(language, responses["en"])

    intake = BRANCH_INTAKES.get(branch)

    if intake is None:
        return get_unknown_response(language)

    if language == "mr":
        return f"{branch} साठी उपलब्ध intake {intake} जागा आहे."

    if language == "hi":
        return f"{branch} के लिए उपलब्ध intake {intake} सीटें हैं।"

    return f"{branch} has an intake of {intake} seats."


def get_response(
    intent: str,
    language: str = "en",
    message: str = ""
) -> str:

    if intent == "branch_intake":
        return get_branch_intake_response(message, language)

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
            "आप विश्वविद्यालय, पाठ्यक्रम, शाखाओं, सुविधाओं, छात्रावास, "
            "पुस्तकालय, प्लेसमेंट या संपर्क जानकारी के बारे में पूछ सकते हैं।"
        )
    }

    return messages.get(language, messages["en"])