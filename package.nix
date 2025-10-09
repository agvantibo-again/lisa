{ python3Packages }:
with python3Packages;
buildPythonApplication {
  pname = "lisa-flask";
  version = "1.0";

  pyproject = true;
  build-system = [ setuptools ];

  propagatedBuildInputs = [
    flask
    flask-httpauth
  ];

  src = ./.;
}
