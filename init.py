import sys
import logging
import os

from classes import WorkerThread
from settings import FUNCTIONS_LIST, EMBEDDING_FILE, CATEGORIES
from typing import Callable

import numpy as np
from sentence_transformers import SentenceTransformer

from queue import PriorityQueue
from input import input_function
from broadcaster import broadcaster
from listener import listener

logger = logging.getLogger(__name__)

def init_logger():
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger() 
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(os.path.join("logs", "logfile.log"), mode="a")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

def init_threads(mainq, listeningqs) -> dict[str, WorkerThread]:
    logging.log(20, "Initialising Threads.....")
    worker_list : dict[str, WorkerThread] = {}
    functions = FUNCTIONS_LIST
    for function in functions["functions"]:
        path = function["func"]
        worker = WorkerThread(target=path)
        worker_list[function["name"]] = worker
    
    worker_list["broadcaster"] = WorkerThread(target=broadcaster, args=(mainq["commandq"], ))
    worker_list["broadcaster"].start()

    logger.log(20, "Broadcaster thread has been started....")

    worker_list["listener"] = WorkerThread(target=listener, args=(listeningqs, ))
    worker_list["listener"].start()
    
    logger.log(20, "Listener thread has been started....")

    logging.log(20, "Workers have been initialised")
    return worker_list

def init_embeddings():
     
    model = SentenceTransformer('all-MiniLM-L6-v2') 
    if os.path.exists(EMBEDDING_FILE):
        logger.log(20, "Found existing embeddings. Loading...")
        embeddings = np.load(EMBEDDING_FILE, allow_pickle=True)
        logger.debug(f"TYPE: {type(embeddings)}")
        logger.debug(f"CONTENT: {embeddings}")
    else:
        logger.log(20, "No embeddings found. Generating now (this may take a moment)...")
        embeddings = model.encode([desired_category for _, desired_category in CATEGORIES.items()], normalize_embeddings=True)
        np.save(EMBEDDING_FILE, embeddings)
    
    logger.log(10, f"THE EMBEDDINGS OBJECT IS:")    
    return {"embeddings": embeddings, "model": model}

"""
{
"music":{"commandq":Queue, "responseq":Queue}
}
"""

def init_queues():
    logger.log(20, "Initializing Queues.....")
    queues_list = {}
    for function in FUNCTIONS_LIST["functions"]:
        queues_list[function["name"]] = {"commandq":PriorityQueue(), "responseq": PriorityQueue()}
    
    queues_list["main queue"] = {"commandq":PriorityQueue(), "responseq":None}
    queues_list["status queue"] = {"commandq":PriorityQueue(), "responseq":None}
    
    logger.log(20, "Initialised Queues")
    logger.log(10, f"THE QUEUE OBJECT IS: {queues_list}")
    return queues_list

def init() : 
    
    return_dict = []

    init_logger()
    logger.log(20, "Logger has been initialised")

    embeddings = init_embeddings()
    queues = init_queues()

    listening_qs = {}
    for obj in queues:
       list_queue = queues[obj]["responseq"]
       listening_qs[obj] = list_queue

    workers_list = init_threads(queues["main queue"], listening_qs)

    return_dict = {
        "workers": workers_list,
        "embeddings":embeddings,
        "queues":queues
    }

    logger.log(20, "Initialisation --- complete ")

    return return_dict