import json
from fuzzywuzzy import process

# Load FAQ data
with open('faq_data.json') as file:
    faq_data = json.load(file)

# Prepare searchable question set including follow-ups
def get_all_questions():
    questions = []
    mapping = {}  # maps question -> full entry

    for entry in faq_data:
        questions.append(entry["question"])
        mapping[entry["question"]] = entry
        for alt in entry.get("alternatives", []):
            questions.append(alt)
            mapping[alt] = entry
        for follow in entry.get("follow_ups", []):
            questions.append(follow["question"])
            mapping[follow["question"]] = {"answer": follow["answer"], "category": entry["category"], "is_followup": True}
    return questions, mapping

all_questions, question_map = get_all_questions()

# Get best match
def get_best_match(user_input):
    return process.extractOne(user_input, all_questions)

# Fetch answer
def get_answer(user_input):
    match = get_best_match(user_input)
    if not match:
        return "Sorry, I couldn't understand your question. Can you rephrase it?"
    
    matched_q = match[0]
    entry = question_map.get(matched_q)

    if not entry:
        return "Sorry, I couldn't find an answer."

    # Main question
    if not entry.get("is_followup", False):
        response = entry["answer"]
        follow_ups = entry.get("follow_ups", [])
        if follow_ups:
            suggestions = "\n\nYou might also want to ask:\n" + "\n".join(f"- {f['question']}" for f in follow_ups)
            return response + suggestions
        return response

    # Follow-up
    return entry["answer"]

# Chat loop
def chat():
    print("Welcome to the VNR VJIET Chatbot! Ask your question. (Type 'exit' to quit)")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        print("Bot:", get_answer(user_input))

# Run
if __name__ == "__main__":
    chat()
