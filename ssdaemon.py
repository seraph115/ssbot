import daemon
import time
import sscheck


def do_ss_service_check(freezen_time):
  while True:
    sscheck.ss_service_check(sscheck.sslocal_jp_start, sscheck.check_jp, ":jp: Tokyo")
    sscheck.ss_service_check(sscheck.sslocal_uk_start, sscheck.check_uk, ":uk: London")
    time.sleep(freezen_time)

def run():
  with daemon.DaemonContext():
    interval_time = 300
    do_ss_service_check(interval_time)

if __name__ == "__main__":
    run()
