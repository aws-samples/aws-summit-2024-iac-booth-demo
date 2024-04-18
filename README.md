# CDK Illuminations for AWS Summit 2024

## directories

- `doc/`: 各種ドキュメント・画像
- `lambda/`: Lambda 関数で動作するプログラム
- `scripts/`: 各種ツール用スクリプト
- `src/`: CDK Illuminations アプリケーション

## getting started

```
npm ci
```

## scripts

- `deploy-destroy-stack.py`: CDK Illuminations スタックの作成・削除を繰り返します
- `describe-stack.py`: CDK Illuminations スタックのリソースを監視し、作成状況を出力します

別タブで2つのプログラムを起動してください。

## architecture

- CDK Illuminations アプリケーションでは以下のアーキテクチャがデプロイされる。

![CDK Illuminations](./doc/cdk-illuminations.png)

## TODO

- API Gateway 以下のアプリケーションが無をしている。いい感じのロジックを考えたい。
- デプロイ・削除の時間の大半を (案の定) CloudFront が占めている。CloudFront だけ別スタックに切り出して、ECS のようなちょっと重めのリソース追加してもいいかも。
- リソース・LED のマッピングと、LED の操作部分は mock にしている。
