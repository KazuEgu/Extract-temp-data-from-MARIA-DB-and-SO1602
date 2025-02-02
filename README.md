# Extract-temp-data-from-MARIA-DB-and-SO1602<br>

以前構築した、ベランダ百葉箱で取得、Database化しているデータを手軽に確認したく、ラズパイZEROと有機ELキャラクターディスプレイ (SO1602A) を使って表示する、プログラムをPythonで検討しました。<BR>
ベランダ百葉箱の簡単な紹介は以下のリンク参照 <BR>
" https://kazuho-e-blog.tokyo/?p=1184 "　<BR>

ハードは以下の通り <br>
ラズベリーパイ ZERO W <br>
有機ELキャラクターディスプレイ S1602AWWB-UC-WB-U <br>
簡単な回路図はpdfファイル参照

開発環境 <br>
Python 3 <br>

必要ライブラリ
adafruit_so1602<br>
参考Web: " https://qiita.com/daisuzu_/items/dad8c99a01f55a7ee704 "

"sensvalues.php"<br>
上記は、Web サーバー内に保存、HTTPのGETとPOSTの処理を実装、GETの場合は全レコードをJSON形式で返す
