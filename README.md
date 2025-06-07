**# College-Chatbot
Python-based chatbot for automating student FAQs using NLP.
**# 🤖 VNR VJIET College Chatbot

An intelligent and friendly web-based chatbot designed to answer FAQs about **VNR VJIET** including admissions, courses, campus life, and more. Built using **Flask**, **JavaScript**, and **spaCy**, this chatbot blends rule-based matching with NLP to deliver accurate and conversational answers, including follow-up suggestions.

---

## 🧠 Features

- 💬 Conversational AI using `spaCy` for similarity matching.
- 🧭 Intent detection for routing questions into meaningful categories.
- 🤝 Follow-up question suggestions to mimic natural conversations.
- 😅 Witty fallback responses when input isn't understood.
- ⏳ Typing animation and timestamped chat bubbles.
- 🔎 Support for alternative phrasings and fuzzy matching.
- 🎯 Threshold-based logic for confidence in responses.

---

## 🏗️ Tech Stack

| Layer            | Technology Used                         |
|------------------|------------------------------------------|
| Backend          | Python (Flask), spaCy, fuzzywuzzy        |
| Frontend         | HTML, CSS, JavaScript (Vanilla)          |
| NLP Engine       | spaCy (`en_core_web_sm`)                 |
| Data Handling    | JSON (Custom FAQ dataset)                |
| Matching Logic   | Vector similarity (`spaCy`) + FuzzyWuzzy |
| UI Features      | Typing effect, time stamps, auto-scroll  |

---

## 📁 Folder Structure

```bash
project-root/
│
├── app.py               # Flask app with NLP & FAQ logic
├── faq_data.json        # FAQ dataset with questions, answers, follow-ups
├── templates/
│   ├── index.html       # Optional landing page
│   └── chatbot.html     # Chatbot UI
├── static/
│   └── script.js        # Frontend chat handling
├── requirements.txt     # Python dependencies
└── README.md            # You're here!
by Pavan chandra katepalli.
