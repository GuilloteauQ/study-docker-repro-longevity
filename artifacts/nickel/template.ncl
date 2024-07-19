{
  artifact_url = "https://example.com/artifact.zip",
  type = "zip", # Possible values: zip, tar
  doi = "...",
  image_name = "image:version",
  dockerfile_location = "path/to/docker/folder",
  package_managers = [ "dpkg" ], # Possible values: dpkg, rpm, pacman, pip, conda
  git_packages = [
    { name = "pkg1", location = "path/to/git/repo"}
  ],
  misc_packages = [
    { name = "mpkg1", url = "http://example.com/package.zip" }
  ]
}
