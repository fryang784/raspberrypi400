" 
" .vimrc_local - Custom setup for vim
" 
" Copy saved for replacing .vimrc installed after each update_physrpi
" 06May22  Created by Richard Yang
" 06May22  Edited based on .vimrc by Everett Lipman
"

:se tabstop=4 ic smd smartcase nohlsearch
:map K !}fmt -w 60
:map V !{fmt -w 60
:se shell=/bin/bash
:se fileformats=unix
:se background=dark
:se viminfo=
:se noloadplugins
if &t_Co > 2
   :syntax on
endif
if has("gui_running")
   :se ruler
   :se guifont=Monospace\ 16
   :highlight Normal guibg=black
   :highlight Normal guifg=green2
   :highlight Cursor guibg=yellow3
   :let &guicursor=substitute(&guicursor,"$",",a:blinkon0","")
   :se lines=41
   :syntax on
endif

" =============================================================================
" THE FOLLOWING SECTION WAS ADDED BY RICHARD YANG
" =============================================================================
 
" Load indentation rules and plugin according to the deteted filetype.
filetype plugin indent on

" Show (partial) command in status line.
set showcmd

" Automatically copy and cut to clipboard
set clipboard=unnamedplus

" Enable mouse usage (all modes).
" set mouse=a

" Add numbers to each line on the left-hand side.
" set number

" =============================================================================
" Keyboard mapping
" =============================================================================

" Map 'jj' in insert mode to <Esc>.
inoremap jj <Esc>

" '='*20 line break. 
inoremap \=20 ====================

" '-'*20 line break.
inoremap \-20 --------------------

" Text block for 'Problem Description'.
inoremap \pd ====================<Enter>Problem Description:<Enter><Enter>====================<Up>

" Text block for 'Begin Program description below'.
inoremap \pb -------------------<Enter>Begin description of the program below:<Enter><Enter>--------------------<Enter>End of program description.<Up><Up>

" Line marker for End of solution.
inoremap \end ====================<Enter>End of solution.

" Python text block for section marker.
inoremap \#%%% #%%============================================================================<Enter>#<Enter>#==============================================================================<Up>

" Python line break for section marker.
inoremap \#%% #%%============================================================================

" Python ## line break.
inoremap \## ###############################################################################

