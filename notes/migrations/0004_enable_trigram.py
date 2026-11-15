from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ("notes", "0003_alter_note_options_note_note_created_idx_and_more"),
    ]
    operations = [TrigramExtension()]
