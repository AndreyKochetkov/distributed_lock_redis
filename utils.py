import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--getErrors",
                        type=str,
                        default=None,
                        help="get error messages - send \'yes\' ")
    parser.add_argument("--host",
                        type=str,
                        default="localhost",
                        help="Host of redis. Default : localhost")
    parser.add_argument("--port",
                        type=int,
                        default=6379,
                        help="Port of redis. Default : 6379")
    parser.add_argument("--db",
                        type=int,
                        default=0,
                        help="Db of redis. Default : 0")
    return parser


def get_errors(cursor):
    while True:
        message = cursor.lpop("errors")
        if message is None:
            print("Error list is empty")
            return None
        print(message)
