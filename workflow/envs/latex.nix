{ pkgs, kapkgs }:

pkgs.mkShell {
  packages = with pkgs; [
    texliveFull
    rubber
  ];
}
