import datetime
import json
import logging
import threading
import timeit
from time import sleep
from typing import List

import schedule

from src.config import OCD_DTL_QUERY_CONFIG_PATH
from src.datalake import Datalake
from src.logger import configure_logging, logger
from src.misp import Misp
from src.signal_manager import SignalManager
from src.types import DtlMispEvent


configure_logging(logging.DEBUG)

datalake = Datalake()
misp = Misp()
signal_manager = SignalManager()

jobs_running = set()


def job(query_hash):
    logger.debug('Starting to process %s' % query_hash)

    try:
        start_time = timeit.default_timer()
        events_pushed = push_data_from_query_hash(query_hash)
        logger.info(
            'Done with the process of %s : %s events, after %1.2fs',
            query_hash,
            len(events_pushed),
            timeit.default_timer() - start_time,
        )
    except:
        logger.exception(f'Threats for query hash {query_hash} failed to be retrieved and injected into misp')
        raise
    finally:
        jobs_running.remove(query_hash)


def push_data_from_query_hash(query_hash) -> List[DtlMispEvent]:
    events = datalake.retrieve_events_from_query_hash(query_hash)
    misp.add_events(events)
    return events


def run_threaded(job_func, query_hash):
    if query_hash not in jobs_running:  # Skip already running jobs
        jobs_running.add(query_hash)
        job_thread = threading.Thread(target=job_func, args=(query_hash,))
        job_thread.start()


def register_jobs(jobs_config_path):
    with open(jobs_config_path) as json_file:
        config = json.load(json_file)

    query_hashes = set()
    for query in config['queries']:
        frequency = query['frequency']
        query_hash = query['query_hash']

        if query_hash in query_hashes:
            raise ValueError(f"Query hash {query_hash} is duplicated, a same query can't be set multiple time")
        query_hashes.add(query_hash)

        frequency_number = int(frequency[:-1])
        if frequency[-1] == 's':
            schedule.every(frequency_number).seconds.do(run_threaded, job, query_hash)
        elif frequency[-1] == 'm':
            schedule.every(frequency_number).minutes.do(run_threaded, job, query_hash)
        elif frequency[-1] == 'h':
            schedule.every(frequency_number).hours.do(run_threaded, job, query_hash)
        else:
            raise ValueError(f'Config expect a frequency: <x>[s|m|h], got {frequency}')

    if len(query_hashes) == 0:
        raise ValueError(f'No query found')
    next_run: datetime.timedelta = schedule.next_run() - datetime.datetime.now()
    logger.info('Loaded %s queries with success, next run in %1.0f s', len(query_hashes), next_run.total_seconds())


register_jobs(OCD_DTL_QUERY_CONFIG_PATH)

while not signal_manager.is_stop_requested:
    schedule.run_pending()
    sleep(1)

misp.close()
