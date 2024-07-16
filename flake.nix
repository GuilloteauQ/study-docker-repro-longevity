{
  description = "Flake study docker longevity";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/24.05";
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
            nickel
            (python3.withPackages (ps: with ps; [
              requests
              pyyaml
            ]))
          ];
        };
      };
    });
}
