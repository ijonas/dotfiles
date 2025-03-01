#! /bin/sh
curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux64.tar.gz
sudo rm -rf /opt/nvim
sudo tar -C /opt -xzf nvim-linux64.tar.gz
sudo apt install ripgrep
git clone https://github.com/NvChad/NvChad ~/.config/nvim --depth 1 && nvim

