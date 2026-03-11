import sys
import logging
import os

from classes import WorkerThread
from settings import FUNCTIONS_LIST, EMBEDDING_FILE
from typing import Callable

import numpy as np
from sentence_transformers import SentenceTransformer
from queue import PriorityQueue

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

def init_threads() -> dict[Callable, WorkerThread]:
    logging.log(20, "Initialising Threads.....")
    worker_list : dict[Callable, WorkerThread] = {}
    functions = FUNCTIONS_LIST
    for function in functions["functions"]:
        path = function["func"]
        worker = WorkerThread(target=path)
        worker_list[function["name"]] = worker
    
    logging.log(20, "Workers have been initialised")
    return worker_list

def init_embeddings() -> np.ndarray:
    categories = {'music': 'music player', 'timer':'timer', 'search':'search', 'end':'end the program'}   
    model = SentenceTransformer('all-MiniLM-L6-v2') 

    if os.path.exists(EMBEDDING_FILE):
        logger.log(20, "Found existing embeddings. Loading...")
        embeddings = np.load(EMBEDDING_FILE)
    else:
        logger.log(20, "No embeddings found. Generating now (this may take a moment)...")
        embeddings = model.encode([desired_category for _, desired_category in categories.items()], normalize_embeddings=True)
        np.save(EMBEDDING_FILE, embeddings)
    
    return embeddings

def init_queues() -> dict[Callable, PriorityQueue]:
    logger.log(20, "Initializing Queues.....")
    queues_list: dict[Callable, PriorityQueue] = {}
    for function in FUNCTIONS_LIST["functions"]:
        queues_list[function["func"]] = PriorityQueue()
    
    logger.log(20, "Initialised Queues")
    return queues_list

def init() : 
    
    return_dict = []

    init_logger()
    logger.log(20, "Logger has been initialised")

    workers_list = init_threads()
    embeddings = init_embeddings()
    queues = init_queues()

    return_dict = [
        {"workers": workers_list},
        {"embeddings":embeddings},
        {"queues":queues}
    ]

    return return_dict

print(init())