"""Custom management command to import data into database."""
import csv
import logging

from apps.api.models import Menu
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Custom management command to read the data from csv file and insert it
    into the database.

    Parameters
    ----------
    BaseCommand : django.core.management.base
    """

    def handle(self, *args, **options):  # noqa: D102
        # check if the data already inserts into the database
        if Menu.objects.exists():
            logger.info("Data already have inserted into the database.")
        else:
            # read the data from the csv file and saves each record
            # in the database
            with open("data/dataset.csv") as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=",")
                line_count = 0
                for row in csv_reader:
                    try:
                        dataset = Menu.objects.create(**row)
                    except Exception:
                        logger.exception(f"unable to insert row: {row}")
                    else:
                        logger.info(f"row inserted: {dataset.id}-{row}")
                        line_count += 1

            logger.info(
                f"Successfully added {line_count} lines into the database."
            )
