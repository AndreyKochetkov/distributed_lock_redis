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
    parser.add_argument("--cleanTemp",
                        type=str,
                        default=None,
                        help="clean trash files from db - send \'yes\' ")
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


def clean_db(cursor, count_of_instances):
    """ Save all trash messages to queue with non handled and delete them from temp queue

    Args:
        cursor: class 'redis.client.StrictRedis', cursor for connection to redis
        count_of_instances: amount of instances of this app from redis

    Returns:
        None: when list of temp messages will be empty
    """
    for i in range(count_of_instances):
        messages = cursor.hgetall("temp:handler:{}".format(i))
        for k in messages.keys():
            cursor.rpush("queue", messages[k])
            cursor.hdel(
                "temp:handler:{}".format(i),
                k
            )
            print(k)
