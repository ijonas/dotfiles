-- load defaults i.e lua_lsp
require("nvchad.configs.lspconfig").defaults()

local lspconfig = require "lspconfig"

-- Server configurations
local servers = { "html", "cssls" }
local nvlsp = require "nvchad.configs.lspconfig"

-- lsps with default config
for _, lsp in ipairs(servers) do
  lspconfig[lsp].setup {
    on_attach = nvlsp.on_attach,
    on_init = nvlsp.on_init,
    capabilities = nvlsp.capabilities,
  }
end

-- Pyright configuration
lspconfig.pyright.setup {
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

-- Solidity
lspconfig.solidity_ls.setup {
  capabilities = nvlsp.capabilities,
  on_attach = nvlsp.on_attach,
  filetypes = { "solidity" },
  root_dir = lspconfig.util.root_pattern("hardhat.config.*", ".git"),
}

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
