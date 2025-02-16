import schedule
import time

from main import check_do_trx

def p():
    print("Running transactions")

# schedule.every(3).seconds.do(check_do_trx)
schedule.every(3).seconds.do(p)

while True:
    schedule.run_pending()
    time.sleep(1)

