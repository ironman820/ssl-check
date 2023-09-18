{
  description = "Flake with python 3.10";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-23.05";
    flake-parts.url = "github:hercules-ci/flake-parts";
    systems.url = "github:nix-systems/default";
    # process-compose-flake.url = "github:Platonic-Systems/process-compose-flake";
  };

  outputs = inputs: inputs.flake-parts.lib.mkFlake { inherit inputs; } {
    systems = import inputs.systems;
    perSystem = {lib, pkgs, self', ... }: let
      python-packages = ps: with ps; [
        requests
      ];
      python = pkgs.python310.withPackages python-packages;
    in {
      devShells.default = pkgs.mkShell {
        name = "python-dev-shell";
        nativeBuildInputs = [
          python
        ];
        shellHook = ''
          rm .python
          ln -sf ${python} .python
          echo "Welcome to the devShell! Python is installed at ./.python"
        '';
      };
    };
  };
}