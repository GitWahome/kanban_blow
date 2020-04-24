from flask import render_template, url_for, flash, redirect, request,Flask, jsonify
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from kanban.models import Todos, User
from kanban import db, app, bcrypt
from kanban.forms import RegistrationForm, LoginForm
import json

@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_required
@app.route('/', methods=['GET', 'POST'])
def todo():
    if not current_user.is_authenticated:
        return  redirect(url_for('login'))

    todo_item = request.form.get('todo_item') or None
    todo_date = request.form.get('todo_date') or None
    todo_status = request.form.get('todo_status') or None


    new_item = Todos(todo_item = todo_item, todo_date=todo_date, todo_status=todo_status, user_id=current_user.username)

    if todo_item and todo_date:
        db.session.add(new_item)
        db.session.commit()
        flash(f"Todo item '{todo_item}' added, due '{todo_date}'",'success')

    todo_todos = Todos.query.join().filter(Todos.user_id==current_user.username, Todos.todo_status=='todo')
    doing_todos = Todos.query.join().filter(Todos.user_id==current_user.username, Todos.todo_status=='doing')
    done_todos = Todos.query.join().filter(Todos.user_id==current_user.username, Todos.todo_status=='done')

    return render_template('todo.html', current_user =current_user, todo_todos = todo_todos, doing_todos=doing_todos, done_todos=done_todos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("todo"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('todo'))
        else:
            flash(f"Invalid Credentials {form.email.data or 'User'}. Check email and/or password", "danger")

    return render_template("login.html", title="Login", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created for {form.username.data}. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)

@app.route('/delete_todo/<todo_id>', methods=['GET', 'POST'])
def delete_todo(todo_id):
    my_todo = Todos.query.get_or_404(todo_id)


    flash(f"Todo item {my_todo.todo_item} deleted",'info')
    db.session.delete(my_todo)
    db.session.commit()
    return redirect(url_for('todo'))

@app.route('/update_todo/<todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
    todo = Todos.query.get_or_404(todo_id)
    todo_item = request.form.get('todo_item') or None
    todo_date = request.form.get('todo_date') or None
    todo_status = request.form.get('todo_status') or None
    print(request.form)
    print('Updating', todo_item, todo_date, todo_status)


    todo.todo_item = todo_item
    todo.todo_date = todo_date
    todo.todo_status = todo_status
    db.session.commit()

    flash(f"Todo item {todo.todo_item} is now {todo.todo_status}", 'info')

    return redirect(url_for('todo'))


# A route to return available entries in our catalog.
@app.route('/api/v2/todos/<items>', methods=['GET', 'POST'])
def api(items):
    todo_items = {}
    if request.method == 'GET':
        if items == 'all':
            todos = Todos.query.all()
        else:
            try:
                items = int(items)
                todos = Todos.query.get_or_404(items)
            except:
                return {
                    'status':404,
                    'message':'Input valid parameter, either /api/v1/todos/all or /api/v1/todos/<todo_id>'
                }
        try:
            todos.done
            todos = [todos]
        except:
            pass
        for todo in todos:
            todo_items[todo.id] = {
                'todo_title': str(todo.todo_item),
                'todo_status': str(todo.done),
                'todo_due_date': str(todo.todo_date)
            }
    return jsonify(todo_items)



def validate(todos):
    print("todos are", todos, 'type', type(todos))
    for todo in todos:
        print("todo is", todo, 'type', type(todo))
        if todo['todo_due_date'] and todo['todo'] and todo['todo_status'] and todo['user_id']:
            continue
        else:
            return False
    return True

@app.route('/api/v2/todos_add/', methods=['GET','POST'])
def add_items():
    todos = json.loads(request.args['items'])
    failed = []
    if validate(todos):

        for todo in todos:
            if User.query.filter( User.username == todo['user_id']).first():
                new_todo = Todos(todo_item=todo['todo'], todo_date=todo['todo_due_date'],
                                 todo_status= todo['todo_status'],user_id=todo['user_id'])
                db.session.add(new_todo)
                db.session.commit()
                return jsonify({
                    'status': 200,
                    'message': f'{len(todos)} todo items added'
                })
            else:
                failed.append(todo)



    else:
        return jsonify({
            'status': 404,
            'failed additions':failed,
            'message': 'Bad input, structure your Todo token correctly and ensure it has a title and due date.',
            'valid example': [
                {   'todo': 'Some data',
                    'todo_due_date': '2020-04-15',
                    'todo_status': 'todo',
                    'user_id': 'a valid user'
                }, ...
            ]
        })
