from multiprocessing.managers import SyncManager
import queue


class DjangoQueue(queue.Queue):
    """
        Custom Queue object that sets up django 1.7 app registry
        so that model instances can be depickled from the queue
    """
    def get(self, block=True, timeout=None):
        import django
        django.setup()

        return super(DjangoQueue, self).get(block=block, timeout=timeout)


class DjangoSyncManager(SyncManager):
    pass

DjangoSyncManager.register('DjangoQueue', DjangoQueue)