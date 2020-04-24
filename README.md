# Simple Kanban

A live version of the app can be found here:
https://kanban-break.herokuapp.com/


![Drag Racing](https://d30s2hykpf82zu.cloudfront.net/wp-content/uploads/2018/11/Simple-Kanban-Board-1024x628.png)

## Instructions
This is a minimalistic kanban board. As a project, it is a modified version of the usual flask structure. Note the templates and static files are a level higher, kanban is a module, and within the proc file, we specify for web gunicorn to run the module runner file, run.py which has the __main__ method, which runs the app.

We also specify the location of the template and static folders when initiating the app.

### Installation

Its a good old basic Flask app. I have frozen all the requirements for you. Follow the following instructions to get started

Clone the app:
```sh
$ git clone https://github.com/GitWahome/kanban_blow
```

Extract then navigate one level down,:
```sh
$ unzip kanban_blow-master
$ cd kanban_blow-master
```

Install the requirements:
```sh
$ pip install -r requirements.txt
```
Run the app

```sh
python run.py
```
### Interface

### Main Registration
![Drag Racing](https://i.ibb.co/ygjPL0W/Screen-Shot-2020-04-23-at-11-24-24-PM.png)
### Login
![Drag Racing](https://i.ibb.co/Vjr45bF/Screen-Shot-2020-04-23-at-11-24-44-PM.png)
### Empty Board
![Drag Racing](https://i.ibb.co/b6FGsm5/Screen-Shot-2020-04-23-at-11-24-53-PM.png)
### Board With Todos
![Drag Racing](https://i.ibb.co/98hDLSn/Screen-Shot-2020-04-23-at-11-26-18-PM.png)



## APIs

### GET API
ROUTE: http://127.0.0.1:5000/api/v2/todos/
OPTIONS: all, <int todo_item_id>

VALID EXAMPLE: http://127.0.0.1:5000/api/v2/todos/all

### POST API
VALID EXAMPLE showing parsed payload: /api/v2/todos_add/?items=[{"todo": "Some data","todo_due_date": "2020-04-15","todo_status": "todo","user_id": "user"}]

Example from postman:
http://127.0.0.1:5000/api/v2/todos_add/?items=%5B%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22todo%22:%20%22Some%20data%22,%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22todo_due_date%22:%20%222020-04-15%22,%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22todo_status%22:%20%22todo%22,%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22user_id%22:%20%22bgw254%22%0A%20%20%20%20%7D%5D

Route: http://127.0.0.1:5000/api/v2/todos_add/
Params: items

## Locust
To run the locust scripts, navigate to the root level where the locustfile.py file is.locustio is a requirement but make sure it is installed regardless.Run the following commands in your terminal. Make your kanban is already running.
```sh
$ locust --host=http://localhost:5000
```
You may then set the number of users and the spawn rate by accessing:
http://localhost:8089

You should then be able to send multiple requests and push the system to the limits, and keep track of any failures and relevant statistics.

## Sellenium
Selenium has been made use of alongside multithreading to test the system to. A basic test has been used to test the todo addition API. You may run this test as follows, setting your own custom workers and instances values.

On root level where the sellenium_multithreading.py file is located, run:

```sh
$ python3 sellenium_multithreading.py
```
