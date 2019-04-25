name = 'sms_alert'


def setup(self):
    self.notify = [item[1] for item in self.config.items() if item[0].startswith("notify")]


def check(self):
    pass


def alert(self, topic, condition):
    pass
