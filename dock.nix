{
  pkgs ? import <nixpkgs> { },
  python3Packages ? pkgs.python313Packages,
  lisa-flask ? pkgs.callPackage ./package.nix {inherit python3Packages;},
  pyenv ? python3Packages.python.withPackages(ps: [lisa-flask]),

  tag ? "latest",
  port ? "80",
  host ? "0.0.0.0"
}:

pkgs.dockerTools.buildLayeredImage {
  name = "lisa-flask";
  inherit tag;
  compressor = "zstd";

  contents = [
    pyenv
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
      "-u"
      "-m"
      "lisa_flask"
    ];
    Env = [
      "LISA_HTTP_HOST=${host}"
      "LISA_HTTP_PORT=${port}"
      "PYTHONDONTWRITEBYTECODE=1"
      "PYTHONUNBUFFERED=1"
      "LISA_DATA_DIR=/data"
    ];
    Volumes = {
      "/data" = {};
    };
    ExposedPorts = {
      "${port}/tcp" = { };
    };
  };
}
