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
BACKEND_URL | redis://user:pass@host:port/db (optional) | URL of the Celery Result Backend
PORT | 8000 (default) | Listening port of this exporter
MAX_TASKS_CAPTURED | 100000 (default) | Max number of tasks considered, helps to limit memory usage

## Metrics

The metrics can be obtained at _http://container:8000/metrics_.
The queue waiting time is labeled with the name of the queue and the task itself.

```
# HELP celery_queue_waiting_seconds Waiting time of tasks in Celery queues
# TYPE celery_queue_waiting_seconds summary
celery_queue_waiting_seconds_count{queue="celery",task_name="tasks.do_something"} 12.0
celery_queue_waiting_seconds_sum{queue="celery",task_name="tasks.do_something"} 6.919644355773926
# HELP celery_queue_waiting_seconds_created Waiting time of tasks in Celery queues
# TYPE celery_queue_waiting_seconds_created gauge
celery_queue_waiting_seconds_created{queue="celery",task_name="tasks.do_something"} 1.635367870602351e+09
# HELP celery_tasks_queue_length Length of Celery queues with tasks
# TYPE celery_tasks_queue_length gauge
celery_tasks_queue_length{queue="celery",task_name="tasks.do_something"} 1.0
# HELP celery_tasks_running Number of Celery Tasks currently running
# TYPE celery_tasks_running gauge
celery_tasks_running{queue="celery",task_name="tasks.do_something",worker="celery@DESKTOP-AFLD8PP"} 1.0
# HELP celery_exporter_tasks_tracked Number of tasks tracked by Celery exporter, limit is MAX_TASKS_CAPTURED
# TYPE celery_exporter_tasks_tracked gauge
celery_exporter_tasks_tracked 2.0
# HELP celery_tasks_duration_seconds Duration of tasks when finished in given state
# TYPE celery_tasks_duration_seconds summary
celery_tasks_duration_seconds_count{queue="celery",state="succeeded",task_name="tasks.do_something",worker="celery@DESKTOP-AFLD8PP"} 11.0
celery_tasks_duration_seconds_sum{queue="celery",state="succeeded",task_name="tasks.do_something",worker="celery@DESKTOP-AFLD8PP"} 4.866418838500977
# HELP celery_tasks_duration_seconds_created Duration of tasks when finished in given state
# TYPE celery_tasks_duration_seconds_created gauge
celery_tasks_duration_seconds_created{queue="celery",state="succeeded",task_name="tasks.do_something",worker="celery@DESKTOP-AFLD8PP"} 1.6353678708143656e+09
```
