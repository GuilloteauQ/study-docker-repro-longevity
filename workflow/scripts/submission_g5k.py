from execo_g5k import oardel, oarsub, OarSubmission, wait_oar_job_start, get_oar_job_nodes, get_oar_job_info
import time
import argparse

def submit_job(cluster, site, maximum_duration_minutes, checkpoint_minutes, is_besteffort, path, script, command):
    reservation_duration = (maximum_duration_minutes + checkpoint_minutes) * 60
    checkpoint = checkpoint_minutes * 60
    job_type = []
    if is_besteffort:
        job_type.append("besteffort")

    oar_job_id, _site = oarsub([(OarSubmission(f"{{cluster='{cluster}'}}/nodes=1",\
                                                reservation_duration,\
                                                job_type=job_type,\
                                                additional_options=f"--checkpoint {checkpoint}",\
                                                command=f"{path}/{script} {path} {command}"), site)])[0]
    return oar_job_id

def wait_for_completion(oar_job_id, site, sleep_time):
    state = "Running"
    while state != "Terminated" and state != "Error":
        time.sleep(sleep_time)
        info = get_oar_job_info(oar_job_id, site)
        state = info["state"]

def main():
    parser = argparse.ArgumentParser(description="Wrapper script to submit to OAR from a namespace")
    parser.add_argument("--site", required=True, help="Grid'5000 site to submit to")
    parser.add_argument("--cluster", required=True, help="Cluster to submit to")
    parser.add_argument("--max-duration", required=True, type=int, help="Max Duration in MINUTES of the docker build")
    parser.add_argument("--checkpoint", required=True, type=int, help="Duration in MINUTES before the end of the job to do the checkpoint")
    parser.add_argument("--besteffort", action='store_false', help="Submit the job as besteffort")
    parser.add_argument("--path", required=True, help="Root of the project")
    parser.add_argument("--script", required=True, help="Path of the bash script to oarsub relative to the '--path'")
    parser.add_argument("--sleep_time", required=False, type=int, default=60, help="Time interval in seconds to check the termination of the job")
    parser.add_argument("command", help="ECG Command")

    args = parser.parse_args()

    oar_job_id = submit_job(args.cluster, args.site, args.max_duration, args.checkpoint, args.besteffort, args.path, args.script, args.command)
    
    wait_oar_job_start(oar_job_id, args.site)

    wait_for_completion(oar_job_id, args.site, args.sleep_time)

    return 0

main()
