{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.nodejs-18_x
    pkgs.yarn
    pkgs.postgresql
    pkgs.redis
  ];
}