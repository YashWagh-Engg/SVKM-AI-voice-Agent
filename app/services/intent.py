def detect_intent(message: str) -> str:
    text = message.lower().strip()

    intent_keywords = {
        "college_location": [
            "where is the college",
            "where is the university",
            "location",
            "located",
            "address",
            "कहाँ",
            "कुठे",
            "पता",
            "ठिकाण"
        ],

        "engineering_branches": [
            "branches",
            "engineering branches",
            "engineering branch",
            "branch",
            "शाखा",
            "शाखाएं"
        ],
        "branch_intake": [
            "intake",
            "how many seats",
            "seat",
            "seats",
            "capacity",
            "कितनी सीट",
            "कितने सीट",
            "जागा",
            "जागा किती"
            ],

        "college_introduction": [
            "tell me about the college",
            "tell me about the university",
            "about the college",
            "about the university",
            "college information",
            "university information",
            "कॉलेज के बारे में",
            "विश्वविद्यालय के बारे में",
            "कॉलेज बद्दल",
            "विद्यापीठाबद्दल"
        ],

        "schools": [
            "schools",
            "school",
            "what schools",
            "कितने स्कूल",
            "कोणते स्कूल",
            "शाळा"
        ],

        "programs": [
            "courses",
            "course",
            "programs",
            "program",
            "what do you offer",
            "कोर्स",
            "पाठ्यक्रम",
            "अभ्यासक्रम"
        ],

        "facilities": [
            "facilities",
            "facility",
            "campus facilities",
            "सुविधाएं",
            "सुविधा",
            "सुविधा आहेत"
        ],

        "hostel": [
            "hostel",
            "accommodation",
            "stay",
            "वसतिगृह",
            "छात्रावास"
        ],

        "library": [
            "library",
            "books",
            "ग्रंथालय",
            "पुस्तकालय"
        ],

        "sports": [
            "sports",
            "playground",
            "games",
            "क्रीडा",
            "खेल"
        ],
        "all_branch_intakes": [
        "all branch intake",
        "all branch intakes",
        "all branches seats",
        "all branch seats",
        "सभी शाखाओं की सीट",
        "सर्व शाखांच्या जागा"
        ],

        "placements": [
            "placement",
            "placements",
            "job",
            "jobs",
            "career",
            "नोकरी",
            "प्लेसमेंट",
            "रोजगार"
        ],

        "research": [
            "research",
            "innovation",
            "research facilities",
            "संशोधन",
            "अनुसंधान"
        ],

        "contact": [
            "contact",
            "phone number",
            "telephone",
            "email",
            "फोन",
            "संपर्क",
            "ईमेल"
        ],

        "website": [
            "website",
            "web site",
            "official website",
            "वेबसाइट"
        ]
    }

    for intent, keywords in intent_keywords.items():
        if any(keyword in text for keyword in keywords):
            return intent

    return "unknown"