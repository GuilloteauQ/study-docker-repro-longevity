{
  artefact_url = "https://example.com/artifact.zip",
  type = "zip",
  doi = "...",
  image_name = "image:version",
  location = "path/to/docker/folder",
  package_managers = [ "dpkg" ],
  git_packages = [
    { name = "pkg1", location = "path/to/git/repo"}
  ],
  misc_packages = [
    { name = "mpkg1", url = "https://", type = "zip" }
  ],
}
