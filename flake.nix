{
  description = "Entorno de desarrollo Data Scrapper datos financieros y económicos";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };


  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system;
                                config.allowUnfree = true;
                              };
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [

            # Instala python 3.12
            python312
            (python312.withPackages (ps: with ps; [
              # Paquetes normales de Python
              pandas numpy matplotlib seaborn scikit-learn openpyxl
              xlrd jupyterlab pytz
              beautifulsoup4

            ]))
          ];
        shellHook = ''
          echo "Entorno de Python activado."
        '';

        
        };
      });

}