{ pkgs, kapkgs }:

pkgs.mkShell {
  packages = with pkgs; [
    nickel
  ];
}
