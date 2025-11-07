{
  pkgs ? import <nixpkgs> { },
  python3Packages ? pkgs.python313Packages,
  lisa-flask ? pkgs.callPackage ./package.nix {inherit python3Packages;},
  py_environment ? python3Packages.python.withPackages(ps: [lisa-flask]),

  tag ? "latest",
  port ? "80",
  host ? "0.0.0.0"
}:

let
#   cyr_wordlist = pkgs.stdenvNoCC.mkDerivation {
#     src = pkgs.fetchurl {
#       url = "https://gist.githubusercontent.com/kissarat/bd30c324439cee668f0ac76732d6c825/raw/147eecc9a86ec7f97f6dd442c2eda0641ddd78dc/russian-mnemonic-words.txt";
#       hash = pkgs.lib.fakeHash;
#     };
#     noExtract = true;
#     installPhase = ''
#       cp $src/russian-mnemonic-words.txt $out
#     '';
#   };
  cyr_wordlist = pkgs.fetchurl {
      url = "https://gist.githubusercontent.com/kissarat/bd30c324439cee668f0ac76732d6c825/raw/147eecc9a86ec7f97f6dd442c2eda0641ddd78dc/russian-mnemonic-words.txt";
      hash = "sha256-meSxfRt6d/Hhopb0XIumAPCIVi9QcQ1WR05l89IZXT8=";
    };
in
pkgs.dockerTools.buildLayeredImage {
  name = "lisa-flask";
  inherit tag;
  compressor = "zstd";

  contents = [
    py_environment
    # developer tools
    pkgs.bash
  ];

  extraCommands = ''
    #!${pkgs.stdenv.shell}
    mkdir -p data
  '';

  config = {
    Entrypoint = "/bin/python";
    Cmd = [
      "-m"
      "lisa_flask"
    ];
    Env = [
      "FLASK_APP=lisa_flask:mk_app"
      "LISA_HTTP_HOST=${host}"
      "LISA_HTTP_PORT=${port}"
      "PYTHONDONTWRITEBYTECODE=1"
      "PYTHONUNBUFFERED=1"
      "LISA_DATA_DIR=/data"
      "LISA_PASSWORD_DICT=${cyr_wordlist}"
    ];
    Volumes = {
      "/data" = {};
    };
    ExposedPorts = {
      "${port}/tcp" = { };
    };
  };
}
