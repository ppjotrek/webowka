# Generated by Django 3.2.25 on 2024-06-05 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leki_app', '0005_drug_other_substances'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
                ('pesel', models.CharField(max_length=11)),
                ('treatment_plan', models.TextField()),
                ('drugs', models.ManyToManyField(blank=True, to='leki_app.Drug')),
            ],
        ),
    ]
