import logging
import time

logging.basicConfig(filename=f"logs/scraping_{time.time()}.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
