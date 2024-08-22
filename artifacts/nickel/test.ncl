{
  version = "1.0",
  artifact_url = "http://127.0.0.1/artifact.zip",
  type = "zip",
  doi = "...",
  conf_date = 0,
  virtualization = "docker",
  buildfile_dir = "./",
  package_managers = [ "dpkg", "pip" ],
  misc_packages = [
    { name = "mpkg1", url = "http://127.0.0.1/package1.zip" }
  ],
  python_venvs = [
    { path = "/prog" }
  ]
}
