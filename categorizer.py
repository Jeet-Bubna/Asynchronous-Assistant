from settings import ACCEPTABLE_RATIO, CATEGORIES, FUNCTIONS_LIST, ASSISTANT_NAME
import re
import numpy as np
import logging

logger = logging.getLogger(__name__)

def calculate_main_embeddings(embeddings, text_embedding):
    similarities = np.dot(embeddings, text_embedding.T).flatten()
    best_idx = np.argmax(similarities)
    confidence = similarities[best_idx]
    category = [cat for cat in CATEGORIES.keys()][best_idx]

    if confidence < ACCEPTABLE_RATIO:
        logger.info("Confidence below acceptable ratio - no category detected")
        return "low confidence"
    else:
        return category

def categorise_embeddings(embeddings, encode, text:str):
    try:
        text = text.replace("jarvis", "")
        text_embedding = encode(text)          
        
        main_category = calculate_main_embeddings(embeddings, text_embedding)

    except KeyError:
        logger.critical('Detect Category failed - key error', exc_info=True)
        return "key error"
    
    except ValueError:
        logger.critical("Detect Category failed - value error - are you using different models?", exc_info=True)
        return "value error"
    
    except IndexError:
        logger.critical("Detect Category failed - index error - the embeddings and FUNCTIONS are out of sync.", exc_info=True)
        return "index error"

def categoriser(text:str, embeddings, model):
    cat = ""

    jarvis_pattern = rf"^{ASSISTANT_NAME.lower()}\b"
    match = re.match(jarvis_pattern, text)
    if not match:
        logger.info("Lead not found in command")
        return "lead error"
    
    pattern = rf"^({ASSISTANT_NAME.lower()})\s+(.*?)\s+(?:of|by|from|in|for)\s+(.*)$"
    match = re.match(pattern, text, re.IGNORECASE)
    if (match):
        logger.log(20, "REGEX Pattern Matched....") 
        program, module, params = match.groups()
        for func in FUNCTIONS_LIST["functions"]:
            if func["name"] in module:
                cat = func["name"]
                logger.log(20, f"Cateogory found: {cat}")
                logger.info("Category found", cat)
        
        return cat

    else:
        return categorise_embeddings(embeddings, model, text)       

    