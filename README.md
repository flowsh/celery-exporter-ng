# Celery Exporter NG

[![Deploy to Docker Hub](https://github.com/flowsh/celery-exporter-ng/actions/workflows/main.yml/badge.svg?event=workflow_dispatch)](https://github.com/flowsh/celery-exporter-ng/actions/workflows/main.yml)

Minimal new generation Prometheus exporter for Celery 5, provides waiting time in queues.
Therefore tasks are captured at the _task-sent_ event, when entering the celery queues.
On _task-started_ event, the delay between entering and leaving the queue is calculated and provided as *celery_queue_waiting*.
If the maximum number of captured tasks is reached, no new entries can be added to the dictionary.

## Supported Stack

Tested with Celery 5, Broker protocols amqp and redis.

## Get Container

Get the container from [Docker Hub](https://hub.docker.com/r/flowsh/celery-exporter-ng).

```bash
docker pull flowsh/celery-exporter-ng
```

## Configuration

Environment variable | Value | Description
------------ | ------------- | -------------
BROKER_URL | redis://user:pass@host:port/db | URL of the Celery Broker
PORT | 8000 (default) | Listening port of this exporter
MAX_TASKS_CAPTURED | 100000 (default) | Max number of tasks considered, helps to limit memory usage
BROKER_RECEIVE_TIMEOUT | 5.0 (default) | Timeout for event capturing in seconds

## Metrics

The metrics can be obtained at _http://container:8000/metrics_.
The queue waiting time is labeled with the name of the queue and the task itself.

```
# HELP celery_queue_waiting_seconds Waiting time of tasks in Celery queues
# TYPE celery_queue_waiting_seconds summary
celery_queue_waiting_seconds_count{queue="celery",task_name="tasks.do_something"} 8.0
celery_queue_waiting_seconds_sum{queue="celery",task_name="tasks.do_something"} 19.50933337211609
# HELP celery_queue_waiting_seconds_created Waiting time of tasks in Celery queues
# TYPE celery_queue_waiting_seconds_created gauge
celery_queue_waiting_seconds_created{queue="celery",task_name="tasks.do_something"} 1.6353504535314684e+09
# HELP celery_tasks_queue_length Length of Celery queues with tasks
# TYPE celery_tasks_queue_length gauge
celery_tasks_queue_length{queue="celery",task_name="tasks.do_something"} 10.0
# HELP celery_tasks_running Number of Celery Tasks currently running
# TYPE celery_tasks_running gauge
celery_tasks_running{queue="celery",task_name="tasks.do_something",worker="celery@DESKTOP-AFLD8PP"} 1.0
# HELP celery_exporter_tasks_captured Number of tasks captured by Celery exporter
# TYPE celery_exporter_tasks_captured gauge
celery_exporter_tasks_captured 11.0
```
