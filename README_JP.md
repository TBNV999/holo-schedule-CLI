# holo-schedule-CLI
ホロジュールの内容を簡易的にCLIで表示します

# Requirement
- Python 3.x
- requests


# Usage
main\.pyを実行することで、このような情報が得られます  
- いつ配信が始まるか  
- 誰が配信するか  
- その配信のURL  

# Notes
のプログラムはスクレイピングツールです。 [ソースのページ](https://schedule.hololive.tv/simple) 
は15分おきに更新されるため、最新の変更に対応できない可能性があります。  
確実に配信を見逃したくない場合、ツイッターをフォローしたり、Youtubeチャンネルを登録することを推奨します。  

このプログラムはオプションが使えます。どのようなオプションが使えるかは"--help"をつけて実行して確認してください。  

配信ではなく動画の場合、投稿後にリストに載り、その投稿時刻が配信時刻として表示されます。  

# Screenshot
![sc](https://user-images.githubusercontent.com/42367122/79976625-e26f4700-84d7-11ea-9e36-e5262e317fbd.png)  
