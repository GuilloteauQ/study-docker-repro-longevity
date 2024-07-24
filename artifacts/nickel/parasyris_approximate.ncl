{
  artifact_url = "https://zenodo.org/record/6926481/files/koparasy/HPAC-v0.0.0-Puppeteer.zip",
  type = "zip",
  doi = "10.5555/3571885.3571974",
  comment = "The package 'cmake-3.14.0-Linux-x86_64' is not specified below, because it is installed using a Bash script included in the artifact archive itself. The file puppet_env.sh is missing and may hold information about a possible Python venv.",
  image_name = "puppeteer:artefact",
  dockerfile_location = "koparasy-HPAC-2723bb8/approx/puppeteer/container",
  package_managers = [ "dpkg", "pip" ],
  git_packages = [],
  misc_packages = [
    { name = "HPAC", url = "https://github.com/koparasy/HPAC/archive/refs/heads/develop.zip" }
  ],
  python_venvs = []
}
