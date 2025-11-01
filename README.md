# CI-CHATBOT-PROJECT

              Ecommerce Customer Service ChatBot 

GROUP MEMBERS
NAME : NAEEM SHAH
REG-NO :21PWBCS0842
NAME :MUHAMMAD SHAHID
REG-NO :21PWBCS0846
NAME :ZEESHAN AHMAD
REG-NO :21PWBCS0838


# E-Shop Assistant Chatbot

## Overview
E-Shop Assistant is a chatbot tailored for e-commerce platforms, providing quick assistance for common customer inquiries such as order tracking, return policies, and shipping information. Built using **Flask** for the backend and **HTML/CSS/JavaScript** for a modern, interactive frontend, the assistant ensures seamless user interactions.

---

## Features

### Chat Interface
- Smooth, responsive UI designed with **Tailwind CSS**.
- Supports dynamic, real-time updates for messages and suggestions.

### Backend
- **Flask-powered API** leveraging **SSE** for streaming responses.
- Fuzzy matching with `thefuzz` for better query resolution.
- Easily extensible with customizable datasets.

### Suggestions and Contextual Responses
- Provides context-aware suggestions based on user input.
- Displays frequently asked questions on page load for quick access.



## Customization

### Frontend
1. Modify the chatbot’s interface by editing `index.html`.
2. Use **Tailwind CSS** for additional styling.

### Backend
1. Add new FAQs in `ecommerce_chatbot_dataset.json`:
   ```json
   {
     "questions": ["How do I track my package?"],
     "answer": "Log in to your account and visit the 'Track Order' page for updates.",
     "category": "shipping"
   }
   ```
2. Update response logic in `chatbot.py` if necessary.

---

## Future Enhancements
1. **Multilingual Support:**
   - Allow conversations in multiple languages.
2. **GPT-4 Integration:**
   - Leverage OpenAI’s latest models for smarter, more conversational responses.
3. **Personalized Assistance:**
   - User-specific suggestions based on history and preferences.
4. **Enhanced API Integrations:**
   - Add hooks for shipping carriers, payment systems, or CRM platforms.

---
