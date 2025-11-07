{ python3Packages }:
with python3Packages;
buildPythonPackage {
  pname = "lisa-flask";
  version = "1.0";

  pyproject = true;
  build-system = [ setuptools ];

  propagatedBuildInputs = [
    werkzeug
    pyyaml

    flask
    flask-httpauth
    click

    waitress
  ];

  pythonImportsCheck = [ "lisa_flask" ];

  src = ./lisa_flask;
}
