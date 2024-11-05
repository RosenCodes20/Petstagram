# Generated by Django 5.1.1 on 2024-11-05 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0001_initial'),
        ('photos', '0002_alter_photo_photo_alter_photo_tagged_pets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='tagged_pets',
        ),
        migrations.AddField(
            model_name='photo',
            name='tagged_pets',
            field=models.ManyToManyField(blank=True, null=True, related_name='tagged_pets', to='pets.pet'),
        ),
    ]