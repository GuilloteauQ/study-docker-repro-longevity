{
  version = "1.0",
  artifact_url = "https://zenodo.org/record/7544675/files/SF2-code.tar.gz",
  type = "tar",
  doi = "10.1145/3572848.3577480",
  comment = "",
  dockerfile_location = "bdm-paper-examples/docker",
  package_managers = [ "dpkg" ],
  git_packages = [
    { name = "pyenv", location = "~/.pyenv" }
  ],
  misc_packages = [
    {
      name = "NetLogo-6.2.0-64",
      url = "http://ccl.northwestern.edu/netlogo/6.2.0/NetLogo-6.2.0-64.tgz"
    },
    {
      name = "root_v6.22.06_python3.9_ubuntu-20.04",
      url = "http://biodynamo-lfs.web.cern.ch/biodynamo-lfs/third-party/root_v6.22.06_python3.9_ubuntu-20.04.tar.gz"
    },
    {
      name = "qt_v5.12.10_ubuntu-20.04",
      url = "http://biodynamo-lfs.web.cern.ch/biodynamo-lfs/third-party/qt_v5.12.10_ubuntu-20.04.tar.gz"
    },
    {
      name = "paraview_v5.9.0_ubuntu-20.04_default",
      url = "http://biodynamo-lfs.web.cern.ch/biodynamo-lfs/third-party/paraview_v5.9.0_ubuntu-20.04_default.tar.gz"
    },
  ],
  python_venvs = []
}
