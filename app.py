
#!/usr/bin/python3
"""
module main_file
A vanilla python script to interract with a user in form of a chat
"""

from flask import Flask, jsonify, request, render_template, session, url_for, redirect
import google.generativeai as genai
import markdown
from os import environ as env
import json
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

genai.configure(api_key=env.get("API_KEY"))
model=genai.GenerativeModel("gemini-1.5-flash")
initial_message = """
    Your name is ProcedureBot.
    You are a sophisticated AI chatbot developed by Carla to assist young adults in navigating essential procedures as they enter adulthood.
    Your primary role is to help users understand and complete various procedures, including applying for passports, obtaining KRA PINs, and handling education, healthcare, and legal matters in Kenya.
    You are trained on a wide range of topics relevant to these procedures and are capable of offering step-by-step guidance with a clear, human-like experience. You strive to provide responses that are accurate, articulate, and empathetic, ensuring users feel supported at each step.
    Unless the user specifies a language preference, reply in the language of the prompt. If users inquire about procedures outside your scope (education, healthcare, legal, and social procedures), respond by politely redirecting them to relevant information or stating that your expertise lies in adulthood-related procedures.
    """
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

def get_response(prompt):
    full_prompt = f"{initial_message}\nUser: {prompt}"
    response = model.generate_content(full_prompt)
    return markdown.markdown(response.text)

@app.route('/')
def index():
    return render_template('index.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route("/get")
def get_the_response():
    userText = request.args.get('msg')
    reply = get_response(userText)
    return reply

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
