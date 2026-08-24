# dotfiles

Personal configuration for macOS and Linux, managed with
[GNU Stow](https://www.gnu.org/software/stow/). Each package mirrors its final
location below `$HOME`; for example, `nvim/.config/nvim/init.lua` is linked to
`~/.config/nvim/init.lua`.

## Quick install

On a machine with GitHub SSH access:

```sh
curl -fsSL https://raw.githubusercontent.com/ijonas/dotfiles/main/bin/install | sh
```

The installer will:

1. Detect Linux or macOS.
2. Install Git, GNU Stow, Zsh, and curl when they are missing.
3. Clone this repository to `~/dotfiles`.
4. Stow the packages appropriate for the operating system into `$HOME`.
5. Install Oh My Zsh without replacing the managed `.zshrc`.

On macOS, Homebrew is bootstrapped if necessary. On Linux, dependency
installation supports `apt`, `dnf`, `pacman`, and `zypper` and may prompt for
`sudo` access.

To clone over HTTPS instead of SSH:

```sh
curl -fsSL https://raw.githubusercontent.com/ijonas/dotfiles/main/bin/install | \
  DOTFILES_REPO_URL=https://github.com/ijonas/dotfiles.git sh
```

To install from an existing checkout:

```sh
bin/install
```

The installer can be configured with:

| Option | Purpose |
| --- | --- |
| `--no-oh-my-zsh` | Skip the Oh My Zsh installation |
| `--skip-PACKAGE` | Skip a stow package; repeat for multiple packages |
| `DOTFILES_DIR=/path` | Change the clone destination from `~/dotfiles` |
| `DOTFILES_REPO_URL=url` | Override the SSH clone URL |
| `INSTALL_OH_MY_ZSH=0` | Skip Oh My Zsh through an environment variable |

For example, to keep existing Neovim and OpenCode configurations when running
from an existing checkout:

```sh
bin/install --skip-nvim --skip-opencode
```

To skip those packages during a remote bootstrap, pass the options after
`sh -s --`:

```sh
curl -fsSL https://raw.githubusercontent.com/ijonas/dotfiles/main/bin/install | \
  sh -s -- --skip-nvim --skip-opencode
```

Some shell fragments currently refer directly to `~/dotfiles`, so the default
clone destination is recommended. GNU Stow stops on conflicts and leaves
existing files untouched rather than adopting or overwriting them.

## Packages

These packages are installed on both Linux and macOS:

| Package | Destination | Contents |
| --- | --- | --- |
| `zsh` | `~/.zshrc`, `~/.zprofile`, `~/.aliases` | Zsh, Oh My Zsh, paths, history, and aliases |
| `tmux` | `~/.tmux.conf` | tmux configuration |
| `nvim` | `~/.config/nvim` | Neovim/NvChad configuration and plugins |
| `claude` | `~/.claude` | Claude Code settings, hooks, and voice utilities |
| `claude-code` | `~/.config/claude-code` | Claude Code application settings |
| `opencode` | `~/.config/opencode` | OpenCode settings, agents, and commands |

These packages are installed only on macOS:

| Package | Destination | Contents |
| --- | --- | --- |
| `aerospace` | `~/.aerospace.toml` | Aerospace window-manager configuration |
| `sketchybar` | `~/.config/sketchybar` | SketchyBar configuration and plugins |

Files such as `path`, `pyenv`, `nvm`, `golang`, and `julia` live at the
repository root and are sourced by `.zshrc`; they are not separate stow
packages. The standalone Neovim setup scripts are retained for manual use.

## Optional development tools

The Neovim configuration may use these global npm language tools:

```sh
npm install -g eslint
npm install -g diagnostic-languageserver
npm install -g typescript-language-server
```

## Updating

Pull the latest changes and rerun the installer. It uses `stow --restow`, so
existing managed links are refreshed safely:

```sh
cd ~/dotfiles
git pull
bin/install
```
