{
  version = "1.0",
  artifact_url = "https://zenodo.org/record/7328505/files/tgopt-artifact.tgz",
  type = "tar",
  doi = "10.1145/3572848.3577490",
  conf_date = 2023,
  comment = "",
  virtualization = "docker",
  buildfile_dir = "tgopt-artifact",
  package_managers = [ "dpkg", "conda" ],
  git_packages = [],
  misc_packages = [
    { name = "Miniconda3-py37_4.12.0-Linux-x86_64", url = "https://repo.anaconda.com/miniconda/Miniconda3-py37_4.12.0-Linux-x86_64.sh" }
  ],
  python_venvs = []
}
