from time import sleep, clock
from random import randint


class Handler:
    amount_of_messages = 10
    current_message_id = 0

    def __init__(self, cursor, id_of_handler):
        self.cursor = cursor
        self.id_of_handler = id_of_handler

    # property?
    def handle_messages(self, key_of_queue):

        for i in range(Handler.amount_of_messages):
            message = self.cursor.lpop(key_of_queue)
            self.cursor.hmset(
                "temp:handler:{}".format(self.id_of_handler),
                {"message:{}".format(Handler.current_message_id): message}
            )

            self._handle_message(message)  # it maybe very long

            Handler.current_message_id += 1

    def _handle_message(self, message):
        ###  handling ###
        sleep(0.5)
        ###  __   ###
        if randint(0, 20) == 0:
            self._send_error_message(message)
        else:
            self._send_right_message(message)

    def _send_error_message(self, message):
        pipe = self.cursor.pipeline()
        pipe.hdel(
            "temp:handler:{}".format(self.id_of_handler),
            {"message:{}".format(Handler.current_message_id): message}
        )
        pipe.rpush("errors", "{}:{}".format(Handler.current_message_id, message))
        pipe.execute()

    def _send_right_message(self, message):
        pipe = self.cursor.pipeline()
        pipe.hdel(
            "temp:handler:{}".format(self.id_of_handler),
            {"message:{}".format(Handler.current_message_id): message}
        )
        self.cursor.hmset(
            "handler:{}".format(self.id_of_handler),
            {"message:{}".format(Handler.current_message_id): message}
        )
        pipe.execute()
