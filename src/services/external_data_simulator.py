import asyncio
import random
import os
from typing import Dict, Any
from src.config.settings import settings

async def fetch_risky_external_data() -> Dict[str, Any]:
    failure_rate = settings.external_service_failure_rate
    if random.random() < failure_rate:
        raise RuntimeError("Simulated external service failure due to high load.")
    await asyncio.sleep(0.05)  
    return {"external_source": "ok", "value": random.randint(100, 200)}
import asyncio
import random
import os
from typing import Dict, Any
from src.config.settings import settings

async def fetch_risky_external_data() -> Dict[str, Any]:
    failure_rate = settings.external_service_failure_rate
    if random.random() < failure_rate:
        raise RuntimeError("Simulated external service failure due to high load.")
    await asyncio.sleep(0.05) 
    return {"external_source": "ok", "value": random.randint(100, 200)}
