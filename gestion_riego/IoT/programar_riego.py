from datetime import datetime
from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler

class DefinirRiego:

    def job(self,text):
        print(text)

    def start(self):
        scheduler = BlockingScheduler()
        # In 2019-8-30 Run once job Method
        scheduler.add_job(self.job, 'interval', seconds=5, args=['Digo Hola'])
        scheduler.start()

definir_riego = DefinirRiego()
definir_riego.start()