import csv
import os

def get_blacklisted(blacklist_dir_path):
    blacklisted = set()
    if os.path.exists(blacklist_dir_path):
        for blacklist in os.listdir(blacklist_dir_path):
            if not os.path.isdir(blacklist):
                blacklist_csv_path = os.path.join(blacklist_dir_path, blacklist)
                with open(blacklist_csv_path, "r") as csv_file:
                    spamreader = csv.reader(csv_file, delimiter=",")
                    for row in spamreader:
                        blacklisted.add(row[0])
    return blacklisted

#def get_artifacts_to_build(artifacts_folder, blacklist_dir_path):
#    blacklisted = get_blacklisted(blacklist_dir_path)
#    all_artifacts = set([os.path.splitext(a)[0] for a in os.listdir(artifacts_folder) if not os.path.isdir(os.path.join(artifacts_folder, a))])
#    artifacts_to_build = list(all_artifacts.difference(blacklisted))
#    if artifacts_to_build != []:
#        return list(all_artifacts.difference(blacklisted))
#    else:
#        raise(Exception(f"There is no artifact to build! Either no artifact configuration files have been found, or they have all been blacklisted."))

def get_artifacts_to_build(artifacts_folder):
    return [os.path.splitext(a)[0] for a in os.listdir(artifacts_folder) if not os.path.isdir(os.path.join(artifacts_folder, a))]
