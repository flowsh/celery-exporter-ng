import os
import logging
from test.celery_app import Celery
from utils import LimitedSizeDict
from prometheus_client import start_http_server, Summary

# define basic logger with european datetime format
log = logging.getLogger('Celery-Exporter-Ng')
log.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d.%m.%Y %H:%M:%S')

# get settings from environment variables
PORT = os.environ.get("PORT", 8000)
BROKER_URL = os.environ.get("BROKER_URL", False)
if not BROKER_URL:
    log.error(f"BROKER_URL not set!")
    exit(-1)
# max_tasks_captured helps to limit memory footprint
MAX_TASKS_CAPTURED = os.environ.get("MAX_TASKS_CAPTURED", 100000)

# define prometheus metrics
waiting_time = Summary('celery_queue_waiting_seconds', 'Waiting time of tasks in Celery queues', ['queue', 'task_name'])
queued_tasks = LimitedSizeDict(size_limit=MAX_TASKS_CAPTURED)


# this monitor captures celery events
def my_monitor(app):

    # event: task entered the queue
    def get_sent_time(event):
        # timestamp, queue and taskname are only send at the sent-event
        queued_tasks[event['uuid']] = {
            "ts": event['timestamp'],
            "queue": event['routing_key'],
            "taskname": event['name']
        }

    def get_started_time(event):
        task_id = event['uuid']
        # check if tasks sent-event was captured previously
        if task_id in queued_tasks:
            # calculate waiting time in queue
            lag = event['timestamp'] - queued_tasks[task_id]['ts']
            waiting_time.labels(queue=queued_tasks[task_id]['queue'],
                                task_name=queued_tasks[task_id]['taskname']).observe(lag)
            # remove entry from memory
            queued_tasks.pop(task_id, None)

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
                'task-sent': get_sent_time,
                'task-started': get_started_time,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)


if __name__ == '__main__':
    # http server will run in the background
    start_http_server(PORT)
    log.info(f"Celery Exporter NG listening on port {PORT}")

    # initialize celery app for monitor
    app = Celery(broker='redis://localhost:6379/')
    log.info(f"Celery Exporter NG connected to Celery broker, capturing events...")
    my_monitor(app)
