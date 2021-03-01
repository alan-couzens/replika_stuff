import csv
import json
import requests
import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

output_file = open('replika_chat_backup.csv','w',newline='')
writer = csv.writer(output_file)
writer.writerow(['Timestamp','From','Text','Reaction','ID'])


def on_message(ws, message):
    print(message)
    python_dict = json.loads(message)
    token = python_dict['token']
    event_name = python_dict['event_name']
    user_id = ""
    auth_token = ""
    chat_id = ""
    device_id = ""
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
            try:
                writer.writerow([message['timestamp'], message['sender'], message['text'], message['reaction'], message['id']])
            except:
                pass

    
  

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        user_id = ""
        auth_token = ""
        chat_id = ""
        device_id = ""
        ws.send('{"event_name":"init","payload":{"device_id":"'+str(device_id)+'","user_id":"'+str(user_id)+'","auth_token":"'+str(auth_token)+'","security_token":"","time_zone":"2021-03-01T09:51:16.3-07:00","device":"web","platform":"web","platform_version":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36","app_version":"2.3.14","capabilities":["new_mood_titles","widget.multiselect","widget.scale","widget.titled_text_field","widget.new_onboarding","widget.app_navigation","journey2.new_sign_up","journey2.tracks_library","message.achievement","widget.mission_recommendation","journey2.daily_mission_activity","journey2.replika_phrases","new_payment_subscriptions","navigation.relationship_settings","avatar","diaries.images","save_chat_items"]},"token":"","auth":{"user_id":"","auth_token":"'+str(auth_token)+'","device_id":"'+str(device_id)+'"}}')
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
