# Repository Guidelines

## Purpose

This repository manages personal dotfiles with GNU Stow. Each package mirrors
the path it owns below `$HOME`; for example, `nvim/.config/nvim/init.lua` is
linked to `$HOME/.config/nvim/init.lua`.

## Repository layout

- Stow packages live in top-level directories named for the package.
- `bin/install` is the cross-platform bootstrap and installation entry point.
- `bin/tmux-cb` is a personal tmux session helper, not a stow package.
- `path`, `pyenv`, `nvm`, `golang`, and `julia` are shell fragments sourced
  directly from `zsh/.zshrc` and currently assume the checkout is
  `$HOME/dotfiles`.
- `install_neovim_on_linux.sh` and `post_nvchad_install.sh` are legacy/manual
  Neovim helpers. Do not make the main installer depend on them.
- Configuration under `claude`, `claude-code`, and `opencode` may contain
  application-managed data; check diffs carefully and never add credentials or
  machine-local caches.

## Package matrix

Shared packages, installed on both Linux and macOS:

- `zsh`
- `tmux`
- `nvim`
- `claude`
- `claude-code`
- `opencode`

macOS-only packages:

- `aerospace`
- `sketchybar`

Keep host-specific packages out of the shared package list. New stow packages
must contain files in their final layout relative to `$HOME`.

When adding or removing a package, update all three of:

1. The package variables in `bin/install`.
2. The package tables in `README.md`.
3. The package matrix in this file.

## Installer

`bin/install` is the supported entry point for both an existing checkout and a
remote bootstrap. It must:

- remain compatible with POSIX `sh`;
- support Linux and macOS explicitly and reject unknown operating systems;
- install or verify `git`, `stow`, `zsh`, and `curl` before use;
- bootstrap Homebrew on macOS when it is not already installed;
- clone the repository to `$DOTFILES_DIR` (default: `$HOME/dotfiles`) when run
  outside a checkout;
- install Oh My Zsh unattended without replacing the repository's `.zshrc`;
- run GNU Stow with the repository root as its source and `$HOME` as its target;
- never stow `aerospace` or `sketchybar` on Linux;
- stop on stow conflicts rather than adopting or deleting user files.

Linux dependency installation currently supports `apt`, `dnf`, `pacman`, and
`zypper`. macOS dependency installation uses Homebrew and bootstraps it when
necessary. Keep dependency installation idempotent and suitable for both root
and `sudo`-based Linux environments.

Keep the clone URL and one-line bootstrap command in `README.md` synchronized
with the installer. The SSH clone URL assumes the machine already has GitHub
SSH credentials; document the HTTPS override for machines that do not.
If the shell fragments stop assuming `$HOME/dotfiles`, update the corresponding
warning in `README.md`.

## Editing and validation

- Preserve user-specific configuration unless the task explicitly changes it.
- Do not commit secrets, generated caches, or machine-local state.
- Run `sh -n bin/install` after changing the installer.
- Run `shellcheck bin/install` when ShellCheck is available.
- Exercise non-mutating paths such as `bin/install --help` during validation.
- Review `git diff --check` before committing.
