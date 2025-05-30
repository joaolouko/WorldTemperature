from flask import Flask, request, redirect, render_template_string
import os
from pymongo import MongoClient

app = Flask(__name__)

#connection

client = MongoClient('mongodb+srv://pires:13795272@perezdb.mfxofrn.mongodb.net/?retryWrites=true&w=majority&appName=perezdb')
db = client['worldTemperature']
collection = db['worldtemp']

# In-memory "database" (cleared when server restarts)
posts = []

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>World Temperature Board</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #74ebd5, #ACB6E5);
            margin: 0;
            padding: 20px;
        }
        h1, h2 {
            text-align: center;
            color: #333;
        }
        form {
            background: white;
            padding: 20px;
            border-radius: 10px;
            max-width: 400px;
            margin: 20px auto;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #45a049;
        }
        .post {
            background: white;
            padding: 15px;
            margin: 10px auto;
            max-width: 500px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .temperature {
            font-size: 24px;
            color: #ff5722;
        }
    </style>
</head>
<body>
    <h1>🌎 Share Your Temperature!</h1>
    <form method="POST">
        <input type="text" name="name" placeholder="Your Name" required><br>
        <input type="text" name="location" placeholder="Your Location" required><br>
        <input type="number" name="temperature" placeholder="Temperature (°C)" required><br>
        <button type="submit">Share</button>
    </form>
    <hr>
    <h2>🌡️ Live Temperature Feed</h2>
    {% for post in posts %}
        <div class="post">
            <p><strong>{{ post['name'] }}</strong> from <strong>{{ post['location'] }}</strong>:</p>
            <p class="temperature">{{ post['temperature'] }}°C</p>
        </div>
    {% endfor %}
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")
        temperature = request.form.get("temperature")

        collection.insert_one({
            "name": name,
            "location": location,
            "temperature": temperature
        })
        return redirect("/")

    posts = list(collection.find().sort("_id", -1))
    return render_template_string(HTML_PAGE, posts=posts)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get the PORT from environment
    app.run(host="0.0.0.0", port=port, debug=True)
