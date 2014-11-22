from multiprocessing.managers import SyncManager
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


class DjangoSyncManager(SyncManager):
    def Queue(self, maxsize=None):
        new_queue = super(DjangoSyncManager, self).Queue(maxsize=maxsize)

        new_queue.old_get = types.MethodType(new_queue.get, new_queue)
        new_queue.get = types.MethodType(django_queue_get, new_queue)

        new_queue.old_put = types.MethodType(new_queue.put, new_queue)
        new_queue.put = types.MethodType(django_queue_put, new_queue)

        return new_queue