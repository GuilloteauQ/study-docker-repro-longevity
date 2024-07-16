let
  conf = {
    ARCHIVE_FORMATS = [ "zip", "tar" ],
    PACKAGE_MANAGERS = [ "dpkg", "conda", "pip"] 
  }
in
{
  PackageManager = std.contract.from_predicate (
      fun value => std.array.any (fun x => x == value) conf.PACKAGE_MANAGERS
  ),
  ArchiveType = std.contract.from_predicate (
      fun value => std.array.any (fun x => x == value) conf.ARCHIVE_FORMATS
    ), 
  GitPackage = {
    name
      | doc "Name of the package for future identification"
      | String,
    location
      | doc "Path where cloned in the container"
      | String
  },
  MiscPackage = {
    name
      | doc "Name of the package for future identification"
      | String,
    url
      | doc "URL of the package. Will be used to compute the hash"
      | String,
    type
      | doc "Type of the archive (zip, tar, ...)"
      | ArchiveType,
  },
  Artifact = {
    artefact_url
      | doc "URL where to download the artifact"
      | String,
    type
      | doc "Type of the archive (zip, tar, ...)"
      | ArchiveType,
    doi
      | doc "DOI of the artifact"
      | String,
    image_name
      | doc "Name to give the image when building"
      | String,
    location
      | doc "Path to the dockerfile in the artifact"
      | String,
    package_managers
      | doc "Package Managers used in the container"
      | Array PackageManager,
    git_packages
      | doc "Git repositories cloned in the container"
      | Array GitPackage,
    misc_packages
      | doc "Misc. packages downloaded from the container"
      | Array MiscPackage,
  }
}
