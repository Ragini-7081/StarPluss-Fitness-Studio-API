
import logging


# Configure logging for the application.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

# Create a logger for API events.
logger = logging.getLogger("starpluss")
