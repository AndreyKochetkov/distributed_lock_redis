import redis
from time import sleep, clock
from faker import Factory


class Generator:
    amount_of_messages = 10000000
    loop_for_updt_lock = 5

    def __init__(self, host, port, db, id_of_gen):
        self.host = host
        self.port = port
        self.db = db
        self.id_of_gen = id_of_gen

    # property?
    def generate_messages(self):
        cursor = redis.StrictRedis(host=self.host, port=self.port, db=self.db)

        self._set_lock(cursor, True)

        fake = Factory.create()
        for i in range(Generator.amount_of_messages):  # all messages of this generator
            for j in range(Generator.loop_for_updt_lock):  # messages for update lock
                sleep(0.5)
                message = fake.text(max_nb_chars=100)
                cursor.rpush("queue", message)
                print(message)

            self._set_lock(cursor, False)  # update lock

    def _set_lock(self, cursor, nx=True):
        status_lock = cursor.set("lock", self.id_of_gen, ex=5, nx=nx)
        if status_lock is not True:
            raise Exception("Set lock is failed")
