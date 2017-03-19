import redis

import sys
from Generator import Generator
from Handler import Handler
from utils import create_parser, get_errors


def main():
    parser = create_parser()
    namespace = parser.parse_args()



    host = namespace.host
    port = namespace.port
    db = namespace.db

    try:
        cursor = redis.StrictRedis(host=host, port=port, db=db)
        id_of_instance = cursor.incr("amount_of_instances")
    except Exception as e:
        print("Error: connection to db failed \n" + str(e))
        sys.exit()

    if namespace.getErrors is not None:
        get_errors(cursor)
        sys.exit()

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


if __name__ == "__main__":
    main()
