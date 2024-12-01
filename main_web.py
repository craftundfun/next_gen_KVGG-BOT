import os

# important
import pymysql
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from database.Domain.BaseClass import Base
from database.Domain.DiscordUser.Entity.DiscordUser import DiscordUser

pymysql.install_as_MySQLdb()

from dotenv import load_dotenv
load_dotenv()

# Initialisiere die Flask App und die Datenbank
app = Flask(__name__)

db = SQLAlchemy(model_class=Base)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'mysql://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_HOST")}/{os.getenv("DATABASE_NAME")}'

db.init_app(app)


# Route für die Homepage
# Route für die Homepage
@app.route('/')
def index():
    posts = db.session.execute(select(DiscordUser)).scalars().all()  # Alle Posts aus der Datenbank abrufen
    return render_template('index.html', posts=posts)


# Route für das Erstellen eines neuen Posts
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = DiscordUser(discord_id=int(title), global_name=content)
        db.session.add(new_post)
        db.session.commit()  # Speichern in der Datenbank
        return redirect(url_for('index'))  # Zurück zur Startseite
    return render_template('create.html')


# Route zum Löschen eines Posts
@app.route('/delete/<int:id>')
def delete(id):
    post_to_delete = db.session.query(DiscordUser).get_or_404(id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('index'))


# Main-Block, um die App auszuführen
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
