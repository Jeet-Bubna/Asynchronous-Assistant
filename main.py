from init import init
from input import input_function
import logging

logger = logging.getLogger(__name__)

def main():
    input_list = init()
    input_function(input_list)
    logger.info('Main ended ---')
    

if __name__ == "__main__":
    main()