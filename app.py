from flask import Flask, render_template, request
from src.pipelines.predict_pipeline import DataFormat, PredictionPipeline

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        data = DataFormat(
            gender=request.form.get("gender", None),
            race_ethnicity=request.form.get("race_ethnicity", None),
            parental_level_of_education=request.form.get("parental_level_of_education", None),
            lunch=request.form.get("lunch", None),
            test_preparation_course=request.form.get("test_preparation_course", None),
            reading_score=request.form.get("reading_score", None),
            writing_score=request.form.get("writing_score", None),
        )

        prediction = PredictionPipeline.predict(data)
        return render_template("index.html", prediction=prediction)
    else:
        return render_template("index.html")

if __name__=="__main__":
    app.run("0.0.0.0", port=5000, debug=True)