from app.utils.logger import logger
from app.services.agent_service import AgentService

async def on_startup():
    logger.info("Initializing services...")
    # Initialize agent service to register callbacks
    agent_service = AgentService() 
    
    # Recover pending scheduled tasks
    await agent_service.scheduler.recover()
    
    logger.info("AI Memory System started successfully")
