import re
import shodan
import os
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.scrolledtext import ScrolledText
import idlelib.colorizer as ic
import idlelib.percolator as ip


api = shodan.Shodan('9r6vVczYqYGR9F3WADASttMPt6fqK2Mm')
window = Tk()
window.title("shadow utility")
window.geometry("1920x1080")

menu = Menu(window)
window.config(menu=menu)


editor = ScrolledText(window, font=("Consolas 10"), wrap=None)
editor.config(fg="black", bg="white")
editor.pack(side=LEFT, fill=BOTH, expand=1)
editor.focus()


output_window = ScrolledText(window, wrap=None)
output_window.config(fg="white", bg="black", insertbackground="white")
output_window.pack(side=RIGHT, fill=BOTH, expand=1)
output_window.config(state=DISABLED)


def inform(IP):
    try:
        ipinfo = api.host(IP)
        address = ipinfo['ip_str']
        country = ipinfo['country_name']
        city = ipinfo['city']
        ports = ipinfo['ports']
        update = ipinfo['last_update']
        domains = ipinfo['domains']
        x = """
            IP : %s
            COUNTRY : %s
            CITY: %s
            PORTS_OPEN : %s
            LAST_UPDATE : %s
            ASSOCIATED_DOMAINS : %s
        """ % (address, country, city, ports, update, domains)
        print(x)
        return(x)
    except shodan.APIError as e:
        return "Error: %s" % (e)


def search(query):

    try:
        dat = ""
        results = api.search(query)
        for result in results['matches']:
            print(dat)
            dat = dat+"""
        IP : %s
        *******results******
    
        %s

            """ % (result['ip_str'], result['data'])

        return dat
    except shodan.APIError as e:
        return "Error: %s" % (e)


def run(event=None):
    output_window.config(state=NORMAL)
    code = editor.get(1.0, END)
    runner = code.split()
    output = "Searching ...."
    if runner[0].lower() == "info":
        host = runner[1]
        info = inform(host)
        output = info
    elif runner[0].lower() == "find":
        query = runner[1]
        info = search(query)
        output = info
    else:
        output = "err"
    output_window.delete(1.0, END)
    output_window.insert(1.0, output)
    output_window.config(state=DISABLED)


run_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Run", menu=run_menu)
run_menu.add_command(label="Run", accelerator="F5", command=run)
window.bind("<F5>", run)


# color scheme syntax setup

KKWORD = r"\b(?P<KKWORD>HTTP|IP|text/html|charset|close|COUNTRY|CITY|PORTS_OPEN|LAST_UPDATE|ASSOCIATED_DOMAINS)\b"
GOOD = r"\b(?P<GOOD>HTTP/1.1|200|OK|results)\b"
DATA = r"\b(?P<DATA>Connection|Content-Type|Content-Length|Cache-control|Date|Expires|Pragma|Server)\b"
PROG = rf"{KKWORD}|{GOOD}|{DATA}"
cdg = ic.ColorDelegator()
ndg = ic.ColorDelegator()

ndg.prog = re.compile(PROG, re.S | re.M)
cdg.tagdefs['COMMENT'] = {'foreground': '#FF0000', 'background': 'none'}
cdg.tagdefs['KEYWORD'] = {'foreground': '#007F00', 'background': 'none'}
cdg.tagdefs['BUILTIN'] = {'foreground': '#7F7F00', 'background': 'none'}
cdg.tagdefs['STRING'] = {'foreground': '#7F3F00', 'background': 'none'}
cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': 'none'}


ndg.tagdefs['KKWORD'] = {'foreground': '#007F00', 'background': 'none'}
ndg.tagdefs['GOOD'] = {'foreground': '#007F7F', 'background': 'none'}
ndg.tagdefs['STRING'] = {'foreground': '#7F3F00', 'background': 'none'}

ip.Percolator(editor).insertfilter(cdg)
ip.Percolator(output_window).insertfilter(ndg)
###########################


window.mainloop()
