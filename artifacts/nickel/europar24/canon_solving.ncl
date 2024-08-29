{
  version = "1.0",
  artifact_url = "https://zenodo.org/records/11636529/files/artifact-pap130.zip",
  type = "zip",
  doi = "10.5281/zenodo.11636529",
  conf_date = 2024,
  virtualization = "docker",
  buildfile_dir = ".docker",
  package_managers = [ "dpkg" ],
  misc_packages = [
    { name = "gurobi10.0.1_linux64", url = "https://packages.gurobi.com/10.0/gurobi10.0.1_linux64.tar.gz" }
  ]
}
