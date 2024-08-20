import csv
import os

def find_last_blacklist(blacklist_dir_path):
    last_blacklist = "0"
    for blacklist in os.listdir(blacklist_dir_path):
        if not os.path.isdir(blacklist):
            # We want the latest one, so the one that has the most recent date
            # as file name:
            curbl_date = int(os.path.splitext(blacklist)[0])
            lastbl_date = int(os.path.splitext(last_blacklist)[0])
            if curbl_date > lastbl_date:
                last_blacklist = blacklist
    return last_blacklist

def get_blacklisted(blacklist_dir_path):
    blacklisted = set()
    if os.path.exists(blacklist_dir_path):
        blacklist_csv_path = os.path.join(blacklist_dir_path, find_last_blacklist(blacklist_dir_path))
        with open(blacklist_csv_path, "r") as csv_file:
            spamreader = csv.reader(csv_file, delimiter=",")
            for row in spamreader:
                blacklisted.add(row[0])
    return blacklisted

def get_artifacts_to_build(artifacts_folder, blacklist_dir_path):
    blacklisted = get_blacklisted(blacklist_dir_path)
    all_artifacts = set([os.path.splitext(a)[0] for a in os.listdir(artifacts_folder) if not os.path.isdir(os.path.join(artifacts_folder, a))])
    return list(all_artifacts.difference(blacklisted))
