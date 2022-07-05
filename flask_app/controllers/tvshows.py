from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.tvshow import Show
from flask_app.models.user import User


@app.route('/new/show')
def new_show():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
    "id":session['user_id']
    }
    return render_template('new.html',user=User.get_by_id(data))


@app.route('/create/show',methods=['POST'])
def create_show():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_show(request.form):
        return redirect('/new/show')
    data = {
        "title": request.form["title"],
        "network": request.form["network"],
        "release_date": request.form["release_date"],
        "description" : request.form["description"],
        "user_id": session["user_id"]
    }
    Show.save(data)
    return redirect('/dashboard')

@app.route('/edit/show/<int:id>')
def edit_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit.html",edit=Show.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/show',methods=['POST'])
def update_show():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_show(request.form):
        return redirect('/new/show')
    data = {
        "title": request.form["title"],
        "network": request.form["network"],
        "release_date": request.form["release_date"],
        "description": request.form["description"],
        "id": request.form["id"]
    }
    Show.update(data)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def show_new_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "show_id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_tv.html",show=Show.get_one_show_with_posted_by(data),user=User.get_by_id(user_data))

@app.route('/destroy/show/<int:id>')
def destroy_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Show.destroy(data)
    return redirect('/dashboard')