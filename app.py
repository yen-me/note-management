# Flask with SQLAlchemy

from distutils.log import debug
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///note.db'
# /// relative path, //// absolute path
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        note_content = request.form['content_input']
        new_note = Todo(content=note_content)

        try:
            db.session.add(new_note)
            db.session.commit()
            return redirect('/')
        except:
            return ("There's error adding your note.")

    else:
        notes = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', notes=notes)


@app.route('/delete/<int:id>')
def delete(id):
    note_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return ("There's error deleting your note.")


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    note_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        note_to_update.content = request.form['content_input']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return ("There's error updating your note.")

    else:
        return render_template('update.html', note_to_update=note_to_update)


if __name__ == "__main__":
    app.run(debug=True)
