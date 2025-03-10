# Generated by Django 5.1.7 on 2025-03-08 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0004_alter_protein_uniprot_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="protein",
            name="uniprot_accession",
            field=models.CharField(default="", max_length=512, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="protein",
            name="entry_id",
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name="protein",
            name="uniprot_id",
            field=models.CharField(max_length=512),
        ),
    ]
