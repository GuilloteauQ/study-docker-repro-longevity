{
  artifact_url = "http://localhost/artifact.zip",
  type = "zip",
  doi = "...",
  image_name = "prog:latest",
  dockerfile_location = "./",
  package_managers = [ "dpkg", "pip" ],
  git_packages = [
    { name = "pkg1", location = "/pkg1"}
  ],
  misc_packages = [
    { name = "mpkg1", url = "http://localhost/package1.zip" }
  ],
}
