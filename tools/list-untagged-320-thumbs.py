import argparse
import datetime


def main():
    parser = argparse.ArgumentParser(description="List non-tagged 320 thumbs "
        "to the standard output")
    parser.add_argument('database', help='Pixtore database')
    args = parser.parse_args()

    from pixortdata.repositories import sa_pixort_data

    pixtore = sa_pixort_data(args.database)

    classification = pixtore.get_classification('Initial cleanup')
    category, = [c for c in classification.categories if c.name == '0']

    zerotime = datetime.datetime(1900, 1, 1)

    for picture in pixtore.pictures():
        for thumb in picture.thumbnails:
            thumb_key = thumb.key

            # Get the raw
            raw = pixtore.raw_by_key(thumb_key)

            for cat in raw.get_categories():
                if cat == category:
                    date = picture.datetime or zerotime
                    print date.strftime('%Y-%m-%d_%H:%M:%S'), thumb_key


if __name__ == "__main__":
    main()
