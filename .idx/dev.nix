{ pkgs, ... }: {
  channel = "stable-24.05";

  packages = [
    pkgs.python312Full
    pkgs.python312Packages.pip
    pkgs.nodejs_20
    pkgs.nodePackages.nodemon
  ];

  env = { };

  idx = {
    extensions = [
      # "vscodevim.vim"
      "ms-python.debugpy"
      "ms-python.python"
    ];

    previews = {
      enable = true;
      previews = {
        web = {
          command = [ "python" "-m" "http.server" "$PORT" ];
          manager = "web";
          env = { };
        };
      };
    };
  };

  # ✅ These go at the root level
  idx.workspace.onCreate  = {
    install-python-dependencies = ''
      pip install -r requirements.txt
      pip install httpstan
      '';
  };

  idx.workspace.onStart = {
    # Example: watch-backend = "npm run watch-backend";
  };
}
