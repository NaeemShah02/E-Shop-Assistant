# from flask import Flask, render_template, Response, request, stream_with_context
# from thefuzz import fuzz, process
# import json
# import re
# import os
# import html

# app = Flask(__name__)

# # -------------------------------
# # Load local Q&A dataset
# # -------------------------------
# def load_qa_data():
#     try:
#         with open("ecommerce_chatbot_dataset.json", "r", encoding="utf-8") as f:
#             dataset = json.load(f)
        
#         qa_data = {}
#         keywords_index = {}
        
#         for item in dataset:
#             for question in item["questions"]:
#                 keywords = set(re.findall(r'\w+', question.lower()))
#                 qa_data[question] = {
#                     "answer": item["answer"],
#                     "keywords": keywords,
#                     "category": item["category"]
#                 }
                
#                 for keyword in keywords:
#                     if keyword not in keywords_index:
#                         keywords_index[keyword] = []
#                     keywords_index[keyword].append(question)
        
#         return qa_data, keywords_index
#     except Exception as e:
#         print(f"Error loading QA data: {e}")
#         return {}, {}

# qa_data, keywords_index = load_qa_data()

# # -------------------------------
# # Suggestion Generator
# # -------------------------------
# def get_context_aware_suggestions(user_input, previous_response):
#     try:
#         base_suggestions = [
#             "What are your shipping policies?",
#             "Do you offer refunds?",
#             "Tell me about your products",
#             "What payment methods do you accept?"
#         ]
        
#         keywords = set(re.findall(r'\w+', user_input.lower()))
#         related_questions = set()

#         for keyword in keywords:
#             if keyword in keywords_index:
#                 related_questions.update(keywords_index[keyword][:2])
        
#         context_suggestions = list(related_questions)[:2] + base_suggestions[:2]
#         return context_suggestions
#     except Exception as e:
#         print(f"Error generating suggestions: {e}")
#         return base_suggestions

# # -------------------------------
# # Local Fuzzy Matching
# # -------------------------------
# def enhanced_matching(user_input, qa_data, threshold=70):
#     try:
#         normalized_input = user_input.lower().strip()
#         keywords = set(re.findall(r'\w+', normalized_input))

#         best_matches = []
#         questions = list(qa_data.keys())

#         # Direct fuzzy match
#         direct_match = process.extractOne(normalized_input, questions, scorer=fuzz.token_sort_ratio)
#         if direct_match and direct_match[1] >= threshold:
#             best_matches.append((direct_match[0], direct_match[1]))

#         # Keyword overlap match
#         for question in questions:
#             question_keywords = qa_data[question]["keywords"]
#             overlap = len(keywords.intersection(question_keywords))
#             if overlap > 1:
#                 similarity = (overlap / len(keywords)) * 100
#                 if similarity >= threshold:
#                     best_matches.append((question, similarity))

#         if best_matches:
#             best_match = max(best_matches, key=lambda x: x[1])[0]
#             return qa_data[best_match]["answer"]
        
#         return None
#     except Exception as e:
#         print(f"Error in enhanced matching: {e}")
#         return None

# # -------------------------------
# # SSE (Server-Sent Events)
# # -------------------------------
# def format_sse(data_type, content):
#     try:
#         if data_type == "content":
#             content = html.escape(content)
#         message = json.dumps({"type": data_type, "content": content})
#         return f"data: {message}\n\n"
#     except Exception as e:
#         print(f"Error formatting SSE: {e}")
#         return f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

# # -------------------------------
# # Flask Routes
# # -------------------------------
# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/chat', methods=['POST'])
# def chat():
#     @stream_with_context
#     def generate():
#         try:
#             user_input = request.json.get("message", "").strip()
#             if not user_input:
#                 yield format_sse("content", "I didn't understand that. Can you rephrase?")
#                 suggestions = get_context_aware_suggestions("", "")
#                 yield format_sse("suggestions", json.dumps(suggestions))
#                 return

