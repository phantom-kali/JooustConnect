from django.core.management.base import BaseCommand
from socialapp.models import Group
from django.db import transaction

class Command(BaseCommand):
    help = 'Remove duplicate groups and keep one instance of each'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            seen_names = set()
            for group in Group.objects.all():
                if group.name in seen_names:
                    group.delete()
                    self.stdout.write(self.style.WARNING(f"Deleted duplicate group: {group.name}"))
                else:
                    seen_names.add(group.name)
            self.stdout.write(self.style.SUCCESS('Duplicates removed successfully.'))
