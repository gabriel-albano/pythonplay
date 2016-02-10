#!/usr/bin/python

#
# com.albanos.logger
#
import logging
import logging.handlers
from os.path import expanduser
home = expanduser("~")

def getLogger(name):
#        logging.basicConfig(level=logging.DEBUG,
#            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#            datefmt='%m/%d/%Y %I:%M:%S %p')

    # create logger
    logger = logging.getLogger(name)

    # create console handler
    ch1 = logging.StreamHandler()

    # create a file handler
    LOG_FILENAME = 'test.log'
    #ch2 = logging.FileHandler(home + '/test.log')
    # Add the log message handler to the logger
    ch2 = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=20, backupCount=5)

    # Set log Lever
    #ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)-8s - %(message)s','%m/%d/%Y %I:%M:%S %p')
    #formatter = logging.Formatter('%(message)s')


    # add formatter to ch
    ch1.setFormatter(formatter)
    ch2.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch1)
    logger.addHandler(ch2)

    return logger

logger  = getLogger('logger')

def setup():
    logger.setLevel(logging.DEBUG)

def test():
    logger.info("This is the logger test!")

    for i in range(20):
        logger.debug({'i': i})

def main():
    setup()
    test()

if __name__ == '__main__':
    main()
