import schedule


class Scheduler():
    def __init__(self,job: function, start_shift: str) -> None:
        self.job = job
        self.start_shift = start_shift
        self.finis_shif = finish_shift
    
    def start_schedule(self):
        schedule.every().day.at(self.start_shift).do(self.job)