#!/usr/bin/env python3

import os
import sys

from Alfred3 import Items, Tools


class VPN:
    CONNECTED = "Connected"
    DISCONNECTED = "Disconnected"


def get_vpn(status: str = VPN.CONNECTED) -> list:
    cmd = f'scutil --nc list | grep "\\({status}\\)" | grep -Eo \'\\"(.*)\\"\' | sed s/\\"//g'
    ret = os.popen(cmd).read().split("\n")
    out = [i for i in ret if i != ""]
    return out


def add_to_vpnlist(source: list, target: list, status: str) -> list:
    for v in source:
        vpn_tpl = (v, status)
        target.append(vpn_tpl)
    return target


def arrange(lst: list, toarrange: str) -> list:
    for i in lst:
        if i[1] == toarrange:
            lst.remove(i)
            lst.insert(0, i)
    return lst


wf = Items()

query = Tools.getArgv(1)

connected_vpn = get_vpn(status=VPN.CONNECTED)
disconnected_vpn = get_vpn(status=VPN.DISCONNECTED)

vpn = list()
vpn = add_to_vpnlist(connected_vpn, vpn, VPN.CONNECTED)
vpn = add_to_vpnlist(disconnected_vpn, vpn, VPN.DISCONNECTED)

if len(vpn) > 0:
    vpn = arrange(vpn, VPN.CONNECTED)
    for v in vpn:
        if query.lower() in v[0].lower() or query == "":
            arg = f"connect" if v[1] == VPN.DISCONNECTED else f"disconnect"
            wf.setItem(
                title=f"{v[0]}",
                subtitle=f"{v[1].upper()}, Press \u23CE to {arg}",
                arg=f"{arg};{v[0]}"
            )
            wf.setIcon(m_path=f"{v[1]}.png", m_type="image)")
            wf.addItem()
else:
    wf.setItem(
        title="No VPN configuration found",
        subtitle="Please configure VPN connection in System Preferences → Network",
        valid=False
    )
    wf.addItem()

if wf.getItemsLengths == 0:
    wf.setItem(
        title=f'No VPN connection matches "{query}"',
        subtitle="Try again",
        valid=False
    )
    wf.addItem()
wf.write()
