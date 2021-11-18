# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Helper Module containing various sites direct links generators. This module is copied and modified as per need
from https://github.com/AvinashReddy3108/PaperplaneExtended . I hereby take no credit of the following code other
than the modifications. See https://github.com/AvinashReddy3108/PaperplaneExtended/commits/master/userbot/modules/direct_links.py
for original authorship. """

import json
import re
import urllib.parse
from base64 import standard_b64encode
from os import popen
from random import choice

import requests
from bs4 import BeautifulSoup
from js2py import EvalJs
from lk21 import Bypass

from bot.helper.ext_utils.exceptions import DirectDownloadLinkException


def direct_link_generator(link: str):
    """direct links generator"""
    if not link:
        raise DirectDownloadLinkException("`No links found!`")
    elif "zippyshare.com" in link:
        return zippy_share(link)
    elif "yadi.sk" in link:
        return yandex_disk(link)
    elif "cloud.mail.ru" in link:
        return cm_ru(link)
    elif "mediafire.com" in link:
        return mediafire(link)
    elif "osdn.net" in link:
        return osdn(link)
    elif "github.com" in link:
        return github(link)
    elif "racaty.net" in link:
        return racaty(link)
    elif "hxfile.co" in link:
        return hxfile(link)
    elif "anonfiles.com" in link:
        return anon(link)
    elif "fembed.com" in link:
        return fembed(link)
    elif "femax20.com" in link:
        return fembed(link)
    elif "naniplay.nanime.in" in link:
        return fembed(link)
    elif "naniplay.nanime.biz" in link:
        return fembed(link)
    elif "naniplay.com" in link:
        return fembed(link)
    elif "layarkacaxxi.icu" in link:
        return fembed(link)
    elif "sbembed.com" in link:
        return sbembed(link)
    elif "streamsb.net" in link:
        return sbembed(link)
    elif "1drv.ms" in link:
        return onedrive(link)
    else:
        raise DirectDownloadLinkException(f"No Direct link function found for {link}")


def zippy_share(url: str) -> str:
    link = re.findall("https:/.(.*?).zippyshare", url)[0]
    response_content = (requests.get(url)).content
    bs_obj = BeautifulSoup(response_content, "lxml")

    try:
        js_script = bs_obj.find("div", {"class": "center",}).find_all(
            "script"
        )[1]
    except:
        js_script = bs_obj.find("div", {"class": "right",}).find_all(
            "script"
        )[0]

    js_content = re.findall(r'\.href.=."/(.*?)";', str(js_script))
    js_content = 'var x = "/' + js_content[0] + '"'

    evaljs = EvalJs()
    setattr(evaljs, "x", None)
    evaljs.execute(js_content)
    js_content = getattr(evaljs, "x")

    return f"https://{link}.zippyshare.com{js_content}"


def yandex_disk(url: str) -> str:
    """Yandex.Disk direct links generator
    Based on https://github.com/wldhx/yadisk-direct"""
    try:
        link = re.findall(r"\bhttps?://.*yadi\.sk\S+", url)[0]
    except IndexError:
        return "`No Yandex.Disk links found`\n"
    api = "https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}"
    try:
        return requests.get(api.format(link)).json()["href"]
    except KeyError:
        raise DirectDownloadLinkException(
            "`Error: File not found / Download limit reached`\n"
        )


