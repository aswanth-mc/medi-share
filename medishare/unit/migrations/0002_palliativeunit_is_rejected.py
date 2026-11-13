from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='palliativeunit',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='palliativeunit',
            name='rejection_reason',
            field=models.TextField(blank=True),
        ),
    ]
