from settings import ACCEPTABLE_RATIO, CATEGORIES, FUNCTIONS_LIST
import re
import numpy as np
import logging

logger = logging.getLogger(__name__)

def categorise_embeddings(embeddings, encode, text:str):
    try:
        text = text.replace("jarvis", "")
        text_embedding = encode(text)          
        # Calculate cosine similarity - encode alr uses l2 normalisation, so cosine similarity is just dot product
        similarities = np.dot(embeddings, text_embedding.T).flatten()
        best_idx = np.argmax(similarities)
        confidence = similarities[best_idx]
        category = [cat for cat in CATEGORIES.keys()][best_idx]

        if confidence < ACCEPTABLE_RATIO:
            logger.info("Confidence below acceptable ratio - no category detected")
            return "low confidence"
        else:
            return category

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
    """
    Categorise the text according to embeddings

    Approach: Regex is applied first to save timem on simple requests.
    Rest are delt with embeddings
    """
    cat = ""

    jarvis_pattern = r"^jarvis\b"
    match = re.match(jarvis_pattern, text)
    if not match:
        logger.info("Lead not found in command")
        return "lead error"
    
    pattern = r"^(jarvis)\s+(.*?)\s+(?:of|by|from|in|for)\s+(.*)$"
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

    