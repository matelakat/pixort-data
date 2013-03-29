import argparse


def main():
    parser = argparse.ArgumentParser(description="Import metadata from"
        " a filestore")
    parser.add_argument('repo', help='Filestore location')
    parser.add_argument('database', help='Pixtore database to import into')
    args = parser.parse_args()

    import fs
    from filestore import repository

    directory = fs.Directory(args.repo)
    repo = repository.Repository(directory)

    from pixortdata.repositories import sa_pixort_data

    pixtore = sa_pixort_data(args.database)

    for obj in repo.objects():
        pixtore.create(obj.checksum, obj.metadata)


if __name__ == "__main__":
    main()
