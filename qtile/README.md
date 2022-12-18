Installing From Source
Python interpreters
We aim to always support the last three versions of CPython, the reference Python interpreter. We usually support the latest stable version of PyPy as well. You can check the versions and interpreters we currently run our test suite against in our tox configuration file.

There are not many differences between versions aside from Python features you may or may not be able to use in your config. PyPy should be faster at runtime than any corresponding CPython version under most circumstances, especially for bits of Python code that are run many times. CPython should start up faster than PyPy and has better compatibility for external libraries.

Core Dependencies
Here are Qtile's core runtime dependencies and the package names that provide them in Ubuntu. Note that Qtile can run with one of two backends -- X11 and Wayland -- so only the dependencies of one of these is required.
```
git clone https://github.com/elparaguayo/qtile-extras.git ##### FOR BAR DECORATIONS
sudo apt install xserver-xorg
sudo apt install python3 
sudo apt install python3-pip
sudo apt install psutil ### this is for bar to display temp
pip install python3-xcffib
pip install python3-cffi
pip install python3-cairocffi
pip install --no-cache-dir cairocffi
```
```
# With the dependencies in place, you can now install the stable version of qtile from PyPI:
pip install qtile
```
```
# Or install qtile-git with:
git clone https://github.com/qtile/qtile.git
cd qtile
pip install .

```
Dependency

Ubuntu Package

Needed for

Core Dependencies

CFFI

python3-cffi

Bars and popups

cairocffi

python3-cairocffi

Drawing on bars and popups (if using X11 install xcffib BEFORE installing cairocffi, see below)

libpangocairo

libpangocairo-1.0-0

Writing on bars and popups

dbus-next

--

Sending notifications with dbus (optional).

X11

X server

xserver-xorg

X11 backends

xcffib

python3-xcffib

required for X11 backend

Wayland

wlroots

libwlroots-dev

Wayland backend (see below)

pywlroots

--

python bindings for the wlroots library

pywayland

--

python bindings for the wayland library

python-xkbcommon

--

required for wayland backeds

cairocffi
Qtile uses cairocffi for drawing on status bars and popup windows. Under X11, cairocffi requires XCB support via xcffib, which you should be sure to have installed before installing cairocffi; otherwise, the needed cairo-xcb bindings will not be built. Once you've got the dependencies installed, you can use the latest version on PyPI:

pip install --no-cache-dir cairocffi
Qtile
With the dependencies in place, you can now install the stable version of qtile from PyPI:

pip install qtile
Or install qtile-git with:

git clone https://github.com/qtile/qtile.git
cd qtile
pip install .
As long as the necessary libraries are in place, this can be done at any point, however, it is recommended that you first install xcffib to ensure the cairo-xcb bindings are built (X11 only) (see above).

Starting Qtile
There are several ways to start Qtile. The most common way is via an entry in your X session manager's menu. The default Qtile behavior can be invoked by creating a qtile.desktop file in /usr/share/xsessions.

A second way to start Qtile is a custom X session. This way allows you to invoke Qtile with custom arguments, and also allows you to do any setup you want (e.g. special keyboard bindings like mapping caps lock to control, setting your desktop background, etc.) before Qtile starts. If you're using an X session manager, you still may need to create a custom.desktop file similar to the qtile.desktop file above, but with Exec=/etc/X11/xsession. Then, create your own ~/.xsession. There are several examples of user defined xsession s in the qtile-examples repository.

If there is no display manager such as SDDM, LightDM or other and there is need to start Qtile directly from ~/.xinitrc do that by adding exec qtile start at the end.

In very special cases, ex. Qtile crashing during session, then suggestion would be to start through a loop to save running applications:

while true; do
    qtile
done
Finally, if you're a gnome user, you can start integrate Qtile into Gnome's session manager and use gnome as usual.

Running from systemd
Running Inside Gnome
Wayland
Qtile can be run as a Wayland compositor rather than an X11 window manager. For this, Qtile uses wlroots, a compositor library which is undergoing fast development. This means we can only support the latest release. Be aware that some distributions package outdated versions of wlroots. More up-to-date distributions such as Arch Linux may also package pywayland, pywlroots and python-xkbcommon.

With the Wayland dependencies in place, Qtile can be run either from a TTY, or within an existing X11 or Wayland session where it will run inside a nested window:

qtile start -b wayland
