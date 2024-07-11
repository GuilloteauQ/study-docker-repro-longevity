import csv
import os

def get_blacklisted_paths(blacklist_csv_path):
  blacklisted = set()
  with open(blacklist_csv_path, "r") as csv_file:
    spamreader = csv.reader(csv_file, delimiter=",")
    for row in spamreader:
      blacklisted.add(row[0])
  return blacklisted

def get_artifacts_to_build(artifacts_folder, blacklist_csv_path):
  blacklisted = get_blacklisted_paths(blacklist_csv_path)
  all_artifacts = set([a.split(".")[0] for a in os.listdir(artifacts_folder) if not os.path.isdir(os.path.join(artifacts_folder, a))])
  return list(all_artifacts.difference(blacklisted))
