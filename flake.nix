{
  description = "An ML based classifier to detect if an apk contains trackers or not.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
    mach-nix-src.url = "github:DavHau/mach-nix";
  };

  outputs = { self, nixpkgs, flake-utils, mach-nix-src }:
    flake-utils.lib.eachDefaultSystem (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          mach-nix = import mach-nix-src { inherit pkgs; python = "python38"; };
          requirements = builtins.readFile ./requirements.txt;
        in
        {
          # defaultPackage = self.packages.${system}.${pname};
          packages = { inherit pkgs; };
          devShell = mach-nix.mkPythonShell {
            inherit requirements;
          };
        });
}
