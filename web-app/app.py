from flask import Flask, request, render_template, redirect
from flask_pymongo import PyMongo, ObjectId
import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/notesDB"
mongo = PyMongo(app)

# home page
@app.route('/')
def home():
    #get the notes from the database
    notes = list(mongo.db.notes.find({}).sort("createdAt",-1))
    print(notes)
    # return "<p>The home page</p>"
    return render_template("/pages/home.html", homeIsActive=True,addNoteIsActive=False,notes=notes)

@app.route('/add-note', methods=['GET','POST'])
def add_note():
    if (request.method == 'GET'):
        # return "<p>Add note page</p>"
        return render_template("/pages/add-note.html",homeIsActive=False,addNoteIsActive=True)
    elif (request.method == 'POST'):
        # logic
        title = request.form['title']
        description = request.form['description']
        createdAt = datetime.datetime.now()
        mongo.db.notes.insert_one({"title": title, "description": description, "createdAt": createdAt})
        return redirect("/")

@app.route('/edit-note', methods=['GET','POST'])
def edit_note():
    if (request.method == 'GET'):
        # return "<p>Edit note page</p>"
        note_id = request.args.get('form')
        note = dict(mongo.db.notes.find_one({"_id": ObjectId(note_id)}))
        return render_template("/pages/edit-note.html", note=note)
    elif (request.method == 'POST'):
        # get data of the note
        note_id = request.form['_id']
        note_desc = request.form['description']
        note_title = request.form['title']

        # update data in db
        mongo.db.notes.update_one({"_id": ObjectId(note_id)}, {"$set": {"title": note_title,
        "description": note_desc}})

        # redirect to home pageasdf
        return redirect("/")

@app.route('/delete-note', methods=['POST'])
def delete_note():
    note_id = request.form['_id']
    mongo.db.notes.delete_one({"_id": ObjectId(note_id)})
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)