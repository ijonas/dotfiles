-- ~/.config/nvim/lua/plugins/git-fugitive.lua
return {
  "tpope/vim-fugitive",
  cmd = { "Git", "G", "Gdiffsplit", "Gwrite", "Gread" }, -- Optional: lazy-load on command
  keys = {
    { "<leader>gs", "<cmd>Git<cr>", desc = "Fugitive Git status" },
    { "<leader>gb", "<cmd>Git blame<cr>", desc = "Fugitive Git blame" },
  },
}
