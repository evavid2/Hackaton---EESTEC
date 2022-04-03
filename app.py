import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        recipient = request.form["recipient"]
        affiliation = request.form["affiliation"]
        purpose = request.form["purpose"]
        signature = request.form["signature"]
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=generate_prompt(recipient, affiliation, purpose, signature),
            temperature=0.6,
            max_tokens=2000
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    print(result)
    return render_template("index.html", result=result)


def generate_prompt(recipient, affiliation, purpose, signature):
    return """Write a polite e-mail to the correct recipient and with the correct purpose. Omit rude words. Use kind and constructive language. Include opening and closing line.

Recipient: {}
Affiliation: {}
Purpose: {}
Signature: {}
Generated e-mail:""".format(recipient, affiliation, purpose, signature)
