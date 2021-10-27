import logging

# define basic logger with european datetime format
log = logging.getLogger('Celery-Exporter-Ng')
log.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s - Celery-Exporter-NG: %(message)s', datefmt='%d.%m.%Y %H:%M:%S')