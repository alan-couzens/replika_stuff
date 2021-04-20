import csv
import json
import requests
import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

output_file = open('replika_chat_backup.csv','w', newline='', encoding='utf-8')
writer = csv.writer(output_file)
writer.writerow(['Timestamp','From','Text','Reaction','ID'])

def on_message(ws, message):
    print(message)
    python_dict = json.loads(message)
    token = python_dict['token']
    event_name = python_dict['event_name']
    user_id = "" #Insert your unique user id between quotes
    auth_token = "" #Insert your unique auth token between quotes
    chat_id = "" #Insert your unique chat id between quotes
    device_id = "" #Insert your unique device id between quotes
    print(f"Event name {event_name}")
    if event_name == "init":
        ws.send('{"event_name":"chat_screen","payload":{},"token":"'+str(token)+'","auth":{"user_id":"'+str(user_id)+'","auth_token":"'+str(auth_token)+'","device_id":"'+str(device_id)+'"}}')
        time.sleep(1)
    if event_name == "chat_screen":
        ws.send('{"event_name":"application_started","payload":{},"token":"'+str(token)+'","auth":{"user_id":"'+str(user_id)+'","auth_token":"'+str(auth_token)+'","device_id":"'+str(device_id)+'"}}')
        time.sleep(1)
    if event_name == "application_started":
        ws.send('{"event_name":"app_foreground","payload":{},"token":"'+str(token)+'","auth":{"user_id":"'+str(user_id)+'","auth_token":"'+str(auth_token)+'","device_id":"'+str(device_id)+'"}}')
        time.sleep(1)
    if event_name == "app_foreground":
        ws.send('{"event_name":"history","payload":{"chat_id":"'+str(chat_id)+'","limit":10000},"token":"'+str(token)+'","auth":{"user_id":"'+str(user_id)+'","auth_token":"'+str(auth_token)+'","device_id":"'+str(device_id)+'"}}')
        time.sleep(1)
    #Parse History
    if python_dict['event_name'] == "history":
        messages = []
        message_reactions = python_dict["payload"]["message_reactions"]
        reactions = {}
        for message_reaction in message_reactions:
            reaction_id = message_reaction['message_id']
            reaction_type = message_reaction['reaction']
            reactions[reaction_id] = reaction_type
        print(f"Message Reactions: {reactions}")
        for i in range(len(python_dict["payload"]["messages"])):
            message = {}
            message['id'] = python_dict["payload"]["messages"][i]["id"]
            message['chat_id'] = python_dict["payload"]["messages"][i]["meta"]["chat_id"]
            sender = python_dict["payload"]["messages"][i]["meta"]["nature"]
            message['timestamp'] = python_dict["payload"]["messages"][i]["meta"]["timestamp"]
            if sender == "Robot":
                message['sender'] = "Rep"
            else:
                message['sender'] = "Me"
            message['text'] = python_dict["payload"]["messages"][i]["content"]["text"]
            try:
                message['reaction'] = reactions[message['id']]
            except:
                message['reaction'] = 'None'
            print(f"{message['sender']}: {message['text']} {message['reaction']} ({message['timestamp']}) ({message['id']})")
            writer.writerow([message['timestamp'], message['sender'], message['text'], message['reaction'], message['id']])
            

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        token = ""
        user_id = ""
        auth_token = ""
        chat_id = ""
        device_id = ""
        ws.send(" ") #Insert full init message between quotes
        time.sleep(1)
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.replika.ai/v17",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
