# Generated by Django 4.2.2 on 2023-08-14 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QoeRating',
            fields=[
                ('qoe_rating_id', models.AutoField(primary_key=True, serialize=False)),
                ('qoe_rating_value', models.IntegerField()),
                ('qoe_rating_perception', models.CharField(max_length=300)),
                ('validation_video_path', models.CharField(max_length=300)),
                ('respondent_validation_video_anwer', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'qoe_rating',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='QoeVideo',
            fields=[
                ('video_id', models.AutoField(primary_key=True, serialize=False)),
                ('video_name', models.CharField(max_length=45)),
                ('packet_loss_value', models.FloatField()),
                ('rtt_value', models.FloatField()),
                ('network', models.CharField(max_length=45)),
                ('video_file_path', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'qoe_video',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Respondent',
            fields=[
                ('respondent_id', models.AutoField(primary_key=True, serialize=False)),
                ('age_range', models.CharField(choices=[('below 18', 'Below 18'), ('18 to 24', '18 to 24'), ('25 to 34', '25 to 34'), ('35 to 44', '35 to 44'), ('45 to 54', '45 to 54'), ('55 to 64', '55 to 64'), ('65 or over', '65 or over')], default='Unspecified', max_length=200)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='None', max_length=45)),
            ],
            options={
                'db_table': 'respondent',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ValidationVideo',
            fields=[
                ('validation_video_id', models.IntegerField(primary_key=True, serialize=False)),
                ('validation_video_name', models.CharField(max_length=45)),
                ('validation_video_file_path', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'validation_video',
                'managed': False,
            },
        ),
    ]
