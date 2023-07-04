from flask import Flask
import psycopg2

# Establish a connection to the PostgreSQL database
while True:
    try:
        connection = psycopg2.connect(
            host="db",
            port="5432",
            user="root",
            password="123",
            database="scrapy"
        )

        break
    except:
        pass

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Create a Flask web application
app = Flask(__name__)

# Route for the homepage


@app.route('/')
def home():
    cursor.execute("SELECT * FROM books LIMIT 300")

    records = cursor.fetchall()

    html = "<h1>Books by Mark!</h1>"
    html += "<title>Books!!!!!!</title>"

    for record in records:
        html += f"""
            <p>
                <img src="{record[1]}" />
                <h4>{ record[2] }</h4>
            </p>
        """

    # Return the HTML response
    return html


# Run the Flask application on port 8080
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
