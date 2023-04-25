import logging

logging.basicConfig(
  level=logging.DEBUG, 
  format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
  handlers=[
    logging.FileHandler("info.log", mode='w'),logging.StreamHandler()
  ]
)