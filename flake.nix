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
      devShells = {
        default = pkgs.mkShell {
          packages = with pkgs; [
            snakemake
            gawk
            nickel
	    # TODO separate into several shells
            (python3.withPackages (ps: with ps; [
              requests
	      kapkgs.execo
            ]))
          ];
        };
      };
    });
}
