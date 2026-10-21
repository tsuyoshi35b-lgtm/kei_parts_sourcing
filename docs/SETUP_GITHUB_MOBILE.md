# GitHub登録と、携帯から操作するための設定

ローカルの Git 初期化と最初のコミットは済み（ブランチ main、リモート origin = https://github.com/tsuyoshi35b-lgtm/kei_parts_sourcing.git を設定済み）。
残りは GitHub へのログインが必要なため、PC で次の手順を行う。

## 1. GitHub にリポジトリを作る（PCのブラウザ、2分）
1. https://github.com/new を開く
2. Repository name：`kei_parts_sourcing`
3. **Private** を選ぶ（営業先リストや今後の取引情報を含むため）
4. 「Add a README」などは**すべてチェックしない**（空のリポジトリにする）
5. Create repository

## 2. PCから送る（PowerShell、1分）
```powershell
cd C:\Users\jacka\Desktop\Claude_Tsuyoshi\projects\business\kei_parts_sourcing
git push -u origin main
```
- ea_diagnosis と同じ GitHub アカウントのログイン情報が使われる

## 3. 携帯から操作する（Claude Code on the web）
1. 携帯の Claude アプリで「Code」を開く（またはブラウザで claude.ai/code）
2. GitHub と連携し、Claude の GitHub アプリに `kei_parts_sourcing` へのアクセスを許可する
3. リポジトリ `kei_parts_sourcing` を選んでセッションを始める
- クラウド上で動くので、PC の電源が切れていても使える
- 携帯で変えた内容は GitHub に送られる。PC 側で続きをするときは、最初に `git pull` で最新にする

## 別の方法：PC の Claude Code を携帯から遠隔操作
- PC で Claude Code を起動したまま、Remote Control 機能を使うと携帯から同じセッションを操作できる（PC の電源と Claude Code が起動している間だけ）
