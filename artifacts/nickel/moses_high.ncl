{
  artifact_url = "https://zenodo.org/record/7508499/files/wsmoses/PolygeistGPU-Docker-v0.2.1.zip",
  type = "zip",
  doi = "10.1145/3572848.3577475",
  comment = "",
  image_name = "polygeist:artefact",
  dockerfile_location = "wsmoses-PolygeistGPU-Docker-ba18197/MocCUDA",
  package_managers = [ "dpkg", "pip" ],
  git_packages = [
    { name = "MocCUDA", location = "/root/MocCUDA" }
  ],
  misc_packages = [
    { name = "cmake-3.23.1", url = "https://github.com/Kitware/CMake/releases/download/v3.23.1/cmake-3.23.1.tar.gz" }
  ],
  python_venvs = [
    { path = "/root/MocCUDA/py3_venv" }
  ]
}
