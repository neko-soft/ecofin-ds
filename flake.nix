{
  description = "Entorno de desarrollo Data Scrapper datos financieros y económicos";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };


  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; config.allowUnfree = true; };

        # Importa los paquetes generados con pip2nix

        pythonPackages = import (self + "/python-packages.nix") { inherit pkgs; };

        # Crea el entorno de Python con los paquetes adicionales
        pythonEnv = pkgs.python312.withPackages (ps: with ps; [
          pandas numpy matplotlib seaborn scikit-learn openpyxl xlrd
          jupyterlab pytz beautifulsoup4 selenium webdriver-manager
          yfinance pip

          # Incluye los paquetes generados con pip2nix
        ] ++ (builtins.attrValues pythonPackages));

      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv
          ];
          shellHook = ''
            echo "Entorno de Python activado."
          '';
        };
      });

}