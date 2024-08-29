{ pkgs, kapkgs }:

pkgs.mkShell {
  packages = with pkgs; [
    snakemake
    gawk
    gnused
    (python3.withPackages (ps: with ps; [
      kapkgs.execo 
    ]))
  ];
}
