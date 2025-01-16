from django.core.management.base import BaseCommand
from main.utils.sync_db import sync_database_schema

class Command(BaseCommand):
    help = 'Synchronise le schéma de la base de données avec Supabase'

    def handle(self, *args, **kwargs):
        self.stdout.write('Début de la synchronisation avec Supabase...')
        try:
            sync_database_schema()
            self.stdout.write(self.style.SUCCESS('Synchronisation réussie !'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors de la synchronisation : {str(e)}'))
