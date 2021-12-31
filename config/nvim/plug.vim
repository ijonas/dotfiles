if has("nvim")
  let g:plug_home = stdpath('data') . '/plugged'
endif

call plug#begin()

" Git + Github
Plug 'tpope/vim-fugitive'
Plug 'tpope/vim-rhubarb'

" Code commenting in/out
Plug 'tpope/vim-commentary'

" fuzzy lookup / better ctrlp
Plug 'junegunn/fzf'
Plug 'junegunn/fzf.vim'

" Solidity
Plug 'tomlion/vim-solidity'

" React/Typescript
Plug 'pangloss/vim-javascript'
Plug 'leafgarland/typescript-vim'
Plug 'peitalin/vim-jsx-typescript'
Plug 'styled-components/vim-styled-components', { 'branch': 'main' }
Plug 'jparise/vim-graphql'

" Search in project
Plug 'mileszs/ack.vim'

if has("nvim")
  Plug 'nvim-lualine/lualine.nvim'
  Plug 'kristijanhusak/defx-git'
  Plug 'kristijanhusak/defx-icons'
  Plug 'Shougo/defx.nvim', { 'do': ':UpdateRemotePlugins' }
  Plug 'neovim/nvim-lspconfig'
  " Plug 'tami5/lspsaga.nvim', { 'branch': 'nvim51' }
  " Plug 'folke/lsp-colors.nvim'
  Plug 'L3MON4D3/LuaSnip'

  Plug 'neoclide/coc.nvim', {'branch': 'release'}

  Plug 'nvim-treesitter/nvim-treesitter', { 'do': ':TSUpdate' }
  Plug 'kyazdani42/nvim-web-devicons'
  Plug 'onsails/lspkind-nvim'
  Plug 'nvim-lua/popup.nvim'
  Plug 'nvim-lua/plenary.nvim'
  Plug 'nvim-telescope/telescope.nvim'
  Plug 'windwp/nvim-autopairs'
  Plug 'simrat39/rust-tools.nvim'
  Plug 'rust-lang/rust.vim'
endif


call plug#end()

