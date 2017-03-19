from time import sleep
from random import randint


class Handler:
    """ handle messages

    Variables:
        amount_of_messages: app handle this number of messages and try to capture lock
        current_message_id: counter for handled and saved messages

    Attributes:
        cursor: class 'redis.client.StrictRedis', cursor for connection to redis
        id_of_handler: a number of this copy of application from redis
    """
    amount_of_messages = 10
    current_message_id = 0

    def __init__(self, cursor, id_of_handler):
        """ Init Handler class with arguments

        Args:
            cursor: class 'redis.client.StrictRedis', cursor for connection to redis
            id_of_handler: a number of this copy of application from redis
        """
        self.cursor = cursor
        self.id_of_handler = id_of_handler

    # property?
    def handle_messages(self, key_of_queue):
        """ Public function for handle messages

        Args:
            key_of_queue: string key of queue with not handled messages
        Returns:
            None
        Raises:
            redis.exceptions.ConnectionError: connection to redis is failed
        """

        # get and handle Handler.amount_of_messages messages
        for i in range(Handler.amount_of_messages):
            message = self.cursor.lpop(key_of_queue)  # get first item in queue
            self.cursor.hmset(  # save it in temp place
                "temp:handler:{}".format(self.id_of_handler),
                {"message:{}".format(Handler.current_message_id): message}
            )

            self._handle_message(message)  # maybe, it will be very long

            Handler.current_message_id += 1

    def _handle_message(self, message):
        """ handle current message

        Args:
            message: string with message

        Returns:
            None
        """
        ###  handling ###
        sleep(1)
        ###  __   ###
        if randint(0, 20) == 0:  # if we have a error with 5% chance
            self._send_error_message(message)
        else:
            self._send_right_message(message)

    def _send_error_message(self, message):
        """ send error message in redis and delete trash from temp place

        Args:
            message: string with message

        Returns:
            None
        """
        pipe = self.cursor.pipeline()
        pipe.hdel(
            "temp:handler:{}".format(self.id_of_handler),
            {"message:{}".format(Handler.current_message_id): message}
        )
        pipe.rpush("errors", "{}:{}".format(Handler.current_message_id, message))
        pipe.execute()

    def _send_right_message(self, message):
        """ send right (non error) message in redis and delete trash from temp place

        Args:
            message: string with message

        Returns:
            None
        """
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