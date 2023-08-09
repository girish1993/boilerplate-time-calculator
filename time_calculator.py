from lib.TimeCalculator import TimeCalculator
from lib.TimeSeparator import TimeSeparator


def add_time(start, duration):

    time_separtor = TimeSeparator()
    time_calcutor = TimeCalculator()

    time_separtor.set_next(time_calcutor)

    result = time_separtor.handle(start=start, duration=duration)

    # return new_time


add_time("11:06 PM", "2:02")
