import logging

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='my_api.log', level=logging.INFO, format=FORMAT)

app_logger = logging.getLogger()