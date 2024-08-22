import csv
import os

def get_analysis_dates(directory):
    outputs = []
    if os.path.exists(directory):
        for file in os.listdir(directory):
            if not os.path.isdir(os.path.join(directory, file)):
                outputs.append(os.path.splitext(file)[0])
    today = datetime.datetime.now().strftime("%Y%m%d")
    if today not in outputs:
        outputs.append(today)
    return outputs

# def find_last_blacklist(blacklist_dir_path):
#     last_blacklist = "0.csv"
#     for blacklist in os.listdir(blacklist_dir_path):
#         if not os.path.isdir(blacklist):
#             # We want the latest one, so the one that has the most recent date
#             # as file name:
#             curbl_date = int(os.path.splitext(blacklist)[0])
#             lastbl_date = int(os.path.splitext(last_blacklist)[0])
#             if curbl_date > lastbl_date:
#                 last_blacklist = blacklist
#     return last_blacklist

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

def get_artifacts_to_build(artifacts_folder, blacklist_dir_path):
    blacklisted = get_blacklisted(blacklist_dir_path)
    all_artifacts = set([os.path.splitext(a)[0] for a in os.listdir(artifacts_folder) if not os.path.isdir(os.path.join(artifacts_folder, a))])
    artifacts_to_build = list(all_artifacts.difference(blacklisted))
    if artifacts_to_build != []:
        return list(all_artifacts.difference(blacklisted))
    else:
        raise(Exception(f"There is no artifact to build! Either no artifact configuration files have been found, or they have all been blacklisted."))
