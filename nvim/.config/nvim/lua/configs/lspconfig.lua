-- load defaults i.e lua_lsp
require("nvchad.configs.lspconfig").defaults()

-- Server configurations
local nvlsp = require "nvchad.configs.lspconfig"

-- Define common servers with default config
local servers = {
  "html",
  "cssls",
  "ts_ls",      -- TypeScript/JavaScript
  "jsonls",     -- JSON
  "tailwindcss", -- Tailwind CSS
  "ruff",       -- Python linter/formatter
}

for _, lsp in ipairs(servers) do
  vim.lsp.config[lsp] = {
    on_attach = nvlsp.on_attach,
    on_init = nvlsp.on_init,
    capabilities = nvlsp.capabilities,
  }
  vim.lsp.enable(lsp)
end

-- Pyright configuration
vim.lsp.config.pyright = {
  on_attach = nvlsp.on_attach,
  on_init = nvlsp.on_init,
  capabilities = nvlsp.capabilities,
  settings = {
    pyright = {
      disableOrganizeImports = false,
    },
    python = {
      analysis = {
        autoImportCompletions = true,
        autoSearchPaths = true,
        diagnosticMode = "workspace",
        useLibraryCodeForTypes = true,
        typeCheckingMode = "basic",
      },
    },
  },
}
vim.lsp.enable('pyright')

-- Solidity
vim.lsp.config.solidity_ls = {
  capabilities = nvlsp.capabilities,
  on_attach = nvlsp.on_attach,
  filetypes = { "solidity" },
  root_dir = function(path)
    return vim.fs.root(path, {"hardhat.config.js", "hardhat.config.ts", ".git"})
  end,
}
vim.lsp.enable('solidity_ls')

-- Diagnostic configuration
vim.diagnostic.config {
  virtual_text = false,
  signs = true, -- Shows signs in the gutter
  underline = true, -- Underlines issues in code
  update_in_insert = false,
}

vim.o.updatetime = 300 -- Lower value means quicker hover popup

-- Show diagnostics on hover
vim.api.nvim_create_autocmd("CursorHold", {
  callback = function()
    vim.diagnostic.open_float(nil, {
      focusable = false,
      close_events = { "BufLeave", "CursorMoved", "InsertEnter", "FocusLost" },
      border = "rounded",
      source = "always",
      prefix = "",
    })
  end,
})