#             # Try local matching first
#             answer = enhanced_matching(user_input, qa_data)
            
#             if answer:
#                 yield format_sse("content", answer)
#                 suggestions = get_context_aware_suggestions(user_input, answer)
#                 yield format_sse("suggestions", json.dumps(suggestions))
#                 return

#             # Offline fallback
#             collected_response = "I'm not sure about that. Please refer to our FAQ or contact support."
#             yield format_sse("content", collected_response)
#             suggestions = get_context_aware_suggestions(user_input, collected_response)
#             yield format_sse("suggestions", json.dumps(suggestions))
                
#         except Exception as e:
#             print(f"Error in generate function: {e}")
#             yield format_sse("content", "An error occurred. Please try again.")
#             yield format_sse("suggestions", json.dumps(["What are your shipping policies?", "Do you offer refunds?"]))

#     return Response(generate(), mimetype='text/event-stream')

# # -------------------------------
# # Create default dataset if missing
# # -------------------------------
# if __name__ == "__main__":
#     if not os.path.exists("ecommerce_chatbot_dataset.json"):
#         sample_dataset = [
#             {
#                 "questions": ["What are your shipping policies?", "How do you handle shipping?", "Tell me about delivery"],
#                 "answer": "We offer free shipping on orders over $50. Standard shipping takes 3-5 business days, while express shipping takes 1-2 business days.",
#                 "category": "shipping"
#             },
#             {
#                 "questions": ["Do you offer refunds?", "What's your return policy?", "Can I return items?"],
#                 "answer": "Yes, we offer a 30-day money-back guarantee on all purchases. Items must be in original condition with tags attached.",
#                 "category": "returns"
#             },
#             {
#                 "questions": ["What payment methods do you accept?", "How can I pay?", "Payment options"],
#                 "answer": "We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and Apple Pay.",
#                 "category": "payment"
#             }
#         ]
#         with open("ecommerce_chatbot_dataset.json", "w", encoding="utf-8") as f:
#             json.dump(sample_dataset, f, indent=4)
    
#     app.run(debug=True, port=5000)




















# chatbot.py
import json
import os
import re
import html
from pathlib import Path
from flask import Flask, render_template, Response, request, stream_with_context
from thefuzz import fuzz, process

app = Flask(__name__, template_folder="templates", static_folder="static")

# -------------------------------
# Dataset loading (path-safe)
# -------------------------------
def load_qa_data():
    try:
        base = Path(__file__).resolve().parent
        dataset_path = base / "ecommerce_chatbot_dataset.json"
        if not dataset_path.exists():
            # create a small default dataset if missing
            sample_dataset = [
                {
                    "questions": ["What are your shipping policies?", "How do you handle shipping?", "Tell me about delivery"],
                    "answer": "We offer free shipping on orders over $50. Standard shipping takes 3-5 business days, while express shipping takes 1-2 business days.",
                    "category": "shipping"
                },
                {
                    "questions": ["Do you offer refunds?", "What's your return policy?", "Can I return items?"],
                    "answer": "Yes, we offer a 30-day money-back guarantee on all purchases. Items must be in original condition with tags attached.",
                    "category": "returns"
                },
                {
                    "questions": ["What payment methods do you accept?", "How can I pay?", "Payment options"],
                    "answer": "We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and Apple Pay.",
                    "category": "payment"
                }
            ]
            with open(dataset_path, "w", encoding="utf-8") as f:
                json.dump(sample_dataset, f, indent=2)

        with open(dataset_path, "r", encoding="utf-8") as f:
            dataset = json.load(f)

        qa_data = {}
        keywords_index = {}

        for item in dataset:
            answer = item.get("answer", "")
            category = item.get("category", "")
            questions = item.get("questions", [])
            for question in questions:
                keywords = set(re.findall(r'\w+', question.lower()))
                qa_data[question] = {
                    "answer": answer,
                    "keywords": keywords,
                    "category": category
                }
                for keyword in keywords:
                    keywords_index.setdefault(keyword, []).append(question)

        return qa_data, keywords_index

    except Exception as e:
        print(f"[load_qa_data] Error: {e}")
        return {}, {}

