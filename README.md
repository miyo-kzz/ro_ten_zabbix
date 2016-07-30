# ro_ten_zabbix - ROtool jRO trade infomation motitoring template for Zabbix
This template is monitoring RO official tool with Zabbix.  
[README in Japanese](https://github.com/miyo-kzz/ro_ten_zabbix/blob/master/README.ja.md)

## Requirements
* Zabbix 3.0, 2.0
* Python 2.7
* CentOS 7.2

## How to use
1. Download scripts/ro_ten_zabbix.py on your Zabbix external script directory.
2. Import templates/3.0/template_ro_trade.xml in the Web management interface on Zabbix.  
(Web management interface -> Settings -> Templates -> Import)  
In the case of Zabbix 2.2: import templates/2.2/template_ro_trade.xml
3. Register the monitoring hosts.  
If you want to monitor wolrd 'Olrun':
  * Host Name: Olrun
  * Templates: Template jRO trade
  - Macros:
    * {$ITEM}: Set item number (look for the number of 'item', search for https://rotool.gungho.jp/torihiki/)
    * {$CARD}: Set 1 (already mounted card) or 0 (not mounted) (default:2, both to search)
    * {$REFINING}: Set refining value (0...10) (default:-1, to search for all)

## License
ro_ten_zabbix.py and template_ro_trade.xml is licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)

## Contacts
Madoka: madoka@zeronet.gr.jp

---
Copyright 2016 in.zernet.gr.jp

