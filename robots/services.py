import datetime


def string_validate_and_convert_to_datetime(datetimestr: str) -> None | datetime.datetime:
    try:
        return datetime.datetime.strptime(datetimestr, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return

