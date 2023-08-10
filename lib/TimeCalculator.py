from handlers.handler import TimeHandler
import math


class TimeCalculator(TimeHandler):
    hour = None
    mins = None
    hour_diff = None
    min_diff = None
    time_format = None
    day = None
    days = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    possible_time_formats = {"AM": "PM", "PM": "AM"}
    return_string = None
    new_hour = None
    new_mins = None
    new_format = None
    new_number_days = None
    day_diff_str = None
    next_handler = None

    def set_next(self, handler):
        self.next_handler = handler

    def handle(self, **request):
        print(request)
        self.hour = request["hour"]
        self.mins = request["minutes"]
        self.hour_diff = request["diff_duration_hour"]
        self.min_diff = request["diff_duration_mins"]
        self.time_format = request["time_format"]
        self.calculate_new_time()
        self.update_new_time()
        return self.formulate_result()

    def formulate_result(self):
        if self.day_diff_str:
            return f"{self.new_hour}:{self.new_mins:02d} {self.time_format} {self.day_diff_str}"
        return f"{self.new_hour}:{self.new_mins:02d} {self.time_format}"

    def calculate_new_time(self):
        self.new_hour = self.hour + self.hour_diff
        self.new_mins = self.mins + self.min_diff

    def update_new_time(self):
        print("in update new time method")

        self.new_number_days = math.ceil(self.new_hour / 24) if self.new_hour > 24 else 0
        number_of_changes = math.ceil(self.new_hour / 12)

        if self.new_mins > 60:
            self.new_mins %= 60
            self.new_hour += 1

        if self.new_hour == 12:
            self.time_format = self.possible_time_formats[self.time_format]
            self.day_diff_str = "(next day)" if self.time_format == "AM" else None
        if self.new_hour > 12:
            changed_time = self.new_hour % 12
            self.new_hour = 12 if changed_time == 0 else changed_time
            self.time_format = self.possible_time_formats[
                    self.time_format] if number_of_changes % 2 != 0 else self.time_format
            if self.time_format == "AM" and self.new_number_days == 1:
                self.day_diff_str = "(next day)"
            if (self.day_diff_str is None) and (self.new_number_days > 1):
                self.day_diff_str = f"({self.new_number_days} days later)"
