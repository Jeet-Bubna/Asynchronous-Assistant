from queue import PriorityQueue
from classes import Packets, WorkerThread
import logging


logger = logging.getLogger(__name__)

def broadcaster(queues):
    isRunning = True
    isEnding = False
    main_queue = queues["main queue"]
    logger.debug("Broadcaster has recieved the args")
    logger.debug(f"Type of Main_Queue is: {type(main_queue)}")
    logger.debug(f"object of Main_Queue is: {main_queue}")
    while isRunning:
        priority , packet = main_queue.get()
        logger.info(f"Recieved message: {packet._content}")
        queue:PriorityQueue = packet._queue["queue"]
        queue.put((priority, packet))

        worker: WorkerThread = packet._worker
        logger.debug(f"THE STATUS OF THE WORKER IS: {worker.is_alive()}")
        logger.info(f"{worker} has been passed [{packet._content}], with queue [{packet._queue}] in queue [{queue}]") 

        if (packet._content == "end"):
            isRunning = False
            isEnding = True

            logger.debug(f"QUEUES OBJECT: {queues}")
            del queues['main queue']
            del queues['listener queue']
            for queue in queues.values():
                queue.put((1, Packets(content="end", queue=main_queue, worker=worker)))

            logger.info(f"ALL QUEUES HAVE BEEN SENT THE END SIGNAL")

        if worker.is_alive() == False: 
            worker.update_args((packet._content, packet._queue))
            worker.start()

    while isEnding:
        priortiy, packet = main_queue.get()
        try:
            error = packet._content["error"]
            if error:
                logger.critical(f"BROADCASTER RECIEVED THE ERROR:{error}")
                worker = packet._content["worker"]
                #Gotta do something for now, just print comment
                print("Ohnoooo errorrrrrr idk how to handle rn")
        except (KeyError, TypeError):
            pass
      