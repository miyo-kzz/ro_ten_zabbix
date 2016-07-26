#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import argparse
import json
import re
import socket
import struct
import sys
from datetime import datetime as dt
from HTMLParser import HTMLParser
from urllib import urlopen,urlencode

class ROtenZabbix(HTMLParser):
    def __init__(self, item, refining, card, world, zbx_host, zbx_port, debug):
        HTMLParser.__init__(self)
        self.zbx_host = zbx_host
        self.zbx_port = zbx_port
        self.result_trade = False
        self.date = False
        self.num = False
        self.itemform = False
        self.item = item
        self.item_name = ''
        self.item_refining = ('all' if refining == '-1' else refining)
        self.item_card = ['無', '有', 'all']
        self.card = self.item_card[card]
        self.map_name = ''
        self.timestamp = ''
        self.zeny = ''
        self.world = world
        self.lld_json = []
        self.send_items = []
        self.debug = debug

    def handle_starttag(self, tagname, attribute):
        if tagname.lower() == "input":
            for i in attribute:
                if i[0].lower() == 'id' and i[1].lower() == 'item_name':
                    self.itemform = True
                elif self.itemform and i[0].lower() == 'value':
                    self.item_name = i[1]
                    self.itemform = False
        if tagname.lower() == "div":
            for i in attribute:
                if i[0].lower() == "class" and i[1].lower() == "result_trade":
                    self.result_trade = True
                if i[0].lower() == "class" and i[1].lower() == "result_recent":
                    self.result_trade = False

        if self.result_trade and tagname.lower() == "p":
            for i in attribute:
                if i[0].lower() == "class" and i[1].lower() == "date":
                    self.date = True
                elif i[0].lower() == "class" and i[1].lower() == "num":
                    self.num = True

    def handle_data(self, data):
        if self.result_trade:
            if self.date:
                if re.match("^[0-9]+/[0-9].*", data):
                    self.timestamp = int(time.mktime(time.strptime(data, "%Y/%m/%d %H:%M")))
                else:
                    self.map_name = data
                self.date = False
            elif self.num:
                self.zeny = int(data.replace(",", ""))
                #print "* %s" % self.map_name.encode('utf8')
                send_item = {
                    "host":self.world,
                    #"key":"ragnarok.item[%s.%s]" % (self.item, self.map_name.encode('utf8')),
                    "key":"ragnarok.item[%s,r:%s,c:%s,m:%s]" % (self.item, self.item_refining, self.card, self.map_name),
                    "clock":int(self.timestamp),
                    "value":self.zeny
                }
                self.send_items.append(send_item)
                self.num = False


    def show_lld(self):
        add_list = []
        #lld_json = json.loads('{"data":[]}')
        for send_item in self.send_items:
            map_name = re.search('.*\[(.*)\,r:(.*),c:(.*),m:(.*)\]', send_item["key"]).group(4)
            if map_name not in add_list:
                lld_json_string = '{"{#TRADE.ITEM}":"","{#TRADE.ITEMNAME}":"","{#TRADE.ITEMREFINING}":"","{#TRADE.ITEMCARD}":"","{#TRADE.MAPNAME}":"","{#TRADE.UNIT}":""}'
                lld_item = json.loads(lld_json_string)
                lld_item['{#TRADE.ITEM}'] = self.item
                lld_item['{#TRADE.ITEMNAME}'] = self.item_name
                lld_item['{#TRADE.ITEMREFINING}'] = self.item_refining
                lld_item['{#TRADE.ITEMCARD}'] = self.card
                lld_item['{#TRADE.MAPNAME}'] = map_name
                lld_item['{#TRADE.UNIT}'] = 'Zeny'
                add_list.append(map_name)
                self.lld_json.append(lld_item)
        #    lld_json["data"].append(lld_item)
        #print json.dumps(lld_json, ensure_ascii=False)


    def send_to_zabbix(self):
        if not self.send_items:
            print "No items."
            return

        send_data = json.loads('{"request":"sender data","data":[]}')
        send_data["data"].extend(self.send_items)

        if not self.debug:
            zbx = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                zbx.connect((self.zbx_host, self.zbx_port))
            except Exception:
                print "Error: can not connect server"
                quit()

        send_data_string = json.dumps(send_data)
        send_data_string = eval("u'''%s'''" % send_data_string).encode('utf8')
        header = struct.pack('<4sBQ', 'ZBXD', 1, len(send_data_string))
        send_data_string = header + send_data_string

        if not self.debug:
            try:
                zbx.sendall(send_data_string)
            except Exception:
                print "Error: send error"
                quit()
        
            res = ''
            while True:
                data = zbx.recv(4096)
                if not data:
                    break
                res += data

            print res[13:]
            zbx.close()
        else:
            print "** debug **"
            print send_data_string


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')

    worlds = [
            'Sigrun', 'Alvitr', 'Vali', 'Trudr', 'Radgrid', 'Olrun', 'Gimle',
            'Hervor', 'Idavoll', 'Frigg', 'Mimir', 'Lif', 'Breidablik', 'Urdr'
        ]
    refinings = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    lld_json_all = json.loads('{"data":[]}')
    
    parser = argparse.ArgumentParser(description='Get Ragnarok Online item trade information')
    parser.add_argument('-H', '--zbx-host',
                        default='127.0.0.1',
                        help='set Zabbix Server address (e.g.: 127.0.0.1)')
    parser.add_argument('-i', '--item',
                        required=True,
                        help='set Item number, search from http://rotool.gungho.jp')
    parser.add_argument('-c', '--card', default=2, type=int,
                        help='set Has card (e.g.: 0=none 1=set 2=none/set, default=2')
    parser.add_argument('-d', '--debug', action='store_true',
                        default=False, help='set Debug mode')
    parser.add_argument('-m', '--mode',
                        default='Show', choices=['Send', 'Show'],
                        help='set Mode (e.g.: Send, Show)')
    parser.add_argument('-P', '--zbx-port', type=int,
                        default=10051, help='set Zabbix Server port (e.g.: 10051)')
    parser.add_argument('-r', '--refining', default='-1',
                        help='set Seiren value (e.g.: 0 ... 10, default=-1')
    parser.add_argument('-w', '--world',
                        required=True, choices=worlds, help='set World name')
    args = parser.parse_args()

    world_num = worlds.index(args.world) + 1
    for item in args.item.split(','):
        for refining in args.refining.split(','):
            url = "http://rotool.gungho.jp/torihiki/index.php?item=%s&world=%s" % (item, world_num)
            if refining != '-1':
                url += "&refining[]=%s" % refining
            if args.card < 2:
                url += "&card=%s" % args.card

            html = urlopen(url)
            rotool = ROtenZabbix(item, refining, args.card, args.world, args.zbx_host, args.zbx_port, args.debug)
            rotool.feed(html.read())
            html.close()

            if args.mode == 'Send':
                rotool.send_to_zabbix()
            else:
                rotool.show_lld()
                lld_json_all["data"].extend(rotool.lld_json)

    if args.mode == 'Show':
        print json.dumps(lld_json_all, ensure_ascii=False)
