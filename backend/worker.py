import asyncio 
from app.core.queue import process_queue 
 
if __name__ == "__main__": 
    asyncio.run(process_queue()) 
