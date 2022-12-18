# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, KeyChord, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401
from libqtile.backend.x11 import window
from libqtile.confreader import ConfigError
from libqtile.widget import base

### INSTALL DECORATIONS FROM HERE //// INSTALL AS SUDO git clone  https://github.com/elparaguayo/qtile-extras.git
### cd qtile-extras ####
#### sudo python setup.py install ####
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration

XEMBED_PROTOCOL_VERSION = 0



#=-/ Created variables /-=#
mod = "mod4"
mod1 = "alt"
mod2 = "control" 
myTerm = "kitty -e fish" 
# myBrowser = "chromium"
# logoutMenu = "kitty -e herbst-logout.sh"

#=-/ Keybindings /-=#
keys = [
         #=-/ Main sys control /-=#
        Key([mod], "z", lazy.next_layout(), desc='Toggle through layouts'),
        Key([mod], "q", lazy.window.kill(), desc='Kill active window'),
        Key([mod, "shift"], "r", lazy.restart(), desc='Restart Qtile'),
        #=-/ Terminals /-=#
        Key([mod], "Return", lazy.spawn("kitty -e fish"), desc='Run Launcher'),
        Key([mod], "r", lazy.spawn("feh --randomize --bg-fill /home/dmne/Pictures/background")),
        Key([mod], "space", lazy.spawn("rofi -show drun -show-icons -modi drun,run")),
        Key([mod2], "space", lazy.spawn("rofi -show calc")),
        Key([mod], "x", lazy.spawn("/usr/bin/clearine ")),
        Key([mod], "t", lazy.spawn("pcmanfm")),
        Key([mod], "e", lazy.spawn("lapce")),
        Key([mod], "o", lazy.spawn("obsidian")),
        Key([mod], "d", lazy.spawn("telegram-desktop")),
        Key([mod, "shift"], "t", lazy.spawn("kitty -e ranger"), desc='Ranger'),
        Key([mod,"control"], "t", lazy.spawn("kitty -e nnn"), desc='Ranger'),
        #=-/ Browsers /-=#
        # Key([mod], "w", lazy.spawn("google-chrome-stable"), desc='chromium-browser'),
        Key([mod], "w", lazy.spawn("firefox"), desc='Firefox'),

        # Emacs programs launched using the key chord CTRL+e followed by 'key'                       
        KeyChord([mod],"i", [
            Key([], "e",
                lazy.spawn("code"),
                desc='vscode'
                ),
            Key([], "return",
                lazy.spawn("kitty -e fish"),
                desc='Terminal'
                ),
            Key([], "w",
                lazy.spawn("brave-browser"),
                desc='Brave'
                ),
            Key([], "y",
                lazy.spawn(" opera"),
                desc='Opera'
                ),
            Key([], "a",
                lazy.spawn("kitty -e mocp"),
                desc='MOCP Music Player')
        ]),
       

         #=-/ Window manipulation /-=#
        #  Key([mod], "j", lazy.layout.down(), desc='Move focus down in current stack pane'),
        #  Key([mod], "k", lazy.layout.up(), desc='Move focus up in current stack pane'),
         Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
         Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
         Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
         Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
   
         Key([mod], "h", lazy.layout.shrink(), lazy.layout.decrease_nmaster(), desc='Shrink window (MonadTall), decrease number in master pane (Tile)'),
         Key([mod], "l", lazy.layout.grow(), lazy.layout.increase_nmaster(), desc='Expand window (MonadTall), increase number in master pane (Tile)'),
         # Key([mod,"shift"], "n", lazy.layout.normalize(), desc='normalize window size ratios'),
         # Key([mod,"shift"], "m", lazy.layout.maximize(), desc='toggle window between minimum and maximum sizes'),
         Key([mod], "f", lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
         
         #=-/ Stack and master manipulation /-=#
         Key([mod, "shift"], "z", lazy.layout.rotate(), lazy.layout.flip(), desc='flip master and stack'),
         Key([mod], "Tab", lazy.layout.next(), desc='Switch window focus to other pane(s) of stack'),
         
         #=-/ Multimedia keys /-=#
         # Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -5%")),
         # Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +5%")),
         # Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

        ##### WIREPLUMBER VOLUME CONTROLS
         Key([], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-")),
         Key([], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+")),
         Key([], "XF86AudioMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")),
         
         
        # INCREASE/DECREASE BRIGHTNESS
        Key([], "XF86MonBrightnessUp", lazy.spawn("light -A 10")),
        Key([], "XF86MonBrightnessDown", lazy.spawn("light -U 10")),
    
        # INCREASE/DECREASE/MUTE VOLUME
        # Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
        # Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
        # Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),
    
        Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
        Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
        Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
        Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),

         #=-/ Scratchpads /-=#
         Key([mod2], "1", lazy.group['scratchpad'].dropdown_toggle('term')),
         Key([mod2], "2", lazy.group['manager'].dropdown_toggle('ranger')),
         Key([mod2], "3", lazy.group['pulse'].dropdown_toggle('mixer')),
         Key([mod2], "4", lazy.group['tel'].dropdown_toggle('telegram')),
         Key([mod2], "9", lazy.group['music'].dropdown_toggle('tunes')),
         Key([mod2], "0", lazy.group['logout'].dropdown_toggle('exitMenu')),
]

#=-/ Window groups settings /-=#
groups = [Group(" 1 ", layout='monadtall'),
          Group(" 2 ", layout='monadtall'),
          Group(" 3 ", layout='monadtall'),
          Group(" 4 ", layout='monadtall'),
          Group(" 5 ", layout='monadtall'),
          Group(" 6 ", layout='monadtall'),
          Group(" 7 ", layout='monadtall'),
          Group(" 8 ", layout='monadtall'),
          Group(" 9 ", layout='monadtall'),
          #=-/ Scratchpad groups /-=#
          ScratchPad("music",[DropDown("tunes", "kitty -e mocp", x=0.05, y=0.02, width=0.90, height=0.6, on_focus_lost_hide=False)]),
          # ScratchPad("pulse",[DropDown("mixer", "kitty -e pulsemixer", x=0.33, y=0.02, width=0.35, height=0.95, on_focus_lost_hide=False)]),
          ScratchPad("logout",[DropDown("exitMenu", "/usr/bin/clearine ", x=0.40, y=0.30, width=0.20, height=0.20, on_focus_lost_hide=False)]),
          ScratchPad("tel",[DropDown("telegram", "telegram-desktop", x=0.12, y=0.02, width=0.75, height=0.6, on_focus_lost_hide=False)]),
          ScratchPad("scratchpad",[DropDown("term", "kitty -e fish", x=0.12, y=0.02, width=0.75, height=0.6, on_focus_lost_hide=False)]),
          ScratchPad("manager",[DropDown("ranger", "kitty -e ranger", x=0.12, y=0.02, width=0.75, height=0.6, on_focus_lost_hide=False)]),
          ScratchPad("pulse",[DropDown("mixer", "kitty -e pulsemixer", x=0.12, y=0.02, width=0.75, height=0.6, on_focus_lost_hide=False)]),
]

from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder("mod4")

#=-/ Layout settings /-=#
layout_theme = {"border_width": 3,
                "margin": 13,
                "border_focus": "3f92f7",
                "border_normal": "fdb302"
                }

layouts = [
    layout.MonadThreeCol(**layout_theme)
    # layout.MonadTall(**layout_theme),
    # layout.MonadWide(**layout_theme),
    #layout.Columns(**layout_theme),
    #layout.Matrix(**layout_theme),
    # layout.Zoomy(**layout_theme),
    #layout.Stack(num_stacks=2),
    #layout.Tile(shift_windows=True, **layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Max(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Floating(**layout_theme)
    # layout.TreeTab(
    #      font = "Ubuntu",
    #      fontsize = 10,
    #      sections = ["FIRST", "SECOND", "THIRD", "FOURTH"],
    #      section_fontsize = 10,
    #      border_width = 2,
    #      bg_color = "1c1f24",
    #      active_bg = "c678dd",
    #      active_fg = "000000",
    #      inactive_bg = "a9a1e1",
    #      inactive_fg = "1c1f24",
    #      padding_left = 0,
    #      padding_x = 0,
    #      padding_y = 5,
    #      section_top = 10,
    #      section_bottom = 20,
    #      level_shift = 8,
    #      vspace = 3,
    #      panel_width = 200
    #      )
]

#=-/ System colors /-=#
colors = [["#282c34", "#282c34"],
          ["#1c1f24", "#1c1f24"],
          ["#dfdfdf", "#dfdfdf"],
          ["#ff6c6b", "#ff6c6b"],
          ["#98be65", "#98be65"],
          ["#da8548", "#da8548"],
          ["#51afef", "#51afef"],
          ["#c678dd", "#c678dd"],
          ["#46d9ff", "#46d9ff"],
          ["#a9a1e1", "#a9a1e1"]]

#=-/ Default settings for widgets /-=#
widget_defaults = dict(
    font="FiraCode Bold",  ### NERD FONT https://www.nerdfonts.com/font-downloads
    fontsize = 10,
    padding = 2,
    # background="#1f233588"
    background="#000000"
)
extension_defaults = widget_defaults.copy()

#=-/ Widgets /-=#
def init_widgets_list():
    widgets_list = [
                    # widget.CurrentLayout(),
                    widget.GroupBox(
                         # disable_drag=True,
                         active="#05ff00",
                         inactive="#3f92f7",
                         rounded=True,
                         highlight_method='line',
                         highlight_text_color='red',
                         borderwidth=3,
                         highlight_color="#3f92f7",
                        #  this_current_screen_boarder="#ffffff",
                        #  this_screen_boarder="#000000",
                        #  other_current_screen_boarder="#3b6699",
                        #  highlight_color="#383838",
                         # background="#1f233588",
                         background="#000000",
                        #  foreground="#fdb302",
                        #  background_inactive='#ffffff',
                        #  background_active='#ffffff',
                         padding = 0,
                         decorations=[
                           BorderDecoration(
                               colour = "#3f92f7",
                               border_width = [0, 0, 2, 0],
                               padding_x = 0,
                               padding_y = None
                           )
                    ],
                    ),            
                    widget.WindowName(
                       foreground="#05ff00",
                       background="#000000",
                       # background="#1f2335",
                       font="Ubuntu ",
                       fontsize=8,
                       padding = 0,
                         decorations=[
                           BorderDecoration(
                            #    colour = colors[9],
                               colour = "#05ff00",
                               border_width = [0, 0, 2, 0],
                               padding_x = 0,
                               padding_y = None
                           )
                    ],
                    ),   
                    

                    # widget.Chord(
                    #   chords_colors={
                    #     "launch": ("#ff0000", "#ffffff"),
                    # },
                    #    name_transform=lambda name: name.upper()
                    # ),
             
              
            #       widget.GenPollText(
            #            name = "ytsubs",
            #            fmt = " " " {} ", update_interval = 3600,
            #            foreground = colors[1], background = colors[7],
            #            func = lambda: subprocess.check_output("/home/jake/.local/scripts/ytsubs.sh").decode("utf-8"),
            #            padding = 0
            #       ),
                    widget.Moc(
                         background="#000000",
                         foreground="#51afef",
                         font="Terminus ",
                         fontsize=7,
                         update_interval=1,
                         padding = 0,
                         decorations=[
                           BorderDecoration(
                            #    colour = colors[9],
                               colour = "#51afef",
                               border_width = [0, 0, 2, 0],
                               padding_x = 0,
                               padding_y = None
                           )
                    ],
                    ),   
                    
            #         widget.Sep(
            #              background="#1f2335",
            #              foreground="#1F2335",
            #    #         linewidth="0",
            #              padding=10
            #         ),
                    widget.CryptoTicker(
                         crypto="BTC",
                         # foreground="#46d9ff",
                         foreground="#E5E661",
                         background="#000000",
                         # background="#1f2335",
                         currency = "USD",
                         symbol = "$",
                         font = "FiraCode Bold",
                         fontsize ="9",
                         padding = 0,
                         decorations=[
                           BorderDecoration(
                            #    colour = colors[9],
                               colour = "#E5E661",
                               border_width = [0, 0, 2, 0],
                               padding_x = 0,
                               padding_y = None
                           )
                    ],
                    ),
                    widget.Sep(
                        background="#000000",
                        foreground="#000000",
               #        linewidth="0",
                        padding=1,
                        decorations=[
                           BorderDecoration(
                            #    colour = colors[9],
                               colour = "#46d9ff",
                               border_width = [0, 0, 2, 0],
                               padding_x = 0,
                               padding_y = None,
                           )
                    ],
                    ),  
                       

                    

                    widget.Sep(
                        background="#000000",
                        foreground="#000000",
               #        linewidth="0",
                        padding=8,
                        decorations=[
                           BorderDecoration(
                            #    colour = colors[9],
                               colour = "#ff0011",
                               border_width = [0, 0, 0, 0],
                               padding_x = 0,
                               padding_y = None,
                           )
                    ],
                    ),  
                    

                    widget.Net(
                        font="FiraCode Bold",
                        fontsize=10,
                        interface="wlp2s0",
                        format = '{down} ↓↑ {up}',
                        foreground="#C74CFF",
                        background="#000000",
                        padding = 0,
                        decorations=[
                           BorderDecoration(
                            #    colour = colors[9],
                               colour = "#C74CFF",
                               border_width = [0, 0, 2, 0],
                               padding_x = 0,
                               padding_y = None,
                           )
                    ],
                    ),   
                       
                    widget.Sep(
                        background="#000000",
                        foreground="#000000",
               #        linewidth="0",
                        padding=1,
                        decorations=[
                           BorderDecoration(
                            #    colour = colors[9],
                               colour = "#ff0011",
                               border_width = [0, 0, 0, 0],
                               padding_x = 0,
                               padding_y = None,
                           )
                    ],
                    ),  
                    widget.Sep(
                        background="#000000",
                        foreground="#000000",
               #        linewidth="0",
                        padding=8,
                        decorations=[
                           BorderDecoration(
                            #    colour = colors[9],
                               colour = "#da8548",
                               border_width = [0, 0, 0, 0],
                               padding_x = 0,
                               padding_y = None,
                           )
                    ],
                    ),     

                    widget.CPU(
                       #format="CPU {freq_current}GHz {load_percent}%",
                       font="FiraCode Bold",
                       fontsize=10,
                       foreground="#ee8617",
                       background="#000000",
                       # background="#1f2335",
                       threshold = 90,
                       padding = 0,
                       decorations=[
                           BorderDecoration(
                            #    colour = colors[9],
                               colour = "#ee8617",
                               border_width = [0, 0, 2, 0],
                               padding_x = 0,
                               padding_y = None,
                           )
                    ],
                    ), 
                    widget.Sep(
                        background="#000000",
                        foreground="#000000",
               #        linewidth="0",
                        padding=8,
                        decorations=[
                           BorderDecoration(
                            #    colour = colors[9],
                               colour = "#da8548",
                               border_width = [0, 0, 0, 0],
                               padding_x = 0,
                               padding_y = None,
                           )
                    ],
                    ),        
                    


                    # widget.Memory(
                    #     background="#1f2335",
                    #     foreground="#fdb302",
                    #     padding=10
                    #  #  font=
                    # # fontsize=9,
                    # ),  

                    widget.Memory(
                        font="FiraCode Bold",
                        fontsize=10,
                        foreground = "#46d9ff",
                        background = "#000000",
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                        fmt = 'Mem: {}',
                        padding = 0,
                        decorations=[
                           BorderDecoration(
                               colour = "#46d9ff",
                               border_width = [0, 0, 2, 0],
                               padding_x = 0,
                               padding_y = None,
                           )
                    ],
                    ),             
                    widget.Sep(
                        background="#000000",
                        foreground="#000000",
                    #   linewidth="0",
                        padding=8
                    ),

                    # widget.DF(
                    #     foreground="#ffffff",
                    #     background="#1f2335",
                    #     padding=10


                    # ),

                    # widget.ThermalSensor(
                    #     foreground = "#f3f50c",
                    #     foreground_alert = "#FF0000",
                    #     background = "#1f2335",
                    #     metric = True,
                    #     padding = 3,
                    #     threshold = 80
                    # ),

                    widget.ThermalSensor(
                        font="FiraCode Bold",
                        fontsize=10,
                        foreground = "#05ff00",
                        background = "#000000",
                        threshold = 80,
                        fmt = 'Temp: {}',
                        padding = 0,
                        decorations=[
                           BorderDecoration(
                               colour = "#05ff00",
                               border_width = [0, 0, 2, 0],
                               padding_x = 0,
                               padding_y = None
                            )
                       ],
                    ),
                    widget.Sep(
                        background="#000000",
                        foreground="#000000",
                    #   linewidth="0",
                        padding=8
                    ),
         
                    # widget.Clock(
                    #    foreground = "#c1c1c1", 
                    #    background = "#1f2335",
                    #    format = "%a %b %d  %H:%M",
                    #    padding = 5
                    # ),
                    widget.Clock(
                        font="FiraCode Bold",
                        fontsize=10,
                        foreground = "#c1c1c1",
                        background = "#000000",
                        format = "%a %b %d  %H:%M",
                        decorations=[
                           BorderDecoration(
                               colour = "#c1c1c1",
                               border_width = [0, 0, 2, 0],
                               padding_x = 0,
                               padding_y = None,
                           )
                    ],

                    ),
                    widget.Sep(
                        background="#000000",
                        foreground="#000000",
                    #   linewidth="0",
                        padding=8
                    ),
         
                    widget.Systray(
                        background="#000000",
                        # background="#737C85",
                        # background="#1f2335",
                        padding=0,
                        decorations=[
                           BorderDecoration(
                               colour = "#ffffff",
                               border_width = [0, 0, 0, 0],
                               padding_x = 0,
                               padding_y = None
                           )
                    ],

                    ),
                                       
          
              ]
                   
    return widgets_list

#=-/ Set bar to screen /-=#
def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

#=-/ Set bar height and opacity, also set wallpaper /-=#
def init_screens():
    return [Screen(top=bar.Bar(
        widgets=init_widgets_screen1(), 
        # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
        # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        # margin=[0, 26, 5, 10], ### FOR BROKEN LAPTOP
        margin=[0, 0, 0, 0],
        background='#000000',
        # background='#1f2335',
        opacity=1.0, 
        size=21))]
        # wallpaper='~/.config/herbstluftwm/wallpaper/teal/city.jpg',
        # wallpaper_mode='fill')]

#=-/ Initiate functions for screens and widgets /-=#
if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()

#=-/ Mouse settings /-=#
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

#=-/ Cursor rules /-=#
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True

#=-/ Window rules /-=#

floating_layout = layout.Floating(
    border_width=3,
    border_focus="#3f92f7",
    border_normal="#EC8011",
    float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
    Match(wm_class="confirmreset"),  # gitk
    Match(wm_class="makebranch"),  # gitk
    Match(wm_class="maketag"),  # gitk
    Match(wm_class="Galculator"),  # gitk Galculator
    Match(wm_class="galculator"),  # gitk Galculator
    Match(wm_class="blueman-manager"),  # gitk
    Match(wm_class="ssh-askpass"),  # ssh-askpass
    Match(wm_class="Gpick"),  # ssh-askpass
    Match(wm_class="gpick"),  # ssh-askpass
    Match(wm_class="browser-window"),  # ssh-askpass
    Match(wm_class="Skype"),  # ssh-askpass
    # Match(wm_class="google-chrome"),  # ssh-askpass
    Match(wm_class="pavucontrol"),  # ssh-askpass
    Match(wm_class="Imager"),  # ssh-askpass
    Match(wm_class="SpeedCrunch"),  # ssh-askpass
    Match(wm_class="system-config-printer"),  # ssh-askpass
    Match(wm_class="crx_dmkamcknogkgcdfhhbddcghachkejeap"),  # ssh-askpass
    Match(wm_class="crx_nkbihfbeogaeaoehlefnkodbefgpgknn"),  # ssh-askpass
    Match(wm_class="crx_jiidiaalihmmhddjgbnbgdfflelocpak"),  # ssh-askpass
    Match(wm_class="crx_mfgccjchihfkkindfppnaooecgfneiii"),
    Match(wm_class="Scanner"),  # ssh-askpass
    Match(wm_class="InfinityWallet"),  # ssh-askpass
    Match(title="branchdialog"),  # gitk
    Match(title="pinentry"),  # GPG key password entry

])


# auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

