from time import sleep, clock
from Generator import Generator
from Handler import Handler
import redis

def main():
    host = "localhost"
    port = 6379
    db = 0

    cursor = redis.StrictRedis(host=host, port=port, db=db)

    id_of_instance = cursor.incr("amount_of_instances")

    generator = Generator(cursor, id_of_instance)
    try:
        generator.generate_messages()
    except Exception as e:
        print("Error: " + str(e))

    handler = Handler(cursor, id_of_instance)

    try:
        while True:
            handler.handle_messages(Generator.key_of_queue)
            try:
                generator.generate_messages()
            except Exception as e:
                print("Try of capture lock \n Error: " + str(e))

    except Exception as e:
        print("Error: " + str(e))
    print("усе")




if __name__ == "__main__":
    main()
