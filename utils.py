import argparse


def create_parser():
    """ Create parser for command-line arguments

    Returns:
        instance of argparse.ArgumentParser . It has all command-line arguments: host, port, db, getErrors.
        If they haven't been sent, they will be set by default values
    """
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
    """ Print all error messages and delete them from redis

    Args:
        cursor: class 'redis.client.StrictRedis', cursor for connection to redis

    Returns:
        None: when list of error will be empty
    """
    while True:
        message = cursor.lpop("errors")
        if message is None:
            print("There are no errors more")
            return None
        print(message)
