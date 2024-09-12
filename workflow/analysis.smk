configfile: "config/config.yaml"
PREFIX = config["prefix"]

include: "utils.smk"
ARTIFACTS_FOLDER_NICKEL = config["folder_artifacts_nickel"]

def get_dates(conference):
  with open(f"dates/{conference}.txt", "r") as f:
    return [d.strip() for d in f.readlines() if len(d.strip()) > 0]

rule all:
  input:
    expand(f"{PREFIX}/aggregated/{{conference}}/{{type}}.csv", type=["pkgs", "artifact_hash", "build_status"], conference=config["conference"])


rule aggregate_per_artifact:
  input:
    lambda w: expand(f"{PREFIX}/{{{{conference}}}}/{{{{type}}}}/{{{{artifact}}}}/{{date}}.csv", date = get_dates(w["conference"]))
  output:
    f"{PREFIX}/aggregated/{{conference}}/{{type}}/{{artifact}}.csv"
  shell:
    "cat {input} > {output}"

rule aggregate_all:
  input:
    lambda w: expand(f"{PREFIX}/{{{{conference}}}}/{{{{type}}}}/{{artifact}}/{{date}}.csv", date = get_dates(w["conference"]), artifact=get_artifacts_to_build(ARTIFACTS_FOLDER_NICKEL + "/" + w['conference']))
    #lambda w: expand(f"{PREFIX}/aggregated/{{{{conference}}}}/{{{{type}}}}/{{artifact}}.csv", artifact=get_artifacts_to_build(ARTIFACTS_FOLDER_NICKEL + "/" + w['conference']))
  output:
    f"{PREFIX}/aggregated/{{conference}}/{{type}}.csv"
  shell:
    "cat {input} > {output}"


    
