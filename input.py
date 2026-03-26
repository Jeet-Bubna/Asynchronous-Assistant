import logging
from classes import Packets
from categorizer import categoriser

logger = logging.getLogger(__name__)

def calculatePriority(isEnd:bool):
    # For now, return 1
    if(isEnd):
        return 1
    else:
        return 3

def input_function(input_list, run_once=False):
    
    isRunning = True 

    workers_list = input_list["workers"]
    embeddings = input_list["embeddings"]["embeddings"]
    encode = input_list["embeddings"]["encode"]

    queues = input_list["queues"]
    main_queue = queues["main queue"]
    listening_queue = queues["listener queue"]

    while isRunning:
        user_input = input("YOU: ")
        categoriser_object = categoriser(user_input, embeddings, encode)
        category = categoriser_object['category']
        command = categoriser_object['command']
        if(category == "end"):
            isRunning = False
            priority = calculatePriority(True)
            packet = Packets("end", {"queue": main_queue, "listening_queue":listening_queue}) # if end, send end in message and default queue and workers objects
            main_queue.put((priority, packet))
            logger.info(f"END COMMAND HAS BEEN PUT IN MAIN QUEUE")
            return "ending"

        try:
            if(category != "low confidence" and category != "lead error"):
                if run_once:
                    isRunning = False
                priority = calculatePriority(False)
                queue = queues[category]
                worker = workers_list[category]["thread"]
                event = workers_list[category]["event"]
                packet_contnet = {"raw text": user_input, "command":command}
                packet = Packets(packet_contnet, {"queue": queue, "listening_queue":queues["listener queue"]}, worker, event) 
                main_queue.put((priority, packet))
                logger.info(f"A PACKET {packet} with PRIORITY {priority} has been send to main queue")
        except KeyError:
            logger.critical(f"Key error occured in input function", exc_info=True)
 