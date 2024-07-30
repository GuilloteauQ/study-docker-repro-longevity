{
  version = "1.0",
  artifact_url = "https://example.com/artifact.zip",
  type = "zip",
  doi = "...",
  comment = "Template for artifact configuration.",
  virtualization = "docker",
  buildfile_dir = "path/to/docker/folder",
  package_managers = [ "dpkg", "rpm", "pacman", "pip", "conda" ],
  git_packages = [
    { name = "pkg1", location = "path/to/git/repo" }
  ],
  misc_packages = [
    { name = "mpkg1", url = "http://example.com/package.zip" }
  ],
  python_venvs = [
    { path = "path/to/venv" }
  ]
}
