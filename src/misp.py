import asyncio
import concurrent
import timeit
from typing import Iterable

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
        self.loop = asyncio.get_event_loop()

        # Init a common thread pool to run sync operation in background
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=OCD_DTL_MISP_WORKER)

    @ignore(Exception, message='Skipping event insertion in misp since an error occurred')
    def add_event(self, event: DtlMispEvent):
        """Add a new event into the misp. If the event already exist, it is ignored"""
        misp_event = MISPEvent()
        misp_event.load(event)
        if not self.misp_backend.event_exists(misp_event):
            return self.misp_backend.add_event(misp_event, pythonify=True)

    async def _add_event(self, event):
        return await self.loop.run_in_executor(self.thread_pool, self.add_event, event)

    def add_events(self, events: Iterable):
        """Add events in batch by calling add_event"""
        self.loop.run_until_complete(self._add_events(events))

    async def _add_events(self, events: Iterable):
        start_time = timeit.default_timer()
        tasks = []

        for event in events:
            tasks.append(self._add_event(event))

        res = await asyncio.gather(*tasks)

        logger.debug(
            'MISP: Done with the insertion of %s events, after %1.2fs',
            len(events),
            timeit.default_timer() - start_time,
        )
        return res
