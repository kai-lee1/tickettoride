import requests
import json
import time
import logging

def repeat(interval, func, *args, **kwargs):
    while True:
        if not func(*args, **kwargs):
            break
        time.sleep(interval)

def get_data(main):
    try:
        if main.quit:
            return False
        t = time.time()
        r = requests.get(main.ip_port + "/previous_move/")
        logging.info(f"Time taken to get data: {time.time() - t}")
        main.test_server()
        return True
    except:
        return True
    