qa_data, keywords_index = load_qa_data()

# -------------------------------
# Suggestion Generator
# -------------------------------
def get_context_aware_suggestions(user_input, previous_response):
    try:
        base_suggestions = [
            "What are your shipping policies?",
            "Do you offer refunds?",
            "Tell me about your products",
            "What payment methods do you accept?"
        ]

        keywords = set(re.findall(r'\w+', user_input.lower()))
        related_questions = set()

        for keyword in keywords:
            if keyword in keywords_index:
                related_questions.update(keywords_index[keyword][:2])

        context_suggestions = list(related_questions)[:2] + base_suggestions[:2]
        return context_suggestions
    except Exception as e:
        print(f"[get_context_aware_suggestions] Error: {e}")
        return [
            "What are your shipping policies?",
            "Do you offer refunds?"
        ]

# -------------------------------
# Local Fuzzy Matching
# -------------------------------
def enhanced_matching(user_input, qa_data, threshold=70):
    try:
        normalized_input = user_input.lower().strip()
        if not normalized_input:
            return None

        keywords = set(re.findall(r'\w+', normalized_input))
        best_matches = []
        questions = list(qa_data.keys())

        # Direct fuzzy match
        try:
            direct_match = process.extractOne(normalized_input, questions, scorer=fuzz.token_sort_ratio)
        except Exception:
            direct_match = None

        if direct_match and direct_match[1] >= threshold:
            best_matches.append((direct_match[0], direct_match[1]))

        # Keyword overlap match
        for question in questions:
            question_keywords = qa_data[question]["keywords"]
            overlap = len(keywords.intersection(question_keywords))
            if overlap > 1 and keywords:
                similarity = (overlap / len(keywords)) * 100
                if similarity >= threshold:
                    best_matches.append((question, similarity))

        if best_matches:
            best_match = max(best_matches, key=lambda x: x[1])[0]
            return qa_data[best_match]["answer"]

        return None
    except Exception as e:
        print(f"[enhanced_matching] Error: {e}")
        return None

# -------------------------------
# SSE Formatting
# -------------------------------
def format_sse(data_type, content):
    try:
        # escape content when type is content to avoid injecting HTML
        if data_type == "content":
            content = html.escape(content)
        message = json.dumps({"type": data_type, "content": content})
        return f"data: {message}\n\n"
    except Exception as e:
        print(f"[format_sse] Error: {e}")
        return f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

# -------------------------------
# Routes
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    @stream_with_context
    def generate():
        try:
            data = request.get_json(silent=True) or {}
            user_input = (data.get("message") or "").strip()
            if not user_input:
                yield format_sse("content", "I didn't understand that. Can you rephrase?")
                suggestions = get_context_aware_suggestions("", "")
                yield format_sse("suggestions", json.dumps(suggestions))
                return

            # First, try local matching
            answer = enhanced_matching(user_input, qa_data)

            if answer:
                yield format_sse("content", answer)
                suggestions = get_context_aware_suggestions(user_input, answer)
                yield format_sse("suggestions", json.dumps(suggestions))
                return

            # Offline fallback
            collected_response = "I'm not sure about that. Please refer to our FAQ or contact support."
            yield format_sse("content", collected_response)
            suggestions = get_context_aware_suggestions(user_input, collected_response)
            yield format_sse("suggestions", json.dumps(suggestions))

        except Exception as e:
            print(f"[/chat generate] Error: {e}")
            yield format_sse("content", "An error occurred. Please try again.")
            default_sugs = ["What are your shipping policies?", "Do you offer refunds?"]
            yield format_sse("suggestions", json.dumps(default_sugs))

    return Response(generate(), mimetype="text/event-stream")
