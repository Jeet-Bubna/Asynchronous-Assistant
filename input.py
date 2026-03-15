import logging
from classes import WorkerThread, Packets

from queue import PriorityQueue
import re
import numpy as np
from sentence_transformers import SentenceTransformer, util

from settings import FUNCTIONS_LIST, ACCEPTABLE_RATIO, CATEGORIES

logger = logging.getLogger(__name__)

def categorise_embeddings(embeddings, model:SentenceTransformer, text:str):
    jarvis_pattern = r"^jarvis\b"
    match = re.match(jarvis_pattern, text)
    if not match:
        logger.log(10, "Lead not found in command")
        return ""
    try:
        text = text.replace("jarvis", "")
        text_embedding = model.encode(text, normalize_embeddings=True)          # Finds the vector values for the text that we have inputed
        scores = util.cos_sim(text_embedding, embeddings)[0]           # Calculates the score
        if scores.max().item() < ACCEPTABLE_RATIO:                          
            logger.log(10, "No suitable match... scores below acceptable ratio")
            return ''
        else:
            best_idx = int(scores.argmax().item())      
            cat = [category for category, _ in CATEGORIES.items()][best_idx]
            logger.log(20, f"Cateogory found: {cat}")
            return cat
    except KeyError:
        logger.critical('Detect Category failed - key error', exc_info=True)
    
    logger.log(20, "No category detected")
    return ""


def categoriser(text:str, embeddings, model:SentenceTransformer):
    """
    Categorise the text according to embeddings

    Approach: Regex is applied first to save timem on simple requests.
    Rest are delt with embeddings
    """
    cat = ""

    pattern = r"^(jarvis)\s+(.*?)\s+(?:of|by|from|in|for)\s+(.*)$"
    match = re.match(pattern, text, re.IGNORECASE)
    if (match):
        logger.log(20, "REGEX Pattern Matched....") 
        program, module, params = match.groups()
        for func in FUNCTIONS_LIST["functions"]:
            if func["name"] in module:
                cat = func["name"]
                logger.log(20, f"Cateogory found: {cat}")
                print("Category found", cat)
        
        return cat

    else:
        return categorise_embeddings(embeddings, model, text)       

    

def calculatePriority(isEnd:bool):
    # For now, return 1
    if(isEnd):
        return 1
    else:
        return 3

def input_function(input_list):
    
    isRunning = True 

    workers_list = input_list["workers"]
    embeddings = input_list["embeddings"]["embeddings"]
    model = input_list["embeddings"]["model"]

    logger.debug(f"TYPE: {type(embeddings)}")
    logger.debug(f"CONTENT: {embeddings}")

    queues = input_list["queues"]

    main_queue = queues["main queue"]

    while isRunning:
        user_input = input("YOU: ")
        category = categoriser(user_input, embeddings, model)
        if(category == "end"):
            isRunning = False
            priority = calculatePriority(True)
            packet = Packets("end", main_queue, workers_list["listener"]) # if end, send end in message and default queue and workers objects
            main_queue['commandq'].put((priority, packet))
            logger.log(20, f"END COMMAND HAS BEEN PUT IN MAIN QUEUE")
            return 1

        if(category != ""):
            priority = calculatePriority(False)
            queue = queues[category]
            worker = workers_list[category]
            packet = Packets(user_input, queue, worker) 
            main_queue['commandq'].put((priority, packet))
            logger.log(20, f"A PACKET {packet} with PRIORITY {priority} has been send to main queue")
 