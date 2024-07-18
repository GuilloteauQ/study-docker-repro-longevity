let { Artifact, .. } = import "../workflow/nickel/artifact_contract.ncl" in
{
  artifact_url = "https://example.com/artifact.zip",
  type = "zip",
  doi = "...",
  image_name = "image:version",
  dockerfile_location = "path/to/docker/folder",
  package_managers = [ "dpkg" ],
  git_packages = [
    { name = "pkg1", location = "path/to/git/repo"}
  ],
  misc_packages = [
    { name = "mpkg1", url = "http://example.com/package.zip", type = "zip" }
  ]
} | Artifact
