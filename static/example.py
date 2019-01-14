import MySQLdb
from aiohttp import web
import json


db = MySQLdb.connect(host="localhost", user="root", passwd="", db="task_list")

cur = db.cursor()
cur.execute("SELECT id FROM TASKS")

for row in cur.fetchall():
    print(row[0])


async def new_user(request):
    try:
        user = await request.json()
        print('Creating a new user with name: ', user['name'])

        response_obj = {'status': 'success', 'message': 'user successfully created'}
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        print(e)
        response_obj = {'status': 'failed', 'message': str(e)}
        return web.Response(text=json.dumps(response_obj), status=500)


app = web.Application()
app.add_routes([web.post('/room/create', new_user)])

web.run_app(app)