import logging
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logs_path = os.path.join(project_root, 'logs')

if not os.path.exists(logs_path):
    os.makedirs(logs_path)

logging.basicConfig(
    filename=os.path.join(logs_path, 'app.log'),
    filemode='a',
    level=logging.DEBUG,
    encoding='utf-8',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)