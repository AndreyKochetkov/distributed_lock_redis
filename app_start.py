import redis
import sys

from Generator import Generator
from Handler import Handler
from utils import create_parser, get_errors, clean_db


def main():
    """
    Main function. Enter point of application
    """
    parser = create_parser()
    namespace = parser.parse_args()  # get arguments from parser

    host = namespace.host
    port = namespace.port
    db = namespace.db

    # try to set connection with redis
    try:
        cursor = redis.StrictRedis(host=host, port=port, db=db)
        id_of_instance = cursor.incr("amount_of_instances")
    except redis.exceptions.ConnectionError as e:
        print("Error: connection to db failed \n" + str(e) + str(type(e)))
        sys.exit()

    # if there is a "getErrors" argument
    if namespace.getErrors is not None:
        get_errors(cursor)
        sys.exit()

    if namespace.cleanTemp is not None:
        clean_db(cursor, id_of_instance)
        sys.exit()

    # firstly, try to become a generator
    generator = Generator(cursor, id_of_instance)
    try:
        generator.generate_messages()
    except Exception as e:
        print("Error: " + str(e))

    # secondly, become a handler
    handler = Handler(cursor, id_of_instance)
    try:
        while True:
            # handle Generator.key_of_queue messages
            handler.handle_messages(Generator.key_of_queue)
            try:
                # try to become generator
                generator.generate_messages()
            except Exception as e:
                print("Try of capture lock \n Error: " + str(e))

    except redis.exceptions.ConnectionError as e:
        print("Error: " + str(e))


if __name__ == "__main__":
    main()
