configfile: "config/config.yaml"

include: "utils.smk"

import os

ARTIFACTS_FOLDER_NICKEL = config["folder_artifacts_nickel"]
ARTIFACTS_FOLDER_JSON   = config["folder_artifacts_json"]
SYSTEM = config["system"]
PREFIX = config["prefix"]

rule main:
  input:
    lambda w: expand(f"{PREFIX}/{{{{conference}}}}/build_status/{{artifact}}/{{{{date}}}}.csv",\
           artifact=get_artifacts_to_build(ARTIFACTS_FOLDER_NICKEL + "/" + w['conference']))
  output:
    "{conference}_{date}.ok"
  shell:
    "echo {input} > {output}"

rule check_artifact:
  input:
    "flake.nix",
    "flake.lock",
    contract="workflow/nickel/artifact_contract.ncl",
    artifact=f"{ARTIFACTS_FOLDER_NICKEL}/{{conference}}/{{artifact}}.ncl"
  output:
    f"{ARTIFACTS_FOLDER_JSON}/{{conference}}/{{artifact}}.json"
  shell:
    """
    nickel export --format json --output {output} <<< 'let {{Artifact, ..}} = import "{input.contract}" in ((import "{input.artifact}") | Artifact)'
    """

# ECG:

rule run_ecg:
  input:
    "flake.nix",
    "flake.lock",
    ecg="ecg/app/ecg.py",
    execo_wrapper="workflow/scripts/submission_g5k.py",
    oar_wrapper="workflow/scripts/ecg_oar_wrapper.oar.bash",
    artifact=f"{ARTIFACTS_FOLDER_JSON}/{{conference}}/{{artifact}}.json"
  output:
    log           = f"{PREFIX}/{{conference}}/logs/{{artifact}}/{{date}}.txt",
    pkg           = f"{PREFIX}/{{conference}}/pkgs/{{artifact}}/{{date}}.csv",
    build_status  = f"{PREFIX}/{{conference}}/build_status/{{artifact}}/{{date}}.csv",
    artifact_hash = f"{PREFIX}/{{conference}}/artifact_hash/{{artifact}}/{{date}}.csv",
  shell:
    (f"python3 {{input.execo_wrapper}} --path {os.getcwd()} \
                                       --script {{input.oar_wrapper}} \
                                       --site {config['site']} \
                                       --cluster {config['cluster']} \
                                       --max-duration {config['max_duration']} \
                                       --checkpoint {config['checkpoint']} \
                                     {'--besteffort' if config['besteffort'] else ''} \
                                       --sleep_time {config['sleep_time']} \
                                       --build_status_file {{output.build_status}} \
                                       --artifact {{wildcards.artifact}} -- '" if SYSTEM == "g5k" else "") + \
    "nix shell .#ecg --command ecg -p {output.pkg} -b {output.build_status} -a {output.artifact_hash} -l {output.log} {input.artifact}" + \
    ("'" if SYSTEM == "g5k" else "echo \"{input.artifact}, `date +%s.%N`, script_crash\" > {output.build_status}")
