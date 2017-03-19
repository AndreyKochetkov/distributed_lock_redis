from time import sleep, clock
from faker import Factory


class Generator:
    amount_of_messages = 10000000
    loop_for_update_lock = 5
    key_of_queue = "queue"

    def __init__(self, cursor, id_of_gen):
        self.cursor = cursor
        self.id_of_gen = id_of_gen

    # property?
    def generate_messages(self):

        self._set_lock(True)

        fake = Factory.create()
        for i in range(Generator.amount_of_messages):  # all messages of this generator
            for j in range(Generator.loop_for_update_lock):  # messages for update lock
                sleep(0.1)
                message = fake.text(max_nb_chars=100)
                self.cursor.rpush(Generator.key_of_queue, message)
                print(message)

            self._set_lock(False)  # update lock

    def _set_lock(self, nx=True):
        status_lock = self.cursor.set("lock", self.id_of_gen, ex=5, nx=nx)
        if status_lock is not True:
            raise Exception("Set lock is failed")
