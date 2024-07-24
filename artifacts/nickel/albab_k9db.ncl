{
  artifact_url = "https://github.com/brownsys/K9db/archive/refs/tags/osdi2023.zip",
  type = "zip",
  doi = "...",
  comment = "",
  dockerfile_location = "K9db-osdi2023",
  package_managers = [ "dpkg", "pip" ],
  git_packages = [],
  misc_packages = [
    { name = "bazel-4.0.0-installer-linux-x86_64", url = "https://github.com/bazelbuild/bazel/releases/download/4.0.0/bazel-4.0.0-installer-linux-x86_64.sh" },
    { name = "rust", url = "https://sh.rustup.rs" },
    { name = "mariadb-connector-cpp-1.0.0-ubuntu-groovy-amd64", url = "https://dlm.mariadb.com/1601342/Connectors/cpp/connector-cpp-1.0.0/mariadb-connector-cpp-1.0.0-ubuntu-groovy-amd64.tar.gz" }
  ],
  python_venvs = [
    { path = "/home/k9db/experiments/scripts/plotting/venv" }
  ]
}
