let { Artifact, .. } = import "artifact_contract.ncl" in
(
  (import "artifacts_nickel/example.ncl") | Artifact
)
