{
  artifact_url = "https://zenodo.org/record/7328505/files/tgopt-artifact.tgz",
  type = "tar",
  doi = "10.1145/3572848.3577490",
  comment = "",
  image_name = "tgopt:artefact",
  dockerfile_location = "tgopt-artifact",
  package_managers = [ "dpkg", "conda" ],
  git_packages = [],
  misc_packages = [
    { name = "Miniconda3-py37_4.12.0-Linux-x86_64", url = "https://repo.anaconda.com/miniconda/Miniconda3-py37_4.12.0-Linux-x86_64.sh" }
  ],
}
