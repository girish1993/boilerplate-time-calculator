from handlers.handler import TimeHandler


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

    new_hour = None
    new_mins = None
    new_format = None
    new_number_days = None

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
        # self.day = request["day"]
        self.calculate_new_time()
        # if self.next_handler:
        #     self.next_handler.handle(self.update_new_time())
        return self.update_new_time()

    def calculate_new_time(self):
        self.new_hour = self.hour + self.hour_diff
        self.new_mins = self.mins + self.min_diff

    def update_new_time(self):
        print("in update new time method")

        self.new_number_days = round(self.new_hour / 24)

        if self.new_mins > 60:
            self.new_mins %= 60
            self.new_hour += 1

        if self.new_hour > 12:
            self.new_hour %= 12
            self.time_format = self.possible_time_formats[self.time_format]

        return f"{self.new_hour}:{self.new_mins} {self.time_format}"
