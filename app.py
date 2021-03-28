import os

from flask import Flask, render_template, request, send_from_directory, after_this_request

from pipeline.pipeline import GenerateAnalysisDataset

app = Flask(__name__)
app.secret_key = "verysecret"


@app.route("/", methods=["GET"])
def get_main_page():
    patterns = ["email", "credit_card", "iban"]
    return render_template("upload.html", patterns=patterns)


@app.route("/process", methods=["POST"])
def post_main_page():
    path = os.path.join(os.getcwd(), "userFile.csv")
    file = request.files["file"]
    pattern = request.form["pattern"]
    file.save(path)
    GenerateAnalysisDataset(path, pattern)

    @after_this_request
    def remove_files(response):
        os.remove("userFile.csv")
        os.remove(pattern + "_dataset.csv")
        return response

    return send_from_directory(os.getcwd(), pattern + "_dataset.csv")


if __name__ == "__main__":
    app.run(debug=True)
