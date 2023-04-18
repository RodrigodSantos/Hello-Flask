<<<<<<< HEAD
import logging

logging.basicConfig(
  level=logging.DEBUG, 
  format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
  handlers=[
    logging.FileHandler("info.log", mode='w'),logging.StreamHandler()
  ]
=======
import logging

logging.basicConfig(
  level=logging.DEBUG, 
  format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
  handlers=[
    logging.FileHandler("info.log", mode='w'),logging.StreamHandler()
  ]
>>>>>>> 6e644c2a40dff79b5007cf8f7be61627c6df9ade
)