from handlers.handler import TimeHandler
import math


class TimeCalculator(TimeHandler):
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

    def __init__(self):
        self.next_handler = None
        self.inp_hour = None
        self.inp_mins = None
        self.inp_clock_format = None
        self.inp_add_hour = None
        self.inp_add_min = None
        self.out_hour = None
        self.out_min = None
        self.out_clock_format = None
        self.out_number_diff_of_days = 0
        self.number_of_clock_format_changes = 0
        self.out_diff_day_str = None
        self.in_day_of_week = None
        self.out_day_of_week = None

    def set_next(self, handler):
        self.next_handler = handler

    @staticmethod
    def conditional_round(inp, divisor):
        if inp == divisor:
            return 1
        result = inp / divisor
        if result > 1:
            if (result - int(result)) > 0.5:
                return math.ceil(result)
            return math.floor(result)

    def handle(self, **request):
        self.inp_hour = request["hour"]
        self.inp_mins = request["minutes"]
        self.inp_add_hour = request["diff_duration_hour"]
        self.inp_add_min = request["diff_duration_mins"]
        self.inp_clock_format = request["time_format"]
        self.in_day_of_week = request["day"]

        self.set_hour_component()
        self.set_minute_component()
        self.update_hour_and_minute_components()
        self.set_date_diff_component()
        self.set_clock_format_component()
        self.set_day_diff_str()
        self.set_day_of_week()

        if self.next_handler:
            return self.next_handler.handle()
        return self.formulate_result()

    def set_hour_component(self):
        self.out_hour = self.inp_hour + self.inp_add_hour

    def set_minute_component(self):
        self.out_min = self.inp_mins + self.inp_add_min

    def update_hour_and_minute_components(self):
        if self.out_min > 60:
            self.out_min %= 60
            self.out_hour += 1

        if self.out_hour >= 12:
            self.number_of_clock_format_changes = self.conditional_round(self.out_hour, 12)
            self.out_hour = 12 if self.out_hour == 12 or self.out_hour % 12 == 0 else self.out_hour % 12

    def set_date_diff_component(self):
        if self.number_of_clock_format_changes:
            if self.inp_clock_format == "PM" and self.number_of_clock_format_changes % 2 != 0:
                self.out_number_diff_of_days = math.ceil(self.number_of_clock_format_changes / 2)
            elif self.inp_clock_format == "AM" and self.number_of_clock_format_changes % 2 != 0:
                self.out_number_diff_of_days = math.floor(self.number_of_clock_format_changes / 2)
            else:
                self.out_number_diff_of_days = int(self.number_of_clock_format_changes / 2)

    def set_clock_format_component(self):
        self.out_clock_format = self.possible_time_formats[
            self.inp_clock_format] if self.number_of_clock_format_changes % 2 != 0 else self.inp_clock_format

    def set_day_diff_str(self):
        if self.out_number_diff_of_days:
            if self.out_number_diff_of_days == 1:
                self.out_diff_day_str = " (next day)"
            else:
                self.out_diff_day_str = f" ({self.out_number_diff_of_days} days later)"

    def set_day_of_week(self):
        if self.in_day_of_week:
            self.in_day_of_week = self.in_day_of_week.lower()
            curr_pos = self.days.index(self.in_day_of_week)
            new_pos = curr_pos + self.out_number_diff_of_days
            self.out_day_of_week = self.days[new_pos % 7]
            if self.out_diff_day_str:
                self.out_diff_day_str = f", {self.out_day_of_week.capitalize()}{self.out_diff_day_str}"
            else:
                self.out_diff_day_str = f", {self.out_day_of_week.capitalize()}"

    def formulate_result(self):
        if self.out_diff_day_str:
            return f"{self.out_hour}:{self.out_min:02d} {self.out_clock_format}{self.out_diff_day_str}"
        return f"{self.out_hour}:{self.out_min:02d} {self.out_clock_format}"
