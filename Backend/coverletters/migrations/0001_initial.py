# Generated by Django 4.2.20 on 2025-04-06 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobdescriptions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoverLetter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('job_description', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cover_letters', to='jobdescriptions.jobdescription')),
            ],
        ),
    ]
