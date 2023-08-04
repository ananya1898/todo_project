from background_task import background
from .views import SendEmail
from django.utils import timezone
import datetime


@background(schedule=timezone.now())
def scheduled_task_to_send_overdue_reminder():
    SendEmail.identify_overdue_tasks_and_send_email()


scheduled_task_to_send_overdue_reminder(repeat=scheduled_task_to_send_overdue_reminder.DAILY)
