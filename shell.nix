{
  pkgs ? import <nixpkgs> { },
}:
let
  package = pkgs.callPackage ./package.nix { };
in
# pkgs.mkShell {
#   buildInputs =
#     with pkgs;
#     [
#       python3
#       black
#     ]
#     ++ (with pkgs.python3Packages; [
#       flask
#       # flask_httpauth
#     ]);
# }
pkgs.mkShellNoCC {
  buildInputs = with pkgs; [
    python3
    black

    docker
    dive
  ];
  propagatedBuildInputs = package.propagatedBuildInputs;

  "DOCKER_HOST" = "unix:///run/user/1000/docker.sock";
}
