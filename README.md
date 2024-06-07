# CDK Illuminations for AWS Summit 2024

## directories

- `doc/`: 各種ドキュメント・画像
- `lambda/`: Lambda 関数で動作するプログラム
- `scripts/`: 各種ツール用スクリプト
- `src/`: CDK Illuminations アプリケーション

## getting started

```
npx projen deploy BaseStack
```

## scripts

- `deploy-destroy-stack.py`: CDK Illuminations スタックの作成・削除を繰り返します
- `describe-stack.py`: CDK Illuminations スタックのリソースを監視し、作成状況を出力します

```
(terminal1)
python3 deploy-destroy-stack.py

(terminal2)
python3 describe-stack.py
```

別タブで2つのプログラムを起動してください。

## architecture

- CDK Illuminations アプリケーションでは以下のアーキテクチャがデプロイされる。

![CDK Illuminations](./doc/cdk-illuminations.png)

## description

作成に時間のかかる CloudFront/VPC を BaseStack として切り出している。
事前に BaseStack をデプロイ (`npx projen deploy`) しておいて、`deploy-destroy-stack.py` でアプリケーション部分 CdkIlluminations Stack の作成・削除を繰り返す。`describe-stack.py` 側でスタックのデプロイ状況を確認し、LED への点灯指示を出す。

ALB, API Gateway の URL はデプロイ時に確定する。CdkIlluminations Stack 内で A レコードを作成してフロント側からは固定の DNS 名で指定できるようにしたいが、デプロイできるアカウントが限られてしまうので現時点ではフロントエンドは CdkIlluminations Stack に含めている。利用するドメインが確定したらフロントエンドは BaseStack 側に移動しても良い。

## TODO

- API Gateway 以下のアプリケーションが無をしている。いい感じのロジックを考えたい。
- リソース・LED のマッピングと、LED の操作部分は mock にしている。
