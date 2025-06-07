from flask import Flask, render_template, request, jsonify, session
import spacy
import json
import random
import string

app = Flask(__name__)

# Function to generate a random secret key
def generate_secret_key(length=24):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

app.secret_key = generate_secret_key()

# Load data and spaCy model
with open("faq_data.json", encoding="utf-8") as f:
    faq_data = json.load(f)

nlp = spacy.load('en_core_web_sm')

# Define intents and keywords
intents = {
    "admissions": ["admission", "apply", "eligibility", "how to join", "application process"],
    "courses": ["courses", "subjects", "degree", "bachelor", "masters"],
    "facilities": ["facilities", "campus", "library", "hostel", "sports"],
    "contact": ["contact", "phone", "email", "address"]
}

# Prepare question mapping
def get_all_questions():
    questions = []
    mapping = {}
    for entry in faq_data:
        questions.append(entry["question"])
        mapping[entry["question"]] = entry
        for alt in entry.get("alternatives", []):
            questions.append(alt)
            mapping[alt] = entry
        for follow in entry.get("follow_ups", []):
            questions.append(follow["question"])
            mapping[follow["question"]] = {
                "answer": follow["answer"],
                "category": entry["category"],
                "is_followup": True
            }
    return questions, mapping

all_questions, question_map = get_all_questions()
all_question_docs = [nlp(q) for q in all_questions]

# Routes
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")

# Intent detection
def get_intent(user_input):
    doc = nlp(user_input.lower())
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in doc.text:
                return intent
    return "unknown"

# Conversational touch
def enhance_conversational_response(response, category=None):
    # Categories where we don't want to add conversational starters
    excluded_categories = ["greetings","farewell","gratitude","help","fallback","identity"]

    if category and category.lower() in excluded_categories:
        return response

    # Conversational starters for regular responses
    starters = [
        "Sure!",
        "Absolutely!",
        "Here’s what I found:",
        "Got it!",
        "Interesting question! Here's what I know:",
        "Let me help you with that!"
    ]
    return f"{random.choice(starters)} {response}"


# Main chatbot logic
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data.get("question", "")

    # spaCy doc
    input_doc = nlp(user_input)

    # Find best match using similarity
    max_similarity = -1
    best_match = None
    for i, question_doc in enumerate(all_question_docs):
        sim = input_doc.similarity(question_doc)
        if sim > max_similarity:
            max_similarity = sim
            best_match = all_questions[i]
    
    # Threshold check
       # Threshold check with multiple witty fallback responses
    THRESHOLD = 0.60
    if max_similarity < THRESHOLD:
        fallback_responses = [
            " That doesn’t sound like something about VNR VJIET. Try asking about courses, placements, or clubs!😅",
            " Hmm... I’m not sure what you mean. Maybe ask me about admissions or campus life?🤖",
            "That went over my robotic head! Could you ask about something VNR-ish?🧐 ",
            " Oops! I think you took a wrong turn. I'm trained to answer questions about VNR VJIET only!🚧",
            " I couldn’t find anything related. Maybe try something like 'placement stats' or 'fest events'?🤔",
            "I’m good, but I’m not that good! Let’s stick to college-related stuff, shall we?😅"
        ]
        return jsonify({
            "answer": random.choice(fallback_responses)
        })


    entry = question_map[best_match]

    # Handle intent
    intent = get_intent(user_input)
    if intent != "unknown":
        response = f"Your question seems related to: {intent.capitalize()}. Here's the answer: {entry['answer']}"
    else:
        response = entry["answer"]

    # Add friendliness
    # Enhance response to make it more conversational, using category
    response = enhance_conversational_response(response, entry.get("category"))


    # Suggest follow-ups
    follow_ups = entry.get("follow_ups", [])
    if follow_ups:
        suggestions = "\n\nYou might also want to ask:\n" + "\n".join(f"- {f['question']}" for f in follow_ups)
        response += suggestions

    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(debug=True)
