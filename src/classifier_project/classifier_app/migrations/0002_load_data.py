# This migration script loads the database from data/train.csv if no records
# are present when Django migrate is run.

from ..classifier import preprocess
from django.db import migrations
import logging
import pandas

logger = logging.getLogger("LoadData")

csvfile = "/data/train.csv"


def load_data(apps, schema_editor):
    """If there are no records in the database yet, load from CSV."""
    Text = apps.get_model("classifier_app", "Text")
    HumanRating = apps.get_model("classifier_app", "HumanRating")
    HumanRatingClass = apps.get_model("classifier_app", "HumanRatingClass")
    if Text.objects.count() == 0:
        logger.info("Loading data...")
        df = pandas.read_csv(csvfile)
        length = len(df)
        for index, row in df.iterrows():
            text = Text(
                id=row["id"],
                unprocessed=row["comment_text"],
                processed=preprocess(row["comment_text"]),
            )
            human_rating = HumanRating(
                text=text,
                raw_rating=row["target"],
                rating=row["target"] >= 0.5,
            )
            human_rating_class = HumanRatingClass(
                human_rating=human_rating,
                severe_toxicity=row["severe_toxicity"],
                obscene=row["obscene"],
                threat=row["threat"],
                insult=row["insult"],
                identity_attack=row["identity_attack"],
                sexual_explicit=row["sexual_explicit"]
            )
            text.save()
            human_rating.save()
            human_rating_class.save()
            if index % 1001 == 0:
                logger.info(f"Loading data: {index/length:6.2%}")


class Migration(migrations.Migration):

    dependencies = [
        ("classifier_app", "0001_initial"),
    ]

    operations = [migrations.RunPython(load_data)]
