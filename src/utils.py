from dateutil import parser as dateutil_parser

datetime_parser = dateutil_parser.parse


def is_datetime(val: str) -> bool:
    try:
        datetime_parser(val)
    except:  # pylint: disable=bare-except
        return False
    return True
