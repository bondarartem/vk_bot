from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import vk
import random
import database

session = vk.Session(access_token='ce22100ccdf80452cb7954a5233f29a780259973bcca2a2c06dfc6a3cdaf557e091140a8284fe58322ee6')
vk_api = vk.API(session)

@csrf_exempt
def get_message(request):
	body = json.loads(request.body)
	print(body)
	if body == { "type": "confirmation", "group_id": 191803844 }:
    		return HttpResponse("0b3d6863")
	if body["type"] == 'message_new':
		if "payload" in body["object"]["message"]:
			if body["object"]["message"]["payload"] == '{"command":"start"}':
				start(request)
			else:
				user_id = body["object"]["message"]["from_id"]
				group = body["object"]["message"]["payload"]
				database.add_member(group,user_id)
		else:
			talk(request)
	return HttpResponse("ok")

def start(request):
	body = json.loads(request.body)
	user_id = body["object"]["message"]["from_id"]
	message = "Привет, чтобы получать от меня уведомления выбери свою группу из предложенных вариантов"
	keyboard = {
		"one_time": True,
		"buttons": [
			[{
					"action": {
						"type": "text",
						"payload": '{"command":"friends"}',
						"label": "Друзья"
					},
					"color": "primary"
				},
				{
					"action": {
						"type": "text",
						"payload": '{"command":"classmates"}',
						"label": "Одноклассники"
					},
					"color": "primary"
				},
				{
					"action": {
						"type": "text",
						"payload": '{"command":"programmers"}',
						"label": "Программисты"
					},
					"color": "primary"
				}
			]
		]
	}
	vk_api.messages.send(user_id=user_id, message=message, keyboard=json.dumps(keyboard), random_id=random.randint(1,50000000000000000000000) ,v=5.103)

def talk(request):
	body = json.loads(request.body)
	data = database.get_db()
	user_id = body["object"]["message"]["from_id"]
	if body["object"]["message"]["text"].find('/') != -1:
		mes = body["object"]["message"]["text"].split('/')
		database.insert_db(mes[0],mes[1])
		vk_api.messages.send(user_id=user_id, message="Я записал новую фразу", random_id=random.randint(1,50000000000000000000000) ,v=5.103)
	else:
		for i in data:
			if i[1] == body["object"]["message"]["text"]:
				messages = i[2]
				vk_api.messages.send(user_id=user_id, message=messages, random_id=random.randint(1,50000000000000000000000) ,v=5.103)
				break
			elif i == data[-1] and i[1] != body["object"]["message"]["text"]:
				message1 = "Я не понимаю это сообщение"
				message2 = "Напиши мне пару Сообщение/Ответ, если ты хочешь добавить новую фразу. Не забудь разделить их знаком /"
				vk_api.messages.send(user_id=user_id, message=message1, random_id=random.randint(1,50000000000000000000000) ,v=5.103)
				vk_api.messages.send(user_id=user_id, message=message2, random_id=random.randint(1,50000000000000000000000) ,v=5.103)
				break

@csrf_exempt
def admin(request):
    with open('myBotVK/templates/index.html', 'r') as file:
        return HttpResponse(file.read())

@csrf_exempt
def script(request):
    with open('myBotVK/templates/script.js', 'r') as file:
        return HttpResponse(file.read())

@csrf_exempt
def client_server(request):
	body = json.loads(request.body)
	res = {}
	if body['type'] == 'login':
		if (body['username'] == 'admin') and (body['password'] == 'admin'):
			res['correct'] = True
			res['val'] = database.get_groups()
			with open('myBotVK/templates/admin.html', 'r') as file:
				res['html'] = file.read()
		else:
			res['correct'] = False
		#print(res)
		return HttpResponse(json.dumps(res))
	elif body["type"] == 'postNewMessage':
		users_chat_id = database.get_member(body["group"])
		for i in users_chat_id:
			vk_api.messages.send(user_id=i, message=body['content'], random_id = random.randint(1, 50000000000000000000000), v=5.103)
		return HttpResponse(json.dumps({"res": "ok"}))