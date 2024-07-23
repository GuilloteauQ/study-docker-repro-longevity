{
  artifact_url = "https://zenodo.org/record/7004393/files/deinsum/sc22-artifact-0.4.zip",
  type = "zip",
  comment = "",
  doi = "10.5555/3571885.3571918",
  image_name = "deinsum:artefact_gpu",
  dockerfile_location = "deinsum-sc22-artifact-7559901/docker_gpu",
  package_managers = [ "dpkg", "pip" ],
  git_packages = [
    { name = "dace", location = "/dace" },
    { name = "multilinear-algebra-sc22-artifact", location = "/multilinear-algebra-sc22-artifact" },
    { name = "ctf", location = "/ctf" }
  ],
  misc_packages = [
    { name = "pip", url = "https://bootstrap.pypa.io/get-pip.py" }
  ],
}
