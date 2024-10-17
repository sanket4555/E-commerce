from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

# Configure the Gemini API client
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    raise Exception("API key not found! Please set the GOOGLE_API_KEY in your environment.")

# Initialize the Gemini Pro model and chat session
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get a response from the Gemini model
def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        return str(e)

# Define the routes
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/blog", methods=["GET"])
def blog():
    return render_template("blog.html")

@app.route("/cart", methods=["GET"])
def cart():
    return render_template("cart.html")
 
@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")

@app.route("/shop", methods=["GET"])
def shop():
    return render_template("shop.html")

@app.route("/sproduct", methods=["GET"])
def sproduct():
    return render_template("sproduct.html")

@app.route("/index", methods=["GET", "POST"])
def index():
    latest_answer = ""
    if request.method == "POST":
        input_text = request.form.get("input_text")
        if input_text:
            response = get_gemini_response(input_text)
            
            # Handle the response depending on its structure
            if isinstance(response, str):
                # An error occurred
                latest_answer = response
            else:
                # Assuming response is an iterable of chunks
                latest_answer = ""
                for chunk in response:
                    latest_answer += chunk.text
            
            return render_template("index.html", latest_answer=latest_answer)
        else:
            flash("Please enter a question.")
            return redirect(url_for('index'))
    return render_template("index.html", latest_answer=latest_answer)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
