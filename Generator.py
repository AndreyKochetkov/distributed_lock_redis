from time import sleep
from faker import Factory


class Generator:
    """ generate messages

    Variables:
        amount_of_messages: app generate this number of messages and become handler
        loop_for_update_lock: app generate this number of messages and update its lock
        key_of_queue: string key of queue where save messages
        life_time_of_lock: time in seconds - how much time lock by this copy of app will be set

    Attributes:
        cursor: class 'redis.client.StrictRedis', cursor for connection to redis
        id_of_gen: a number of this copy of application from redis
    """
    amount_of_messages = 10000000
    loop_for_update_lock = 5
    key_of_queue = "queue"
    life_time_of_lock = 5

    def __init__(self, cursor, id_of_gen):
        """ Init Generator class with arguments

        Args:
            cursor: class 'redis.client.StrictRedis', cursor for connection to redis
            id_of_gen: a number of this copy of application from redis
        """
        self.cursor = cursor
        self.id_of_gen = id_of_gen

    
    def generate_messages(self):
        """ Public function for handle messages

        Returns:
            None
        Raises:
            redis.exceptions.ConnectionError: connection to redis is failed
            Exception: when set or update lock if failed
        """
        self._set_lock(True)  # set lock

        fake = Factory.create()  # for random text
        for i in range(Generator.amount_of_messages):  # all messages of this generator
            for j in range(Generator.loop_for_update_lock):  # messages for update lock
                sleep(0.5)
                message = fake.text(max_nb_chars=100)
                self.cursor.rpush(Generator.key_of_queue, message)
                print(message)  # TODO: delete it from release version

            self._set_lock(False)  # update lock

    def _set_lock(self, nx=True):
        """ set or update distributed lock

        Args:
            nx: boolean variable, that means:
                True - set lock, only if it doesn't exist
                False - set lock in any case

        Returns:
            None

        Raises:
            Exception: when set or update lock if failed
        """
        status_lock = self.cursor.set("lock", self.id_of_gen, ex=Generator.life_time_of_lock, nx=nx)
        if status_lock is not True:
            raise Exception("Set lock is failed")