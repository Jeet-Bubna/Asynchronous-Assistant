from init import init
import logging

logger = logging.getLogger(__name__)

def main():
    
    init()
    logger.info('Main ended ---')
    

if __name__ == "__main__":
    main()