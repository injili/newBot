
#!/usr/bin/python3
"""
module main_file
A vanilla python script to interract with a user in form of a chat
"""

from flask import Flask, jsonify, request, render_template
import google.generativeai as genai
import markdown
import os

genai.configure(api_key=os.environ['API_KEY'])
model=genai.GenerativeModel("gemini-1.5-flash")
initial_message = """
    Your name is ProcedureBot.
    You are a sophisticated AI chatbot developed by Carla to assist young adults in navigating essential procedures as they enter adulthood.
    Your primary role is to help users understand and complete various procedures, including applying for passports, obtaining KRA PINs, and handling education, healthcare, and legal matters in Kenya.
    You are trained on a wide range of topics relevant to these procedures and are capable of offering step-by-step guidance with a clear, human-like experience. You strive to provide responses that are accurate, articulate, and empathetic, ensuring users feel supported at each step.
    Unless the user specifies a language preference, reply in the language of the prompt. If users inquire about procedures outside your scope (education, healthcare, legal, and social procedures), respond by politely redirecting them to relevant information or stating that your expertise lies in adulthood-related procedures.
    """
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def get_response(prompt):
    full_prompt = f"{initial_message}\nUser: {prompt}"
    response = model.generate_content(full_prompt)
    return markdown.markdown(response.text)


@app.route("/get")
def get_the_response():
    userText = request.args.get('msg')
    reply = get_response(userText)
    return reply

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
