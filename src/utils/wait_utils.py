import time

def wait_minutes(minutes):
    wait_seconds(minutes * 60)

def wait_seconds(seconds):
    time_out = seconds / 60
    print(f'Waiting for {time_out} minutes')
    time.sleep(seconds)