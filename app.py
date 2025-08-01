from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Aa9767470225'
app.config['MYSQL_DB'] = 'homeharbor'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_property', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        location = request.form['location']
        bedrooms = request.form['bedrooms']
        bathrooms = request.form['bathrooms']
        area_sqft = request.form['area_sqft']
        image_url = request.form['image_url']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO properties
            (title, description, price, location, bedrooms, bathrooms, area_sqft, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (title, description, price, location, bedrooms, bathrooms, area_sqft, image_url))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('add_property.html')

@app.route('/delete/<int:property_id>', methods=['POST'])
def delete_property(property_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM properties WHERE id = %s", (property_id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/listings')


@app.route('/listings')
def listings():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM properties ORDER BY created_at DESC")
    properties = cur.fetchall()
    cur.close()
    return render_template('listings.html', properties=properties)

if __name__ == "__main__":
    app.run(debug=True)
