-- Specify Spoons which will be loaded
hspoon_list = {
    "FnMate",
    "WinWin",
}

-- appM environment keybindings. Bundle `id` is prefered, but application `name` will be ok.
hsapp_list = {
    {key = 'e', name = 'Evernote'},
    {key = 'f', name = 'Finder'},
    {key = 'i', name = 'Messages'},
    {key = 'm', name = 'MacVim'},
    {key = 'o', name = 'Todoist'},
    {key = 'p', name = 'PyCharm'},
    {key = 't', name = 'Terminal'},
    {key = 'w', id = 'WhatsApp'},
    {key = 'v', id = 'com.apple.ActivityMonitor'},
    {key = 'x', id = 'org.mozilla.firefox'},
    {key = 'y', id = 'com.apple.systempreferences'},
}

-- Modal supervisor keybinding, which can be used to temporarily disable ALL modal environments.
hsupervisor_keys = {{"cmd", "shift", "ctrl"}, "Q"}

-- Reload Hammerspoon configuration
hsreload_keys = {{"cmd", "shift", "ctrl"}, "R"}

-- Toggle help panel of this configuration.
hshelp_keys = {{"alt", "shift", "control"}, "/"}

-- aria2 RPC host address
hsaria2_host = "http://localhost:6800/jsonrpc"
-- aria2 RPC host secret
hsaria2_secret = "token"

----------------------------------------------------------------------------------------------------
-- Those keybindings below could be disabled by setting to {"", ""} or {{}, ""}

-- appM environment keybinding: Application Launcher
hsappM_keys = {"alt", "A"}

-- Lock computer's screen
hslock_keys = {"alt", "L"}

-- resizeM environment keybinding: Windows manipulation
hsresizeM_keys = {"alt", "R"}

