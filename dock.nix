{
  pkgs ? import <nixpkgs> { },
  python3Packages ? pkgs.python313Packages,
  lisa-flask ? pkgs.callPackage ./package.nix {inherit python3Packages;},
  pyenv ? python3Packages.python.withPackages(ps: [lisa-flask]),

  tag ? "latest",
  port ? "80",
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
      "-m"
      "lisa_flask"
    ];
    Env = [
      ''LISA_HTTP_PORT="${port}"''
      ''PYTHONDONTWRITEBYTECODE="1"''
      ''PYTHONUNBUFFERED=1''
      # "LISA_HTTP_HOST" = host;
    ];
    Volumes = {
      "/data" = {};
    };
    ExposedPorts = {
      "${port}/tcp" = { };
    };
  };
}
