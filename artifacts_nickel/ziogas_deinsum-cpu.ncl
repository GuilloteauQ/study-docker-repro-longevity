let { Artifact, .. } = import "../workflow/nickel/artifact_contract.ncl" in
{
  artifact_url = "https://zenodo.org/record/7004393/files/deinsum/sc22-artifact-0.4.zip",
  type = "zip",
  doi = "10.5555/3571885.3571918",
  comment = "",
  image_name = "deinsum:artefact-cpu",
  dockerfile_location = "deinsum-sc22-artifact-7559901/docker_cpu",
  package_managers = [ "dpkg", "pip" ],
  git_packages = [
    { name = "dace", location = "/dace"},
    { name = "multilinear-algebra-sc22-artifact", location = "/multilinear-algebra-sc22-artifact"},
    { name = "ctf", location = "/ctf"}
  ],
  misc_packages = [
    {
      name = "mpich-3.1.4",
      url = "http://www.mpich.org/static/downloads/3.1.4/mpich-3.1.4.tar.gz"
    },
    {
      name = "Python-3.10.2",
      url = "https://www.python.org/ftp/python/3.10.2/Python-3.10.2.tgz"
    }
  ],
} | Artifact