# coding: utf8
import argparse
import textwrap
import pygame as pg
from pygame.colordict import THECOLORS as COLORS
import numpy as np

description = 'Welcome to the RocketWorld.\n\
------------------------------------------------------------------------------------\n\
This is a small demonstrator for an evolutionary algorithm.\n\
A population of rockets is evolving towards starting and landing safely.\n\
Have fun!\n\
------------------------------------------------------------------------------------\n'
authors = '------------------------------------------------------------------------------------\n\
Authors:\n      Maximilian Burger:  maximilian.burger@fau.de\n      Robin Lutz:         robin.lutz@fau.de\n'




def display_hints(rworld):
    hints = {'R': "Press 'R' to start", 'S': "Press 'S' to stop drawing, simulation only",
        'D': "Press 'D' to reactive drawing", 'ESC': "Press 'ESC' to exit"}
    for i, key in enumerate(hints.keys()):
        hint = rworld.font.render(hints[key], True,
                                COLORS['white'])
        hint_rect = hint.get_rect(center=(rworld.resolution[0]/2, 
            rworld.resolution[1]/2 +((i-round(len(hints)/2))*rworld.fontSize)))
        rworld.screen.blit(hint, hint_rect)
    pg.display.flip()

def scale_resolution(scale=None):
    """
    """
    if scale == None or scale > 1.:
        print("no screen scale value set or too large. fallback to scale 0.7\n")
        scale=0.7

    # dynamic (automatic scale to quarter of system display)
    width, height=get_screen_resolution('px')
    resolution=(int(width*scale), int(height*scale))
    return resolution


def parser():
    """
    parser for rocket world, using argparse
    Returns
    -------
        args
    """
    parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent(description),
                                     epilog=textwrap.dedent(authors))
    parser.add_argument("-m", "--manually", help="used for manually parameter setup of the rocket world",
                        action="store_true", dest="manually")
    parser.add_argument(
        "-l", "--load", help="maybe used in future, to load presets", action="store_true", dest="load")
    parser.add_argument("-f", "--FPS", type=int,
                        help="set framerate", nargs=1, dest="FPS")
    parser.add_argument("-r", "--resolution", type=int, metavar=('WIDTH', 'HEIGHT'),
                        help="set desired resolution of window", nargs=2, dest="screen")
    parser.add_argument("-s", "--scale", type=float, nargs=1,
                        help="set automatic screen scaler, value between 0 and 1. Ignored if -r option is used.", dest="scale", metavar="SCALE")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true", dest="verbose")
    args=parser.parse_args()
    if args.verbose:
        print("verbosity turned on")
    return args


def random_floats(decimals=1, size=None):
    """
    Return random floats from uniform distribution of closed intervall [0,1]

    Parameters:
    -----------
        decimals : int, optional
            Number of decimal places of random floats (default: 1)

        size : int or tuple of ints, optional
            Output shape. If the given shape is, e.g., (m, n, k),
            then m * n * k samples are drawn. Default is None,
            in which case a single value is returned.
    Returns:
    --------
        out: int or ndarray of floats
            size-shaped array of random floats
    """
    # generate random integers
    u=10**decimals
    r=np.random.randint(0, u+1, size=size)
    # map random integers to [0,1]
    out=np.interp(r, [0, u], [0, 1])
    # round output to ensure decimals
    return np.round(out, decimals=decimals)


def to_pygame_acc():

    pass


def from_pygame_acc():

    pass


def to_pygame(coord, ymax):
    """
    transfrom coordinates to pygame coordinates
    Parameters
    ----------
        coord : tuple
            (x,y) - coordinates
        ymax :  int
            max screen height
    Returns
    -------
        coord : tuple
            transformed to pygame
    """
    return (int(coord[0]), int(ymax - coord[1]))


def from_pygame(coord, ymax):
    """
    transform from pygame coordinates
    Parameters
    ----------
        coord : tuple
            (x,y) - coordinates
        ymax : int
            max screen height
    Returns
    -------
        coord : tuple
            transformed from pygame
    """
    return (int(coord[0]), int(-(coord[1]-ymax)))


def userinput_integer(prompt):
    while True:
        try:
            value=int(input(prompt))
        except ValueError:
            print("expected integer. please retry..")
            continue
        else:
            break
    return value


def userinput_float(prompt):
    while True:
        try:
            value=float(input(prompt))
        except ValueError:
            print("expected float. please retry..")
            continue
        else:
            break
    return value


