import pyodbc
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

connection_string = r'Driver={SQL Server};Server=WIN-SPFE3KCRJES;Database=test;Trusted_Connection=yes;'


def create_connection():
    return pyodbc.connect(connection_string)


def insert_data(first_name, last_name, phone_number, email, service_name):
    with create_connection() as connection:
        cursor = connection.cursor()
        query = "INSERT INTO Kalina (first_name, last_name, phone_number, email, service_name) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (first_name, last_name, phone_number, email, service_name))
        connection.commit()


def get_services():
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT name FROM Service')
        services = [row[0] for row in cursor.fetchall()]
    return services


@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone_number = data.get('phone_number')
    email = data.get('email')
    service_name = data.get('service')

    insert_data(first_name, last_name, phone_number, email, service_name)

    return redirect(url_for('index', modal=True))


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/', methods=['GET'])
def index():
    services = get_services()
    return render_template('base.html', services=services)


if __name__ == "__main__":
    app.run(debug=True)
