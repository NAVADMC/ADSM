from django.db import models, connections, transaction
from django.db.models import Expression, Value, When, Case

from ADSM import __version__


class SimulationProcessRecord(models.Model):
    is_parser = models.BooleanField(default=True)
    pid = models.IntegerField(default=0)
    time_created = models.DateTimeField(auto_now_add=True)


class SingletonManager(models.Manager):
    def get(self, **kwargs):
        if kwargs:
            return self.get_or_create(**kwargs)[0]
        else:
            return super(SingletonManager, self).get_or_create(id=1)[0]

    def get_or_create(self, **kwargs):
        kwargs.pop('id', None)  # make sure there's no id specified
        kwargs.pop('pk', None)
        try:  # modify an existing copy by overwriting with additional values
            result = super(SingletonManager, self).get()
            for key in kwargs:
                setattr(result, key, kwargs[key])
            if len(kwargs):
                result.save()
            return result, False
        except:
            return super(SingletonManager, self).get_or_create(id=1, **kwargs)

    def create(self, **kwargs):
        return self.get_or_create(**kwargs)[0]
    

class SmSession(models.Model):
    scenario_filename = models.CharField(max_length=255, default="Untitled Scenario", blank=True)
    unsaved_changes = models.BooleanField(default=False)
    update_available = models.CharField(max_length=25, default=None, null=True, blank=True, help_text='Is there are new version of ADSM available?')
    simulation_version = models.CharField(max_length=25, default=None, null=True, blank=True, help_text='ADSM Simulation version.')
    population_upload_status = models.CharField(default='', null=True, blank=True, max_length=255)
    population_upload_percent = models.FloatField(default=0)
    simulation_has_started = models.BooleanField(default=False)
    iteration_text = models.TextField(default='')
    show_help_text = models.BooleanField(default=True)
    calculating_summary_csv = models.BooleanField(default=False)
    combining_outputs = models.BooleanField(default=False)
    show_help_overlay = models.BooleanField(default=True)


    @property
    def current_version(self):
        return __version__

    def set_population_upload_status(self, status=None, percent=None):
        if status:
            self.population_upload_status = status
        if percent:
            self.population_upload_percent = float(percent)
        self.save()

    def reset_population_upload_status(self):
        self.population_upload_status = None
        self.population_upload_percent = 0
        self.save()
    
    ## Singleton code
    objects = SingletonManager()
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.id=1
        return super(SmSession, self).save(force_insert, force_update, using, update_fields)


def unsaved_changes(new_value=None):
    session = SmSession.objects.get()  # This keeps track of the state for all views and is used by basic_context
    if new_value is not None:  # you can still set it to False
        session.unsaved_changes = new_value
        session.save()
    return session.unsaved_changes


class BulkUpdateManager(models.Manager):
    def bulk_update(self, objs, fields, batch_size=None):
        """
        Update the given fields in each of the given objects in the database.

        TODO NOTE: This is taken from the dev version of Django (what will be 2.2)
        and modified to work in this older Django.

        There are assumptions for SQLite built in now, and features missing.
        So don't rely too heavily on this without testing the end results.

        IF/WHEN we update Django, this should be REMOVED.
        """
        if batch_size is not None and batch_size < 0:
            raise ValueError('Batch size must be a positive integer.')
        if not fields:
            raise ValueError('Field names must be given to bulk_update().')
        objs = tuple(objs)
        if not all(obj.pk for obj in objs):
            raise ValueError('All bulk_update() objects must have a primary key set.')
        fields = [self.model._meta.get_field(name) for name in fields]
        if any(not f.concrete or f.many_to_many for f in fields):
            raise ValueError('bulk_update() can only be used with concrete fields.')
        if any(f.primary_key for f in fields):
            raise ValueError('bulk_update() cannot be used with primary key fields.')
        if not objs:
            return
        # PK is used twice in the resulting update query, once in the filter
        # and once in the WHEN. Each field will also have one CAST.
        max_batch_size = connections[self.db].ops.bulk_batch_size(['pk', 'pk'] + fields, objs)
        batch_size = min(batch_size, max_batch_size) if batch_size else max_batch_size
        batches = (objs[i:i + batch_size] for i in range(0, len(objs), batch_size))
        updates = []
        for batch_objs in batches:
            update_kwargs = {}
            for field in fields:
                when_statements = []
                for obj in batch_objs:
                    attr = getattr(obj, field.attname)
                    if not isinstance(attr, Expression):
                        attr = Value(attr, output_field=field)
                    when_statements.append(When(pk=obj.pk, then=attr))
                case_statement = Case(*when_statements, output_field=field)
                update_kwargs[field.attname] = case_statement
            updates.append(([obj.pk for obj in batch_objs], update_kwargs))
        with transaction.atomic(using=self.db, savepoint=False):
            for pks, update_kwargs in updates:
                self.filter(pk__in=pks).update(**update_kwargs)

    bulk_update.alters_data = True
