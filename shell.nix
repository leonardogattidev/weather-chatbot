let
  pkgs = import <nixpkgs> {};
in
    pkgs.mkShell {
        packages = with pkgs; [
            python3
            poetry
        ];
    }
