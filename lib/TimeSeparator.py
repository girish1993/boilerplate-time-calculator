from handlers.abstractHandler import AbstractTimeHandler


class TimeSeparator(AbstractTimeHandler):
    _components = {}

    def set_components(self, key, value):
        self._components[key] = value

    def get_components(self):
        return self._components

    @staticmethod
    def split_time(obj, sep):
        return obj.split(sep)

    def handle(self, **request):
        split_time = self.split_time(obj=request.start, sep=" ")
        split_hour_min = self.split_time(obj=split_time[0], sep=":")
        split_diff = self.split_time(obj=request.duration, sep=":")
        self.set_components(key="time_format", value=split_time[1])
        self.set_components(key="hour", value=int(split_hour_min[0]))
        self.set_components(key="minutes", value=int(split_hour_min[1]))
        self.set_components(key="diff_duration_hour", value=int(split_diff[0]))
        self.set_components(key="diff_duration_mins", value=int(split_diff[1]))

        self.get_components()
