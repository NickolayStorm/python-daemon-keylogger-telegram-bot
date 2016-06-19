import telepot
import time
import datetime
# import logging


TOKEN = 'Your Telegram bot TOKEN'

# Job Q for reading message updates


class TGBot():
    def __init__(self, q):
        self.bot = telepot.Bot(TOKEN)
        self.chat_ids = []
        self.q = q

        def loop():
            print("loop")
            if not self.q.empty():
                msg = self.q.get()
                self.send_messages(msg)
        
        self.bot.message_loop(self.handle)
        while 1:
            time.sleep(3)
            loop()

    def send_messages(self, text):
        for i in self.chat_ids:
            self.bot.sendMessage(i, text)

    def follow(self, chat_id):
        if chat_id in self.chat_ids:
            return
        self.bot.sendMessage(chat_id, "Hey! Now you have started to monitor my creator's keyboard")
        self.chat_ids.append(chat_id)

    def handle(self, msg):
        chat_id = msg['chat']['id']
        command = msg['text']

        print('Got command: %s' % command)

        if command == '/follow':
            self.follow(chat_id)
        elif command == '/unfollow':
            self.unfollow(chat_id)


    def unfollow(self, chat_id):
        if chat_id in self.chat_ids:
            self.bot.sendMessage(chat_id, "See you later!")
            self.chat_ids.remove(chat_id)
        else:
            self.bot.sendMessage(chat_id, "At first You should use the command /follow to start to recieve messages")

