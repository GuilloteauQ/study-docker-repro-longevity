let { Artifact, .. } = import "../workflow/nickel/artifact_contract.ncl" in
{
  artifact_url = "https://zenodo.org/record/6632461/files/SC22_artifacts_submission.zip",
  type = "zip",
  doi = "10.5555/3571885.3571906",
  image_name = "taxo:artefact",
  dockerfile_location = "SC22_artifacts_submission",
  package_managers = [ "dpkg", "pip" ],
  git_packages = [],
  misc_packages = [],
} | Artifact