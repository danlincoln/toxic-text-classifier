# This migration script loads the database from data/train.csv if no records
# are present when Django migrate is run.

from ..classifier import preprocess
from django.apps.registry import Apps
from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
import logging
import multiprocessing
import pandas
import time

logging.basicConfig(
    format="%(asctime)s [%(name)s] %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("LoadData")

csvfile = "/data/train.csv"

num_processors = max(1, multiprocessing.cpu_count())
num_savers = 1


def process_data(
    unprocessed_queue: multiprocessing.Queue,
    processed_queue: multiprocessing.Queue,
) -> None:
    """Data preprocessing worker for multi-processing."""
    while True:
        text = unprocessed_queue.get()
        if text is None:  # None means done.
            processed_queue.put(None)
            break
        text.processed = preprocess(text.unprocessed)
        processed_queue.put(text)  # Hand off the record to the saver queue.


def save_data(processed_queue: multiprocessing.Queue) -> None:
    """Data saving worker for multi-processing."""
    count_done = 0
    while True:
        text = processed_queue.get()
        # A number of Nones equal to number of preprocessors means done.
        if text is None:
            count_done += 1
            if count_done == num_processors:
                break
        else:
            text.save()
            text.humanrating.save()
            text.humanrating.humanratingclass.save()


def load_data(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    """Load records from CSV"""

    start = time.time()
    Text = apps.get_model("classifier_app", "Text")
    if Text.objects.count() > 0:
        logger.info("Database is loaded already, skipping CSV load.")
        return  # Do not load if the database has records.

    logger.info("Beginning data preprocessing and load from CSV.")

    HumanRating = apps.get_model("classifier_app", "HumanRating")
    HumanRatingClass = apps.get_model("classifier_app", "HumanRatingClass")

    # Distribute preprocessing across multiple processes to speed up the app.
    unprocessed_queue = multiprocessing.Queue(maxsize=20)
    processed_queue = multiprocessing.Queue(maxsize=20)

    # Build preprocessor work pool.
    logger.info(f"Building processor pool: {num_processors} processes")
    processor_pool = multiprocessing.Pool(
        num_processors, process_data, (unprocessed_queue, processed_queue)
    )

    # Build saver work pool.
    logger.info(f"Building saver pool: {num_savers} processes")
    saver_pool = multiprocessing.Pool(
        num_savers, save_data, (processed_queue,)
    )

    # Load from the CSV.
    df = pandas.read_csv(csvfile)
    length = len(df)
    threshold = length // 100
    for i, series in df.iterrows():
        # Create & load model objects, then send to preprocessors and savers.
        text = Text(id=series["id"], unprocessed=series["comment_text"])
        text.humanrating = HumanRating(
            text=text,
            raw_rating=series["target"],
            rating=series["target"] >= 0.5,
        )
        text.humanrating.humanratingclass = HumanRatingClass(
            severe_toxicity=series["severe_toxicity"],
            obscene=series["obscene"],
            threat=series["threat"],
            insult=series["insult"],
            identity_attack=series["identity_attack"],
            sexual_explicit=series["sexual_explicit"],
        )
        unprocessed_queue.put(text)  # Send the work for processing.
        if i % threshold == 0:
            logger.info(f"Loading data: {i/length:4.0%}")

    # Put enough Nones into the queue to stop the preprocessors & savers.
    for _ in range(num_processors):
        unprocessed_queue.put(None)

    processor_pool.close()
    processor_pool.join()

    saver_pool.close()
    saver_pool.join()

    min, sec = divmod(time.time() - start, 60)
    logger.info(f"Data loading completed in {int(min)}m {int(sec)}s.")


class Migration(migrations.Migration):

    dependencies = [
        ("classifier_app", "0001_initial"),
    ]

    operations = [migrations.RunPython(load_data)]
