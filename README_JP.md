# holo-schedule-CLI
ホロジュールの内容を簡易的にCLIで表示します

# Requirement
- Python 3.x
- requests
- pytz (JST以外のタイムゾーンを使う場合)


# Usage
main\.pyを実行することで、このような情報が得られます  
- いつ配信が始まるか  
- 誰が配信するか  
- その配信のURL  
- 配信のタイトル(任意)

# Notes
このプログラムはスクレイピングツールです。 [ソースのページ](https://schedule.hololive.tv/simple)
は15分おきに更新されるため、最新の変更に対応できない可能性があります。  
確実に配信を見逃したくない場合、ツイッターをフォローしたり、Youtubeチャンネルを登録することを推奨します。  

このプログラムはオプションが使えます。どのようなオプションが使えるかは"--help"をつけて実行して確認してください。  

配信ではなく動画の場合、投稿後にリストに載り、その投稿時刻が配信時刻として表示されます。プレミアムは配信として表示されます。  

タイトルの中の一部の絵文字は自動的に削除されます。

# Timezone
タイムゾーンを/text/timezoneから設定することができます。[ここ](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568)から有効なタイムゾーンを確認してください。

# Screenshot
![Screenshot](https://user-images.githubusercontent.com/42367122/111053945-9d675100-84ab-11eb-8744-adcb6354d637.png) 
