import redis
from time import sleep, clock
from random import randint


class Handler:
    amount_of_messages = 10
    current_message_id = 0

    def __init__(self, cursor, id_of_hndl):
        self.cursor = cursor
        self.id_of_hndl = id_of_hndl

    # property?
    def handle_messages(self, key_of_queue):

        for i in range(Handler.amount_of_messages):
            sleep(0.1)
            message = self.cursor.lpop(key_of_queue)
            if randint(0, 20) == 0:
                self._create_error_message(message)
            else:
                self._create_right_message(message)


    def _create_error_message(self, message):
        self.cursor.rpush("errors", message)


    def _create_right_message(self, message):
        self.cursor.hmset("handler:{}".format(self.id_of_hndl),
                          {"message:{}".format(Handler.current_message_id): message})
        Handler.current_message_id += 1
