{ pkgs, kapkgs }:

pkgs.mkShell {
  packages = with pkgs; [
    (rWrapper.override {
      packages = with rPackages; [
        tidyverse
        reshape2
      ];
    })
  ];
}
