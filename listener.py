from settings import FUNCTIONS_LIST
from classes import Packets
import logging 
import random
import traceback

logger = logging.getLogger(__name__)

def listener(listening_queue, main_queue, threads):
    isRunning = True
    RUNNING_STATUS = {}
    for function in FUNCTIONS_LIST["functions"]:
        name = function["name"]
        RUNNING_STATUS[name] = False

    while isRunning:
        priority, packet = listening_queue.get()

        if packet._content["started"] == True:
            function = packet._content["function"]

            if RUNNING_STATUS[function] == False:
                RUNNING_STATUS[function] = True
                logger.info(f"{function} has been marked as STARTED")
            
            else:
                packet._content['error'] = "S2" # Started twice
                main_queue.put((1, packet))
                logger.critical(f"{function} has been started twice!!!")
        
        elif packet._content["started"] == False:
            function = packet._content["function"]

            if RUNNING_STATUS[function] == True:
                RUNNING_STATUS[function] = False
                logger.info(f"{function} has been marked as STOPPED")
            
            else: 
                packet._content["error"] = "E2" # Ended twice
                main_queue.put(1, packet)
                logger.critical((f"{function} has been ended twice!!!"))

        try:
            if packet._content["end"] == True:
                isRunning = False
                # Removing broadcaster from the thread (listener thread wont be there)
                del threads['broadcaster']
                for program, thread in threads.items():
                    #try:
                        if thread.is_alive():
                            thread.join()
                            logger.info(f"{program} has JOINED in Listener")
                        else:
                            logger.info(f"{program} was never started")
                    # No need to put in main queue for success
                    #except Exception as e:
                    #    logger.critical(f"{program} was not able to join, ERROR: {e}")
                    #    print(traceback.print_exc())
                    #    # Priority = 1 + (random number b/w 0 and 1)
                    #    # Really hacky, dont wanna refactor rn
                    #    main_queue.put(
                    #        (1 + random.random(), Packets(
                    #            content={
                    #                "function":program,
                    #                "error":e }, 
                    #            queue=main_queue, 
                    #            worker=thread)))

                #Sending last packet confirming everyting has ended   
                main_queue.put(
                    (1 + random.random(), Packets(
                        content={
                            "function":None,
                            "error": None,
                            "ended": True
                        },
                        queue=main_queue, 
                        worker=thread)))
        except KeyError:
            pass