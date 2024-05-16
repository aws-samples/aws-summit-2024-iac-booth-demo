# スタックと各リソースのデプロイ状況を監視し、LED を点滅させる
import serial
import time
import boto3

# 監視対象のスタック名
target_stack_name = 'CdkIlluminations'

# LED 管理用の処理
# PORT = '/dev/cu.usbmodem1101'

# ser = serial.Serial(PORT, 9600)


def dummy_serial(code):
    print('serial write:', code)


class Color:
    RED = (0, 255, 0)
    ORANGE = (165, 255, 0)
    YELLOW = (255, 165, 0)
    GREEN = (255, 0, 0)
    LIGHT_BLUE = (255, 0, 255)
    BLUE = (0, 0, 255)
    PURPLE = (0, 255, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


def change_color(led_index: int, color: tuple):
    code = ','.join(map(str, [led_index, color[0], color[1], color[2]])) + '\n'
    # ser.write(bytes(code, 'utf-8'))
    dummy_serial(code)
    time.sleep(0.11)


# if __name__ == '__main__':
#     change_color(0, Color.RED)
#     change_color(1, Color.BLUE)
#     change_color(2, Color.RED)
#     change_color(3, Color.ORANGE)
#     change_color(4, Color.YELLOW)
#     # change_color(5, Color.GREEN)
#     # change_color(6, Color.LIGHT_BLUE)
#     # change_color(7, Color.BLUE)
#     # change_color(8, Color.PURPLE)
#     # change_color(9, Color.WHITE)

#     while 1:
#         change_color(0, Color.RED)
#         change_color(0, Color.WHITE)

# 監視対象のリソースタイプ
target_resource_type = ['AWS::Lambda::Function', 'AWS::S3::Bucket',
                        'AWS::CloudFront::Distribution', 'AWS::DynamoDB::Table', 'AWS::ApiGateway::RestApi',
                        'AWS::EC2::VPC', 'AWS::ECS::Cluster', 'AWS::ElasticLoadBalancingV2::LoadBalancer',
                        'AWS::ECS::Service']

# リソースと LED の対応関係
# PhysicalResourceId の一意に識別可能な部分文字列と LED インデックスの組合せ
resource_identifier_led_mapping = {
    's3deployment': 0,  # Custom::CDKBucketDeployment
    'ANY': 1,  # AWS::ApiGateway::Method
    'CdkIlluminationsReadFunction': 2,  # AWS::Lambda::Function
    'CdkIlluminationsTable': 3, # AWS::DynamoDB::Table
    'loadbalancer': 4, # AWS::ElasticLoadBalancingV2::LoadBalancer
    'CdkIlluminationsService': 5, # AWS::ECS::Service
    'CdkIlluminationsCluster': 6, # AWS::ECS::Cluster
    # CloudFront::Distribution
    # VPC
    # Stack
}

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
