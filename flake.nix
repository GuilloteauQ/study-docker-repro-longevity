{
  description = "Flake study docker longevity";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/23.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells = {
        default = pkgs.mkShell {
          packages = with pkgs; [
<<<<<<< HEAD
            snakemake
            gawk
=======
            nickel
>>>>>>> 127c5c5ef4d0e7d4d1826007cdc27c903eb59314
            (python3.withPackages (ps: with ps; [
              requests
              pyyaml
            ]))
          ];
        };
      };
    });
}