def get_screen_resolution(measurement="px"):
    # Source: https://stackoverflow.com/questions/3129322/how-do-i-get-monitor-resolution-in-python
    """
    Tries to detect the screen resolution from the system.
    Parameters
    ----------
        measurement: string
            The measurement to describe the screen resolution in.
            Can be either 'px', 'inch' or 'mm'.
    Returns
    -------
        (screen_width,screen_height) : tuple of int
            where screen_width and screen_height
            are int types according to measurement.
    """
    mm_per_inch=25.4
    px_per_inch=72.0  # most common
    try:  # Platforms supported by GTK3, Fx Linux/BSD
        from gi.repository import Gdk
        screen=Gdk.Screen.get_default()
        if measurement == "px":
            width=screen.get_width()
            height=screen.get_height()
        elif measurement == "inch":
            width=screen.get_width_mm()/mm_per_inch
            height=screen.get_height_mm()/mm_per_inch
        elif measurement == "mm":
            width=screen.get_width_mm()
            height=screen.get_height_mm()
        else:
            raise NotImplementedError(
                "Handling %s is not implemented." % measurement)
        # print('GdK')
        return (width, height)
    except:
        try:  # Probably the most OS independent way
            import sys
            if sys.version_info[0] < 3:
                import Tkinter as tkinter
            else:
                import tkinter
            root=tkinter.Tk()
            if measurement == "px":
                width=root.winfo_screenwidth()
                height=root.winfo_screenheight()
            elif measurement == "inch":
                width=root.winfo_screenmmwidth()/mm_per_inch
                height=root.winfo_screenmmheight()/mm_per_inch
            elif measurement == "mm":
                width=root.winfo_screenmmwidth()
                height=root.winfo_screenmmheight()
            else:
                raise NotImplementedError(
                    "Handling %s is not implemented." % measurement)
            # print('tkinter')
            root.destroy()
            return (width, height)
        except:
            try:  # Windows only
                from win32api import GetSystemMetrics
                width_px=GetSystemMetrics(0)
                height_px=GetSystemMetrics(1)
                # print('win32api')
                if measurement == "px":
                    return (width_px, height_px)
                elif measurement == "inch":
                    return (width_px/px_per_inch, height_px/px_per_inch)
                elif measurement == "mm":
                    return (width_px/mm_per_inch, height_px/mm_per_inch)
                else:
                    raise NotImplementedError(
                        "Handling %s is not implemented." % measurement)
            except:
                try:  # Windows only
                    import ctypes
                    user32=ctypes.windll.user32
                    width_px=user32.GetSystemMetrics(0)
                    height_px=user32.GetSystemMetrics(1)
                    # print('ctypes')
                    if measurement == "px":
                        return (width_px, height_px)
                    elif measurement == "inch":
                        return (width_px/px_per_inch, height_px/px_per_inch)
                    elif measurement == "mm":
                        return (width_px/mm_per_inch, height_px/mm_per_inch)
                    else:
                        raise NotImplementedError(
                            "Handling %s is not implemented." % measurement)
                except:
                    try:  # Mac OS X only
                        import AppKit
                        for screen in AppKit.NSScreen.screens():
                            width_px=screen.frame().size.width
                            height_px=screen.frame().size.height
                            # print('AppKit')
                            if measurement == "px":
                                return (width_px, height_px)
                            elif measurement == "inch":
                                return (width_px/px_per_inch, height_px/px_per_inch)
                            elif measurement == "mm":
                                return (width_px/mm_per_inch, height_px/mm_per_inch)
                            else:
                                raise NotImplementedError(
                                    "Handling %s is not implemented." % measurement)
                    except:
                        try:  # Linux/Unix
                            import Xlib.display
                            resolution=Xlib.display.Display().screen().root.get_geometry()
                            width_px=resolution.width
                            height_px=resolution.height
                            # print('Xlib')
                            if measurement == "px":
                                return (width_px, height_px)
                            elif measurement == "inch":
                                return (width_px/px_per_inch, height_px/px_per_inch)
                            elif measurement == "mm":
                                return (width_px/mm_per_inch, height_px/mm_per_inch)
                            else:
                                raise NotImplementedError(
                                    "Handling %s is not implemented." % measurement)
                        except:
                            try:  # Linux/Unix
                                if not self.is_in_path("xrandr"):
                                    raise ImportError(
                                        "Cannot read the output of xrandr, if any.")
                                else:
                                    # print('xrandr')
                                    args=["xrandr", "-q", "-d", ":0"]
                                    proc=subprocess.Popen(
                                        args, stdout=subprocess.PIPE)
                                    for line in iter(proc.stdout.readline, ''):
                                        if isinstance(line, bytes):
                                            line=line.decode("utf-8")
                                        if "Screen" in line:
                                            width_px=int(line.split()[7])
                                            height_px=int(
                                                line.split()[9][:-1])
                                            if measurement == "px":
                                                return (width_px, height_px)
                                            elif measurement == "inch":
                                                return (width_px/px_per_inch, height_px/px_per_inch)
                                            elif measurement == "mm":
                                                return (width_px/mm_per_inch, height_px/mm_per_inch)
                                            else:
                                                raise NotImplementedError(
                                                    "Handling %s is not implemented." % measurement)
                            except:
                                # Failover
                                screensize=1366, 768
                                sys.stderr.write(
                                    "WARNING: Failed to detect screen size. Falling back to %sx%s" % screensize)
                                if measurement == "px":
                                    return screensize
                                elif measurement == "inch":
                                    return (screensize[0]/px_per_inch, screensize[1]/px_per_inch)
                                elif measurement == "mm":
                                    return (screensize[0]/mm_per_inch, screensize[1]/mm_per_inch)
                                else:
                                    raise NotImplementedError(
                                        "Handling %s is not implemented." % measurement)
