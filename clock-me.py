import sqlite3
from flask import Flask, render_template, url_for, redirect
import datetime

app = Flask(__name__)

connection =  sqlite3.connect("data.sql")
cursor = connection.cursor()




def update_tables(now): 
    cursor.execute("select * from dates;")
    existing_dates = cursor.fetchall()
    if (now,) not in existing_dates: 
        cursor.execute("INSERT INTO dates VALUES ('" + now + "');")
        cursor.execute("INSERT INTO data VALUES ('" + now + "', 0, 0);")
        connection.commit()



@app.route('/')
@app.route('/home')
def home():
    now = datetime.datetime.now().strftime("%x")
    update_tables(now)
    cursor.execute("SELECT sum(productive) FROM data;")
    total_productive = cursor.fetchall() 
    cursor.execute("SELECT sum(fun) FROM data;")
    total_fun = cursor.fetchall() 
    cursor.execute("SELECT productive FROM data WHERE date = '" + now + "';")
    today_productive = cursor.fetchall() 
    cursor.execute("SELECT fun FROM data WHERE date = '" + now + "';")
    today_fun = cursor.fetchall()
    return render_template("home.html", total_productive=total_productive[0][0], total_fun=total_fun[0][0], today_productive=today_productive[0][0], today_fun=today_fun[0][0], now=now)

@app.route('/add_one_productive')
def add_one_productive():
    now = datetime.datetime.now().strftime("%x")
    update_tables(now)
    cursor.execute("UPDATE data SET productive = productive + 1 WHERE date = '" + now + "';")
    connection.commit()
    return redirect(url_for("home"))

@app.route('/minus_one_productive')
def minus_one_productive():
    now = datetime.datetime.now().strftime("%x")
    update_tables(now)
    cursor.execute("UPDATE data SET productive = productive - 1 WHERE date = '" + now + "';")
    connection.commit()
    return redirect(url_for("home"))

@app.route('/add_one_fun')
def add_one_fun():
    now = datetime.datetime.now().strftime("%x")
    update_tables(now)
    cursor.execute("UPDATE data SET fun = fun + 1 WHERE date = '" + now + "';")
    connection.commit()
    return redirect(url_for("home"))

@app.route('/minus_one_fun')
def minus_one_fun():
    now = datetime.datetime.now().strftime("%x")
    update_tables(now)
    cursor.execute("UPDATE data SET fun = fun - 1 WHERE date = '" + now + "';")
    connection.commit()
    return redirect(url_for("home"))