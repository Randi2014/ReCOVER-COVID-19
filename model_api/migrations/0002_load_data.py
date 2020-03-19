# Generated by Django 3.0.4 on 2020-03-19 21:06

from django.db import migrations
import csv
import datetime

COVID_19_CSV_PATH = "data/time_series_19-covid-Confirmed.csv"


def load_covid19_data(apps, schema_editor):
    Area = apps.get_model('model_api', 'Area')
    Covid19DataPoint = apps.get_model('model_api', 'Covid19DataPoint')

    with open(COVID_19_CSV_PATH) as f:
        reader = csv.reader(f)
        header = next(reader, None)

        for row in reader:
            state = row[0]
            country = row[1]
            lat = float(row[2])
            long = float(row[3])

            # Write new infection area to database.
            area = Area(state=state, country=country, lat=lat, long=long)
            area.save()

            for i in range(4, len(header)):
                raw_date = header[i]
                date = datetime.datetime.strptime(raw_date, "%m/%d/%y").strftime("%Y-%m-%d")
                val = int(row[i])

                # Write new infection data to database.
                covid19_data_point = Covid19DataPoint(area=area, date=date, val=val)
                covid19_data_point.save()


def delete_covid19_data(apps, schema_editor):
    Area = apps.get_model('model_api', 'Area')
    Covid19DataPoint = apps.get_model('model_api', 'Covid19DataPoint')

    # Clear any previously-existing data.
    Area.objects.all().delete()
    Covid19DataPoint.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('model_api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_covid19_data, delete_covid19_data),
    ]
