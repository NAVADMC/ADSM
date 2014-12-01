from multiprocessing.managers import SyncManager
from multiprocessing.pool import Pool
import queue
import types


class DjangoQueue(queue.Queue):
    pass
    # def get(self, block=True, timeout=None):
    #     import django
    #     django.setup()
    #
    #     return super(DjangoQueue, self).get(block=block, timeout=timeout)


def django_queue_get(self, block=True, timeout=None):
    import django
    django.setup()

    print("IN OUR GET!!!")
    return self.old_get()


def django_queue_put(self, item, block=True, timeout=None):
    import django
    django.setup()

    return self.old_put()


class DjangoManager(SyncManager):
    def Queue(self, maxsize=None):
        new_queue = super(DjangoManager, self).Queue(maxsize=maxsize)

        new_queue.old_get = types.MethodType(new_queue.get, new_queue)
        new_queue.get = types.MethodType(django_queue_get, new_queue)

        new_queue.old_put = types.MethodType(new_queue.put, new_queue)
        new_queue.put = types.MethodType(django_queue_put, new_queue)

        return new_queue


class DjangoPool(Pool):
    _wrap_exception = False

    def __init__(self, processes=None, initializer=None, initargs=()):
        super(DjangoPool, self).__init__(processes, initializer, initargs)

        # self._taskqueue.old_get = types.MethodType(self._taskqueue.get, self._taskqueue)
        # self._taskqueue.get = types.MethodType(django_queue_get, self._taskqueue)
        #
        # self._taskqueue.old_put = types.MethodType(self._taskqueue.put, self._taskqueue)
        # self._taskqueue.put = types.MethodType(django_queue_put, self._taskqueue)

    def __reduce__(self):
        return super(DjangoPool, self).__reduce__()