def cm_ru(url: str) -> str:
    """cloud.mail.ru direct links generator
    Using https://github.com/JrMasterModelBuilder/cmrudl.py"""
    try:
        link = re.findall(r"\bhttps?://.*cloud\.mail\.ru\S+", url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No cloud.mail.ru links found`\n")
    command = f"vendor/cmrudl/cmrudl -s {link}"
    result = popen(command).read()
    result = result.splitlines()[-1]
    try:
        data = json.loads(result)
    except json.decoder.JSONDecodeError:
        raise DirectDownloadLinkException("`Error: Can't extract the link`\n")
    return data["download"]


def mediafire(url: str) -> str:
    """MediaFire direct links generator"""
    try:
        link = re.findall(r"\bhttps?://.*mediafire\.com\S+", url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No MediaFire links found`\n")
    page = BeautifulSoup(requests.get(link).content, "lxml")
    info = page.find("a", {"aria-label": "Download file"})
    return info.get("href")


def osdn(url: str) -> str:
    """OSDN direct links generator"""
    osdn_link = "https://osdn.net"
    try:
        link = re.findall(r"\bhttps?://.*osdn\.net\S+", url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No OSDN links found`\n")
    page = BeautifulSoup(requests.get(link, allow_redirects=True).content, "lxml")
    info = page.find("a", {"class": "mirror_link"})
    link = urllib.parse.unquote(osdn_link + info["href"])
    mirrors = page.find("form", {"id": "mirror-select-form"}).findAll("tr")
    urls = []
    for data in mirrors[1:]:
        mirror = data.find("input")["value"]
        urls.append(re.sub(r"m=(.*)&f", f"m={mirror}&f", link))
    return urls[0]


def github(url: str) -> str:
    """GitHub direct links generator"""
    try:
        re.findall(r"\bhttps?://.*github\.com.*releases\S+", url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No GitHub Releases links found`\n")
    download = requests.get(url, stream=True, allow_redirects=False)
    try:
        return download.headers["location"]
    except KeyError:
        raise DirectDownloadLinkException("`Error: Can't extract the link`\n")


def racaty(url: str) -> str:
    try:
        link = re.findall(r"\bhttps?://.*racaty\.net\S+", url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No Racaty links found`\n")
    reqs = requests.get(link)
    bss = BeautifulSoup(reqs.text, "html.parser")
    op = bss.find("input", {"name": "op"})["value"]
    id = bss.find("input", {"name": "id"})["value"]
    rep = requests.post(link, data={"op": op, "id": id})
    bss2 = BeautifulSoup(rep.text, "html.parser")
    return bss2.find("a", {"id": "uniqueExpirylink"})["href"]


def useragent():
    """
    useragent random setter
    """
    useragents = BeautifulSoup(
        requests.get(
            "https://developers.whatismybrowser.com/"
            "useragents/explore/operating_system_name/android/"
        ).content,
        "lxml",
    ).findAll("td", {"class": "useragent"})
    user_agent = choice(useragents)
    return user_agent.text


def hxfile(url: str) -> str:
    """Hxfile direct links generator
    based on https://github.com/breakdowns/slam-mirrorbot"""
    try:
        link = re.findall(r"\bhttps?://.*hxfile\.co\S+", url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No Hxfile links found`\n")
    bypasser = Bypass()
    return str(bypasser.bypass_url(link))


def anon(url: str) -> str:
    """Anonfiles direct links generator
    based on https://github.com/breakdowns/slam-mirrorbot"""
    try:
        link = re.findall(r"\bhttps?://.*anonfiles\.com\S+", url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No Anonfiles links found`\n")
    bypasser = Bypass()
    return str(bypasser.bypass_url(link))


def fembed(link: str) -> str:
    """Fembed direct link generator
    Based on https://github.com/breakdowns/slam-mirrorbot"""
    bypasser = Bypass()
    result_dict = bypasser.bypass_fembed(link)
    return list(result_dict.keys())[-1]


def sbembed(link: str) -> str:
    """Sbembed direct link generator
    Based on https://github.com/breakdowns/slam-mirrorbot"""
    bypasser = Bypass()
    result_dict = bypasser.bypass_sbembed(link)
    return list(result_dict.keys())[-1]


def onedrive(link: str) -> str:
    """Onedrive direct link generator
    Based on https://github.com/UsergeTeam/Userge"""
    link_without_query = urllib.parse.urlparse(link)._replace(query=None).geturl()
    direct_link_encoded = str(
        standard_b64encode(bytes(link_without_query, "utf-8")), "utf-8"
    )
    direct_link1 = (
        f"https://api.onedrive.com/v1.0/shares/u!{direct_link_encoded}/root/content"
    )
    resp = requests.head(direct_link1)
    if resp.status_code != 302:
        return "`Error: Unauthorized link, the link may be private`"
    return str(resp.next.url)