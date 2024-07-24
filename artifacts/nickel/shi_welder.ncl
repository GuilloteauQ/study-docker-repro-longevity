{
  artifact_url = "https://github.com/microsoft/nnfusion/archive/refs/heads/osdi2023welder.zip",
  type = "zip",
  doi = "",
  comment = "",
  image_name = "welder_cuda",
  dockerfile_location = "nnfusion-osdi2023welder",
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
