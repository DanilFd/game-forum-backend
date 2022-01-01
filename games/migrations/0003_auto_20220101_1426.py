# Generated by Django 3.2.7 on 2022-01-01 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_usergamerelation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usergamerelation',
            options={'verbose_name': 'Избранная игра', 'verbose_name_plural': 'Избранные игры'},
        ),
        migrations.AlterField(
            model_name='usergamerelation',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_relations', to='games.game'),
        ),
    ]
