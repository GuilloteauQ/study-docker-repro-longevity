{
  version = "1.0",
  artifact_url = "http://localhost.com/artifact.zip",
  type = "zip",
  doi = "...",
  virtualization = "docker",
  buildfile_dir = "./",
  package_managers = [ "dpkg", "pip" ],
  git_packages = [
    { name = "pkg1", location = "/pkg1" }
  ],
  misc_packages = [
    { name = "mpkg1", url = "http://localhost.com/package1.zip" }
  ]
}
