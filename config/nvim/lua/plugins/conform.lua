-- ~/.config/nvim/lua/plugins/conform.lua
return {
  "stevearc/conform.nvim",
  opts = {
    formatters_by_ft = {
      python = { "ruff_format" }, -- you can add "isort" too if desired
    },
    formatters = {
      ruff_format = {
        command = "ruff",
        args = { "format", "-" },
        stdin = true,
      },
    },
  },
}
