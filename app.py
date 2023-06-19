import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

import requests
import random

# Configure application
app = Flask(__name__)
#app.run(debug=True, port 8000)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

city_name = ''
streak = 0

# NEW
# Define the grid size
GRID_SIZE = 4

# Create a grid of buttons
buttons = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template('index.html', buttons = buttons)

@app.route('/button_click', methods=['POST'])
def button_click():
    # Get the coordinates of the clicked button from the request
    row = int(request.form['row'])
    col = int(request.form['col'])

    # Check if the coordinates are within the valid range
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        # Change the color of the clicked button
        buttons[row][col] = not buttons[row][col]

    return ''
@app.route("/about",  methods=["GET", "POST"])
def about():
    return render_template('about.html')

@app.route("/playgame",  methods=["GET", "POST"])
def playgame():
    with open("database.csv", 'r') as f:
        n = f.readlines()
    global city_name
    global streak

    if request.method == 'GET':
        city_num = random.randint(1,100)
        city =  n[city_num].strip().split(',')

        city_name = city[1]
        city_funfact = city[2]
        city_state = city[3]
        pop_2020 = city[7]
        land_area_sqm = city[11]
        
        return render_template('playgame.html', city_funfact = city_funfact, city_state = city_state, pop_2020 = pop_2020, land_area_sqm = land_area_sqm, city_name = city_name)

    elif request.method == 'POST':
        print(streak)
        query = str(request.form.get("guess"))


        if query == city_name:
            streak += 1
            return render_template('congrats.html', streak = streak)
        else:
            temp = streak
            streak = 0
            return render_template('wrong.html', city_name = city_name, streak = temp)






if __name__=="__main__":
    app.run(host=os.getenv('IP', '127.0.0.1'),
            port=int(os.getenv('PORT', 5000)))