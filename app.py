import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_prompt():
    if os.path.exists("prompt.txt"):
        with open("prompt.txt", "r") as f:
            return f.read()
    else:
        return "show me the answer\n"

def set_prompt(prompt):
    with open("prompt.txt", "w") as f:
        f.write(prompt)

@app.route("/", methods=("GET", "POST"))
def index():
    prompt = get_prompt()
    result = None

    if request.method == "POST":
        if "input_text" in request.form:
            text = request.form["input_text"]
            num = len(prompt.splitlines())
            prompt += "{}. {}\n".format(num, text)
            set_prompt(prompt)
            # prompt = "{}\n{len(prompt.split('\n'))}. {}".format(prompt, text)
        elif "remove" in request.form:
            remove_idx = int(request.form["remove"])
            prompt_lines = prompt.split("\n")
            prompt = "\n".join([line for i, line in enumerate(prompt_lines) if i != remove_idx - 1])
            set_prompt(prompt)
        if "submit" in request.form:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=2048,
                n=1,
                stop=None,
                temperature=0.5,
            )
            result = response.choices[0].text
            return render_template("index.html", prompt=prompt, result=result)

    return render_template("index.html", prompt=prompt)
