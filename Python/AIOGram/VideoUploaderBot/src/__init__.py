import logging
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logs_path = os.path.join(project_root, 'logs')
videos_path = os.path.join(project_root, 'videos')
text_files = os.path.join(project_root, 'text_files')


if not os.path.exists(logs_path):
    os.makedirs(logs_path)

if not os.path.exists(videos_path):
    os.makedirs(videos_path)

if not os.path.exists(text_files):
    os.makedirs(text_files)

logging.basicConfig(
    filename=os.path.join(logs_path, 'app.log'),
    filemode='a',
    level=logging.DEBUG,
    encoding='utf-8',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)