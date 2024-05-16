# スタックと各リソースのデプロイ状況を監視し、LED を点滅させる
from typing import Tuple
import serial
import time
import boto3

# 監視対象のスタック名
target_stack_name = 'CdkIlluminations'


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

# LED 管理用の処理
# PORT = '/dev/cu.usbmodem1101'

# ser = serial.Serial(PORT, 9600)


def change_color(led_index: int, color: tuple):
    code = ','.join(map(str, [led_index, color[0], color[1], color[2]])) + '\n'
    # ser.write(bytes(code, 'utf-8'))
    dummy_change_color(code)
    time.sleep(0.11)


def dummy_change_color(code):
    '''
    LED に繋いでいない時用の処理
    '''
    print("serial write:", code)


def turn_off_all_leds():
    '''
    全ての LED を消灯する
    '''

    # LED の個数
    LED_NUM = 10

    for i in range(LED_NUM):
        change_color(i, Color.BLACK)


def get_status_color(resource: dict) -> Color:
    '''
    リソースを表す json を受け取り、ステータスに対応する LED カラーを返す
    '''
    # CloudFormation 上のステータスと色の対応関係 (割り当ては適当)
    resource_status_color_mapping = {
        'CREATE_COMPLETE': Color.BLUE,
        'CREATE_IN_PROGRESS': Color.GREEN,
        'CREATE_FAILED': Color.RED,
        'DELETE_COMPLETE': Color.BLACK,
        'DELETE_IN_PROGRESS': Color.ORANGE,
        'DELETE_FAILED': Color.RED,
    }

    # ResourceStatus が対応関係にあるものなら対応表を参照して Color を決定、そうでなければ WHITE を返しておく
    return resource_status_color_mapping.get(resource['ResourceStatus'], Color.WHITE)


def is_target_resource(resource: dict) -> Tuple[bool, int]:
    '''
    リソースを表す json を受け取り、(監視対象のリソースか、そうならば何番目の LED に対応するか) を返す

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

    # リソースと LED の対応関係
    # PhysicalResourceId の一意に識別可能な部分文字列と LED インデックスの組合せ
    resource_identifier_led_mapping = {
        's3deployment': 0,  # Custom::CDKBucketDeployment
        'ANY': 1,  # AWS::ApiGateway::Method
        'CdkIlluminationsReadFunction': 2,  # AWS::Lambda::Function
        'CdkIlluminationsTable': 3,  # AWS::DynamoDB::Table
        'loadbalancer': 4,  # AWS::ElasticLoadBalancingV2::LoadBalancer
        'CdkIlluminationsService': 5,  # AWS::ECS::Service
        'CdkIlluminationsCluster': 6,  # AWS::ECS::Cluster
        # CloudFront::Distribution
        # VPC
        # Stack
    }

    for identifier, led_index in resource_identifier_led_mapping.items():
        if identifier in resource['PhysicalResourceId']:
            return True, led_index

    return False, -1


if __name__ == '__main__':
    cfn = boto3.client('cloudformation')

    # 定期的に処理を実行する
    while True:
        # スタック内のリソース一覧情報を取得
        try:
            response = cfn.list_stack_resources(StackName=target_stack_name)
            resources = response['StackResourceSummaries']
            for resource in resources:
                is_target, led_index = is_target_resource(resource)
                if not is_target:
                    continue

                led_color = get_status_color(resource)

                # print(f'ResourceType: {resource["ResourceType"]}, LogicalResourceId: {
                #     resource["LogicalResourceId"]}, ResourceStatus: {resource['ResourceStatus']}')
                # LED 状態を変更する
                change_color(led_index, led_color)

        except Exception as e:
            # スタックが存在しない場合
            print(f'スタックが存在しません: {e}')
            # 全ての LED を OFF にする
            turn_off_all_leds()

        # n 秒ごとに実行
        time.sleep(10)
        print('------------------------')
