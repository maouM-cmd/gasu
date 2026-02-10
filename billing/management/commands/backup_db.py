import os
import gzip
import shutil
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Backup SQLite DB file to backups/ with timestamp (gzipped)'

    def handle(self, *args, **options):
        db_path = settings.BASE_DIR / 'db.sqlite3'
        if not db_path.exists():
            self.stderr.write('No db.sqlite3 found')
            return
        backups_dir = settings.BASE_DIR / 'backups'
        backups_dir.mkdir(exist_ok=True)
        ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        out_name = backups_dir / f'db_{ts}.sqlite3'
        shutil.copy2(db_path, out_name)
        # gzip it
        with open(out_name, 'rb') as f_in, gzip.open(str(out_name) + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        os.remove(out_name)
        self.stdout.write(self.style.SUCCESS(f'Backup created: {out_name}.gz'))
