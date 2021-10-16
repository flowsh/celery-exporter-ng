# Celery Exporter NG

[![Deploy to Docker Hub](https://github.com/flowsh/celery-exporter-ng/actions/workflows/main.yml/badge.svg?event=push)](https://github.com/flowsh/celery-exporter-ng/actions/workflows/main.yml)

Minimal new generation Prometheus exporter for Celery 5, provides waiting time in queues.
Therefore tasks are captured at the _task-sent_ event, when entering the celery queues.
On _task-started_ event, the delay between entering and leaving the queue is calculated and provided as *celery_queue_waiting*.
If the maximum number of captured tasks is reached, oldest entries in the internal memory will be dropped first.

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

## Metrics

The metrics can be obtained at _http://container:8000/metrics_.
The queue waiting time is labeled with the name of the queue and the task itself.

```
# HELP celery_queue_waiting_seconds Waiting time of tasks in Celery queues
# TYPE celery_queue_waiting_seconds summary
celery_queue_waiting_seconds_count{queue="celery",task_name="tasks.do_something"} 152.0
celery_queue_waiting_seconds_sum{queue="celery",task_name="tasks.do_something"} 589.1490948200226
# HELP celery_queue_waiting_seconds_created Waiting time of tasks in Celery queues
# TYPE celery_queue_waiting_seconds_created gauge
celery_queue_waiting_seconds_created{queue="celery",task_name="tasks.do_something"} 1.6343385165777767e+09
```
