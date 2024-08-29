{
  version = "1.0",
  artifact_url = "https://zenodo.org/records/11558678/files/peanuts-playground.zip",
  type = "zip",
  doi = "10.5281/zenodo.11558678",
  conf_date = 2024,
  comment = "Files in /var/lib/apt/lists/ are removed.",
  virtualization = "docker",
  buildfile_dir = "./",
  package_managers = [ "dpkg" ],
  git_packages = [
    { name = "spack", location = "/home/vscode/.cache/spack" }
  ],
  misc_packages = [
    { name = "cmake-3.22.2-linux", url = "https://github.com/Kitware/CMake/releases/download/v3.22.2/cmake-3.22.2-linux-x86_64.sh" }
  ]
}
