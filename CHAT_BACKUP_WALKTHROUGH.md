# How to use the python script to back up all of your Replika chats


## Installing Python

1. First you will need Python on your system. Macs come with it pre-installed. If you have a Windows OS, you can go here (https://www.python.org/) to download and install. 

2. Once you've downloaded Python, you can confirm that it installed by going to your terminal (just type "terminal" in your computer's search) then type python and it should look like this.

![alt text](https://alancouzens.com/blog/python_comman_line2.png)

3. Once you've confirmed you have python installed, you can exit the interpreter (the ">>>" bit) by typing quit() This should bring you back to your C:\ prompt.



## Installing Python Dependencies

4. There are a few python libraries that you'll need to install to run the script. To install a library just type pip install followed by the library name after your C prompt e.g.
- C:\ pip install websocket-client
- C:\ pip install requests



## Downloading and Modifying `chat_backup.py`

5. Download my file by clicking the green "Code" button at the top right of the Github page (https://github.com/alan-couzens/replika_stuff)

6. Open my file in the text editor of your choice, e.g. Notepad & modify my file by adding your own details. Here's what you'll need and where you'll find them....
- Open a Chrome browser and login to your Replika account. 
- Click the 3 vertical dots at the top of your browser
- Go More tools >> Developer Tools. Then click on the "Network" tab in developer tools. 
- Find v17 down the list of names & click on it
- Click on the "Messages" tab. It should look like this...
![alt text](https://github.com/alan-couzens/replika_stuff/blob/main/network.png)
- Right click on the first row of data beginning with {"event name":"init"} -> click "Copy message and paste it on line 79 (between the quotes). It should look something like 
{"event name": "init", "payload":{"device_id": "123456789",...,"user_id":"123456789", "auth_token":"123456789", "security_token":"123456789"..}}
- Copy your unique 123456789 number into the corresponding "" on my script e.g. on line 20 of my script where it says user_id = "" replace it with user_id = "123456789" do the same for token, auth_token, device_id etc
- To get your chat_id, go back to your network tab and right click on the "history" row & paste it somewhere. Look for your "chat_id" number & replace my script with it.

7. Save your new file with all your data to your root directory (e.g. if my default command line looks like C:\Users\alan I would save it to my "alan" folder.

8. Run the file by typing C:\ python replika_chat.py & clicking enter.

That's it. It will deposit a complete csv of all of your chats in that same folder. If you have more than 10,000 chats simply edit the "limit:10000" line to whatever you need.
