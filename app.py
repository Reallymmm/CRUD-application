from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'flash message'

# Настройки SQLite
app.config['DATABASE'] = 'crud_flask_app.db'


def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    if not os.path.exists(app.config['DATABASE']):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                city TEXT,
                pincode TEXT
            )
        ''')
        conn.commit()
        conn.close()


@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('app.html', students=students)


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        flash('Данные успешно добавлены')
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        city = request.form['city']
        pincode = request.form['pincode']

        conn = get_db_connection()
        conn.execute('INSERT INTO students (name, email, phone, address, city, pincode) VALUES (?, ?, ?, ?, ?, ?)',
                     (name, email, phone, address, city, pincode))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        city = request.form['city']
        pincode = request.form['pincode']

        conn = get_db_connection()
        conn.execute("""
            UPDATE students
            SET name=?, email=?, phone=?, address=?, city=?, pincode=?
            WHERE id=?
        """, (name, email, phone, address, city, pincode, id_data))
        flash("Данные успешно обновлены")
        conn.commit()
        conn.close()
        return redirect(url_for('index'))


@app.route('/delete/<string:id_data>', methods=['POST', 'GET'])
def delete(id_data):
    flash("Запись успешно удалена")
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id=?", (id_data,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)