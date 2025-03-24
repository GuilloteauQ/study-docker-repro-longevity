{
  version = "1.0",
  artifact_url = "https://github.com/dariomnz/xpn-docker/archive/refs/tags/euro-par2024.zip",
  type = "zip",
  doi = "10.5281/zenodo.11544491",
  conf_date = 2024,
  comment = "There are two dockerfiles. a dockerfile from the authors that serves as a base image. we will only rebuild the base image. the top level image appear to be mostly a copy + compile, no install",
  virtualization = "docker",
  buildfile_dir = "xpn-docker-euro-par2024",
  dockerfile_path = "docker/base/dockerfile",
  build_args = [
    "UID=1234",
    "GID=1000"
  ],
  package_managers = [ "dpkg" ],
  misc_packages = [
    { name = "mpich-4.1.1", url = "https://www.mpich.org/static/downloads/4.1.1/mpich-4.1.1.tar.gz" }
  ]
}
