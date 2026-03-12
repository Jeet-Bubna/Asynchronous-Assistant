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

def init_threads() -> dict[str, WorkerThread]:
    logging.log(20, "Initialising Threads.....")
    worker_list : dict[str, WorkerThread] = {}
    functions = FUNCTIONS_LIST
    for function in functions["functions"]:
        path = function["func"]
        worker = WorkerThread(target=path)
        worker_list[function["name"]] = worker
    
    worker_list["input"] = WorkerThread(target=input_function)
    worker_list["input"].start()

    logger.log(20, "Input thread has been started....")

    worker_list["broadcaster"] = WorkerThread(target=broadcaster)
    worker_list["listener"] = WorkerThread(target=listener)

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

    workers_list = init_threads()
    embeddings = init_embeddings()
    queues = init_queues()

    return_dict = {
        "workers": workers_list,
        "embeddings":embeddings,
        "queues":queues
    }

    logger.log(20, "Initialisation --- complete ")

    return return_dict