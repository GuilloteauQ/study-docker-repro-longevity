{
  version = "1.0",
  artifact_url = "https://github.com/microsoft/nnfusion/archive/refs/heads/osdi2023welder.zip",
  type = "zip",
  doi = "",
  conf_date = 2023,
  comment = "",
  buildfile_dir = "nnfusion-osdi2023welder",
  virtualization = "docker",
  package_managers = [ "dpkg", "pip", "conda" ],
  git_packages = [
    { name = "tvm", location = "/root/tvm" },
    { name = "nnfusion", location = "/root/nnfusion" },
    { name = "cutlass", location = "/root/cutlass" }
  ],
  misc_packages = [
    {
        name = "Miniconda3-py310_23.1.0-1-Linux-x86_64",
        url = "https://repo.anaconda.com/miniconda/Miniconda3-py310_23.1.0-1-Linux-x86_64.sh"
    }
  ],
  python_venvs = []
}
