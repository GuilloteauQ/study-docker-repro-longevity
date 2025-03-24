{
  description = "Flake study docker longevity";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/23.11";
    flake-utils.url = "github:numtide/flake-utils";
    kapack.url = "github:oar-team/nur-kapack";
    kapack.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, flake-utils, kapack }:
    flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };
      kapkgs = kapack.packages.${system};
    in
    {
      packages = {
        ecg = pkgs.python3Packages.buildPythonPackage {
          name = "ecg";
          version = "0.0.1";
          src = ./ecg;
          propagatedBuildInputs = with (pkgs.python3Packages); [
            requests
          ];
          doCheck = false;
        };
      };
      devShells = {
        default  = import ./workflow/envs/snakemake.nix { inherit pkgs kapkgs; };
        nickel   = import ./workflow/envs/nickel.nix { inherit pkgs kapkgs; };
        latex    = import ./workflow/envs/latex.nix { inherit pkgs kapkgs; };
        analysis = import ./workflow/envs/analysis.nix { inherit pkgs kapkgs; };
      };
    });
}
