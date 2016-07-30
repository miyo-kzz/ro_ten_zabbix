# ro_ten_zabbix - RO公式ツール 露店情報監視テンプレート for Zabbix
RO公式ツールの露店情報をZabbixで監視するテンプレートです。
[README in English](https://github.com/miyo-kzz/ro_ten_zabbix/README.md)

## 動作環境
Zabbix 3.0, 2.2
Python 2.7
CentOS 7.2

## 導入方法
1. スクリプト scripts/ro_ten_zabbix.py をZabbixの外部スクリプト用ディレクトリに保存する。
2. ZabbixのWeb管理画面でテンプレート templates/3.0/template_ro_trade.xml をインポート  
(ZabbixのWeb管理画面 -> 設定 -> テンプレート -> インポート)する。  
Zabbix 2.2の場合は templates/2.2/template_ro_trade.xml をインポートする。
3. ZabbixのWeb管理画面で、監視ホストを登録する。  
Olrunの露店情報を監視する場合
  * ホスト名: Olrun
  * テンプレート: Template jRO trade
  - マクロ:
    * {$ITEM}: アイテム番号を設定する(http://rotool.gungho.jp/torihiki/で検索してitemの番号を探す)
    * {$CARD}: カードが装着済み(1)か未装着(0)かを選択する (デフォルト:2,どちらも検索する)
    * {$REFINING}: 精錬値(0...10)を設定する (デフォルト:-1,すべてを検索する)

## ライセンス
ro_ten_zabbix.py and template_ro_trade.xml is licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)

## 連絡先
[Madoka](madoka@zeronet.gr.jp)

---
Copyright 2016 in.zeronet.gr.jp

