{
  version = "1.0",
  artifact_url = "https://zenodo.org/record/7004393/files/deinsum/sc22-artifact-0.4.zip",
  type = "zip",
  comment = "",
  doi = "10.5555/3571885.3571918",
  conf_date = 2022,
  virtualization = "docker",
  buildfile_dir = "deinsum-sc22-artifact-7559901/docker_gpu",
  package_managers = [ "dpkg", "pip" ],
  git_packages = [
    { name = "dace", location = "/dace" },
    { name = "multilinear-algebra-sc22-artifact", location = "/multilinear-algebra-sc22-artifact" },
    { name = "ctf", location = "/ctf" }
  ],
  misc_packages = [
    { name = "pip", url = "https://bootstrap.pypa.io/get-pip.py" }
  ],
  python_venvs = []
}
