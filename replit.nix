{ pkgs }: {
  deps = [
    pkgs.python310   # Change this to the version you want, e.g., pkgs.python311 for Python 3.11
    pkgs.python310Packages.pip
  ];
}
