import logging

from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            PeriodicTask.objects.get(task="feedreader.tasks.update")
            logger.info("Task found, nothing to do")
        except PeriodicTask.DoesNotExist:
            logger.info("Task not found")
            crontab_schedule, created = CrontabSchedule.objects.get_or_create(
                minute="*/15",
                hour="*",
                day_of_week="*",
                day_of_month="*",
                month_of_year="*",
            )
            logger.info("Schedule created" if created else "Schedule exists")
            PeriodicTask(
                name="Feed update",
                task="feedreader.tasks.update",
                crontab=crontab_schedule,
            ).save()
            logger.info("Created task")
