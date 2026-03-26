from queue import PriorityQueue
from classes import Packets, WorkerThread
import logging


logger = logging.getLogger(__name__)

def broadcaster(queues, event = None, run_once=False):
    isRunning = True
    isEnding = False
    main_queue:PriorityQueue = queues["main queue"]
    logger.debug("Broadcaster has recieved the args")
    logger.debug(f"Type of Main_Queue is: {type(main_queue)}")
    logger.debug(f"object of Main_Queue is: {main_queue}")

    while isRunning:
        if run_once:
            isRunning = False

        priority , packet = main_queue.get()
        main_queue.task_done()

        logger.info(f"Recieved message: {packet._content}")

        if (packet._content == "end"):
            isRunning = False
            isEnding = True

            logger.debug(f"QUEUES OBJECT: {queues}")
            del queues['main queue']
            del queues['listener queue']
            for queue in queues.values():
                queue.put((1, Packets(content="end", queue=main_queue)))

            logger.info(f"ALL QUEUES HAVE BEEN SENT THE END SIGNAL")
        else:
            queue = packet._queue["queue"] # Key Error no?
            queue.put((priority, packet))

        if packet._event != None:
            packet._event.set()

    while isEnding:
        if run_once:
            isEnding = False
        priortiy, packet = main_queue.get()
        main_queue.task_done()

        try:
            error = packet._content["error"]
            if error:
                logger.critical(f"BROADCASTER RECIEVED THE ERROR:{error}")
                return "ended"
            
            success = packet._content["success"]
            if success:
                logger.info("Broadcaster ensures all threads are closed")
                return "success"
        except (KeyError, TypeError) as e:
            logger.critical(f"{e} occured at broadcaster")
      