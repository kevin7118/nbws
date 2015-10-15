import logging

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s|%(filename)s:%(lineno)s|%(levelname)s|%(message)s')

fh = logging.FileHandler('nbws.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)