let { Artifact, .. } = import "workflow/nickel/artifact_contract.ncl" in
(
  (import "artifacts_nickel/example.ncl") | Artifact
)
