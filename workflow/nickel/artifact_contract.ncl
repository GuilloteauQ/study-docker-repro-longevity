let
  conf = {
    ARCHIVE_FORMATS = ["zip", "tar"],
    PACKAGE_MANAGERS = ["dpkg", "rpm", "pacman", "pip", "conda"],
    FILEPATH_REGEX = "^[^\\x00]+$", # For UNIX, anything of length > 0 but without NULL characters, found at: https://stackoverflow.com/questions/537772/what-is-the-most-correct-regular-expression-for-a-unix-file-path
    URL_REGEX = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$", # Found at: https://uibakery.io/regex-library/url
    IMAGENAME_REGEX = "^[a-z0-9]+(([.]{0,1}|[_]{0,2}|[-]*)[a-z0-9]+)*(:[a-zA-Z0-9_]+[a-zA-Z0-9._-]*){0,1}$", # Based on, with modifications: https://regexr.com/3bsog
    VERNUMBER_REGEX = "[0-9]+(\\.([0-9])+)*"
  }
in
{
  PackageManager = std.contract.from_predicate (
      fun value => std.array.any (fun x => x == value) conf.PACKAGE_MANAGERS
  ),
  ArchiveType = std.contract.from_predicate (
      fun value => std.array.any (fun x => x == value) conf.ARCHIVE_FORMATS
  ),
  FilePath = std.contract.from_predicate (
      fun value => std.string.is_match conf.FILEPATH_REGEX value
  ),
  URL = std.contract.from_predicate (
      fun value => std.string.is_match conf.URL_REGEX value
  ),
  VersionNumber = std.contract.from_predicate (
      fun value => std.string.is_match conf.VERNUMBER_REGEX value
  ),
  GitPackage = {
    name
      | doc "Name of the package for future identification"
      | String,
    location
      | doc "Path where cloned in the container"
      | FilePath
  },
  MiscPackage = {
    name
      | doc "Name of the package for future identification"
      | String,
    url
      | doc "URL of the package. Will be used to compute the hash"
      | URL
  },
  PythonVenv = {
    path
      | doc "Path to the Python venv."
      | FilePath
  },
  Artifact = {
    version
      | doc "Version of the Nickel contract"
      | String,
    artifact_url
      | doc "URL where to download the artifact"
      | URL,
    type
      | doc "Type of the archive. Possible values: zip, tar"
      | ArchiveType,
    doi
      | doc "DOI of the artifact"
      | String,
    comment
      | doc "Additional comments on the artifact that couldn't be written elsewhere"
      | String,
    dockerfile_location
      | doc "Path to the dockerfile in the artifact"
      | FilePath,
    package_managers
      | doc "Package Managers used in the container. Possible values: dpkg, rpm, pacman, pip, conda"
      | Array PackageManager,
    git_packages
      | doc "Git repositories cloned in the container"
      | Array GitPackage,
    misc_packages
      | doc "Misc. packages downloaded from the container"
      | Array MiscPackage,
    python_venvs
      | doc "Python venvs created in the container"
      | Array PythonVenv
  }
}
