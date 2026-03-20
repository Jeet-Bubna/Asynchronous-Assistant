import sys
import logging
import os

from classes import WorkerThread
from settings import FUNCTIONS_LIST, EMBEDDING_FILE, CATEGORIES, MODEL_PATH, MODEL_NAME
from typing import Callable

import numpy as np
from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer, pipeline

from queue import PriorityQueue
from input import input_function
from broadcaster import broadcaster
from listener import listener

# 1. Force Offline Mode globally before loading the model
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'

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

def init_threads(queues) -> dict[str, WorkerThread]:
    logging.log(20, "Initialising Threads.....")
    worker_list : dict[str, WorkerThread] = {}
    functions = FUNCTIONS_LIST
    for function in functions["functions"]:
        path = function["func"]
        worker = WorkerThread(target=path)
        worker_list[function["name"]] = worker
    
    worker_list["broadcaster"] = WorkerThread(target=broadcaster, args=(queues,))
    worker_list["broadcaster"].start()

    logger.log(20, "Broadcaster thread has been started....")

    worker_list["listener"] = WorkerThread(target=listener, kwargs={"listening_queue":queues['listener queue'], "main_queue":queues["main queue"], "threads":worker_list})
    worker_list["listener"].start()
    
    logger.log(20, "Listener thread has been started....")

    logging.log(20, "Workers have been initialised")
    return worker_list

def init_embeddings():
    
    if os.path.exists(MODEL_PATH):
        logger.info("Loading {MODEL_NAME} locally")
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
        os.environ['HF_HUB_OFFLINE'] = '1'
        model = ORTModelForFeatureExtraction.from_pretrained(MODEL_PATH, local_files_only=True)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)

    else:
        logger.info(f"Saving {MODEL_NAME} for the first time in memory!")
        model = ORTModelForFeatureExtraction.from_pretrained(MODEL_NAME, export=True)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model.save_pretrained(MODEL_PATH)
        print(f"Model saved to {MODEL_PATH}")

    def encode(sentence):
        """
        Takes a sentence, and uses the extractor to return 
        a normalised embedding vector
        """

        # Tokenize the text, and allow padding and truncation, to get equal spaced arrays
        inputs = tokenizer(
            sentence,
            padding=True,
            truncation=True,
            return_tensors="np"
        )

        # run onxx model 
        outputs = model(**inputs)

        # Mean pooling: Dont use CLS token [the first token in the array which is 
        # noramlly used to classify sentences] because this model is trained to 
        # excel at mean pooling, and also outputs[0] is the last hidden state
        embeddings = np.mean(outputs[0], axis=1)

        #Normalisation - to basically make calucaltion easier and mitigate the effect
        # of the frequency of words in long sentences, by basicaly making the relative
        # vector have a square length of 1 to calucalte cosine similarity
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        return embeddings / norms        

    if os.path.exists(EMBEDDING_FILE):
        logger.log(20, "Found existing embeddings. Loading...")
        embeddings = np.load(EMBEDDING_FILE, allow_pickle=True)
        logger.debug(f"TYPE: {type(embeddings)}")
        logger.debug(f"CONTENT: {embeddings}")
    else:
        logger.log(20, "No embeddings found. Generating now (this may take a moment)...")
        extractor = pipeline("feature-extraction", model=model, tokenizer=tokenizer) # type: ignore
        categories = [description for description in CATEGORIES.values()]
        embeddings = encode(sentence=categories)
        np.save(EMBEDDING_FILE, embeddings)
    
    logger.log(10, f"THE EMBEDDINGS OBJECT IS:")    
    return {"embeddings": embeddings, "encode": encode}

"""
{
"music":{"commandq":Queue, "responseq":Queue}
}
"""

def init_queues():
    logger.log(20, "Initializing Queues.....")
    queues_list = {}
    for function in FUNCTIONS_LIST["functions"]:
        queues_list[function["name"]] = PriorityQueue()
    
    queues_list["main queue"] = PriorityQueue()
    queues_list["listener queue"] = PriorityQueue() 
    
    logger.log(20, "Initialised Queues")
    logger.log(10, f"THE QUEUE OBJECT IS: {queues_list}")
    return queues_list

def init() : 
    
    return_dict = []

    init_logger()
    logger.log(20, "Logger has been initialised")

    embeddings = init_embeddings()
    queues = init_queues()
    workers_list = init_threads(queues)

    return_dict = {
        "workers": workers_list,
        "embeddings":embeddings,
        "queues":queues
    }

    logger.log(20, "Initialisation --- complete ")

    return return_dict