import concurrent
import timeit
from typing import Iterable
import concurrent.futures

from pymisp import ExpandedPyMISP, MISPEvent

from src.config import OCD_DTL_MISP_HOST, OCD_DTL_MISP_API_KEY, OCD_DTL_MISP_USE_SSL, OCD_DTL_MISP_WORKER
from src.logger import logger
from src.types import DtlMispEvent
from src.wrappers import ignore


class Misp:

    def __init__(self):
        self.misp_backend = ExpandedPyMISP(
            OCD_DTL_MISP_HOST,
            OCD_DTL_MISP_API_KEY,
            ssl=OCD_DTL_MISP_USE_SSL,
            timeout=60,
        )

        # Init a common thread pool to run sync operation in background
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=OCD_DTL_MISP_WORKER)

    @ignore(Exception, message='Skipping event insertion in misp since an error occurred')
    def add_event(self, event: DtlMispEvent):
        """Add a new event into the misp. If the event already exist, it is ignored"""
        misp_event = MISPEvent()
        misp_event.load(event)
        if not self.misp_backend.event_exists(misp_event):
            return self.misp_backend.add_event(misp_event, pythonify=True)

    def add_events(self, events: Iterable):
        """Add events in batch by calling add_event"""
        start_time = timeit.default_timer()

        if not self.thread_pool:
            logger.warning('Add events called while misp is already shutdown')
            return  # close() has already been called

        # Use the thread_pool to perform several insertion in parallel
        results = []
        futures = [self.thread_pool.submit(self.add_event, event=event) for event in events]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

        logger.debug(
            'MISP: Done with the insertion of %s events, after %1.2fs',
            len(events),
            timeit.default_timer() - start_time,
        )
        return results

    def close(self):
        """Close the misp connection by finishing to push events marked for insertion"""
        logger.warning('Gracefully shutting down the misp connector')
        self.thread_pool.shutdown(wait=True)
        self.thread_pool = None
