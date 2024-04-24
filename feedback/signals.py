from django.dispatch import receiver
from django.db.models.signals import post_delete

from feedback.models import Feedback

# When a Feedback entry is removed from the database also remove the recording from R2
@receiver(post_delete, sender=Feedback)
def remove_file_from_r2(sender, instance, using, **kwargs):
    instance.recording_file.delete(save=False)
