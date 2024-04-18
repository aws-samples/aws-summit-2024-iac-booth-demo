# スタックと各リソースのデプロイ状況を監視し、LED を点滅させる

# 監視対象のスタック名
import time
import boto3

target_stack_name = 'CdkIlluminations'

# 監視対象のリソースタイプ
target_resource_type = ['AWS::Lambda::Function', 'AWS::S3::Bucket',
                        'AWS::CloudFront::Distribution', 'AWS::DynamoDB::Table', 'AWS::ApiGateway::RestApi',]
# 自動的に作成される Lambda 関数は監視対象に含めたくない
exclude_logical_resource_keywords = ['Custom']


def is_target_resource(resource: str) -> bool:
    '''
    リソースの形式例
    {
        "LogicalResourceId": "DeploymentBucketC91A09DA",
        "PhysicalResourceId": "cdkilluminations-deploymentbucketc91a09da-m97w2za96d9b",
        "ResourceType": "AWS::S3::Bucket",
        "LastUpdatedTimestamp": "2024-04-18T02:28:37.518000+00:00",
        "ResourceStatus": "CREATE_COMPLETE",
        "DriftInformation": {
            "StackResourceDriftStatus": "NOT_CHECKED"
        }
    },
    '''
    if resource['ResourceType'] not in target_resource_type:
        return False
    for keyword in exclude_logical_resource_keywords:
        if keyword in resource['LogicalResourceId']:
            return False

    return True


# LED 状態変更用 dummy API
def change_led_status(resource_id: str, resource_status: str):
    '''
    TODO: ボード上の LED とリソースの対応関係を何らかの方法でマッピングする必要がある
    '''
    print(f'Change LED status: {resource_id} {resource_status}')

# 全ての LED を OFF にする dummy API
def turn_off_all_leds():
    print('Turn off all LEDs')

if __name__ == '__main__':
    cfn = boto3.client('cloudformation')

    # 定期的に処理を実行する
    while True:
        # スタック内のリソース一覧情報を取得
        try:
            response = cfn.list_stack_resources(StackName=target_stack_name)
            resources = response['StackResourceSummaries']
            for resource in resources:
                if not is_target_resource(resource):
                    continue

                print(f'ResourceType: {resource["ResourceType"]}, LogicalResourceId: {
                    resource["LogicalResourceId"]}, ResourceStatus: {resource['ResourceStatus']}')
                # LED 状態を変更する
                # change_led_status(resource['LogicalResourceId'], resource['ResourceStatus'])
        
        except Exception as e:
            # スタックが存在しない場合
            print(f'スタックが存在しません: {e}')
            # 全ての LED を OFF にする
            # turn_off_all_leds()

        # n 秒ごとに実行
        time.sleep(5)
