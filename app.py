from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return(
        f"Home Page<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tops"
    )





if __name__ == "__main__":
    app.run(debug=True)