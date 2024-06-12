
# スタックと各リソースのデプロイ状況を監視し、LED を点滅させる
from typing import Tuple
import serial
import time
import boto3

# 監視対象のスタック名
CDK_ILLUMINATIONS_STACK = 'CdkIlluminations'
BASE_STACK = 'BaseStack'


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
    # print("serial write:", code)
    pass


def turn_off_all_leds():
    '''
    全ての LED を消灯する
    '''

    # LED の個数
    LED_NUM = 11

    for i in range(LED_NUM):
        change_color(i, Color.BLACK)


def get_resource_status_color(resource: dict) -> Color:
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


def get_stack_status_color(stack_status: str) -> Color:
    '''
    スタックを表す json を受け取り、ステータスに対応する LED カラーを返す
    '''
    # CloudFormation 上のステータスと色の対応関係 (割り当ては適当)
    resource_status_color_mapping = {
        'CREATE_COMPLETE': Color.BLUE,
        'CREATE_IN_PROGRESS': Color.GREEN,
        'CREATE_FAILED': Color.RED,
        'UPDATE_COMPLETE': Color.BLUE,
        'UPDATE_IN_PROGRESS': Color.GREEN,
        'UPDATE_FAILED': Color.RED,
        'DELETE_COMPLETE': Color.BLACK,
        'DELETE_IN_PROGRESS': Color.ORANGE,
        'DELETE_FAILED': Color.RED,
    }

    # StackStatus が対応関係にあるものなら対応表を参照して Color を決定、そうでなければ WHITE を返しておく
    return resource_status_color_mapping.get(stack_status, Color.WHITE)


def get_stack_led_mapping(stack_name: str):
    stack_name_led_mapping = {
        CDK_ILLUMINATIONS_STACK: 6,
        BASE_STACK: 7,
    }


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
        's3deployment': 5,  # Custom::CDKBucketDeployment
        'ANY': 1,  # AWS::ApiGateway::Method
        'CdkIlluminationsReadFunction': 4,  # AWS::Lambda::Function
        'CdkIlluminationsTable': 8,  # AWS::DynamoDB::Table
        'loadbalancer': 2,  # AWS::ElasticLoadBalancingV2::LoadBalancer
        'CdkIlluminationsCluster/CdkIlluminationsService': 9,  # AWS::ECS::Service
        'CdkIlluminationsCluster': 3,  # AWS::ECS::Cluster
    }

    resource_type_led_mapping = {
        'AWS::CloudFront::Distribution': 0,
        #'AWS::EC2::VPC': 8  # EC2::VPC
    }

    for identifier, led_index in resource_identifier_led_mapping.items():
        if 'PhysicalResourceId' not in resource:
            continue
        try:
            if identifier in resource['PhysicalResourceId']:
                return True, led_index
        except Exception as e:
            print(e, resource)

    for identifier, led_index in resource_type_led_mapping.items():
        if 'ResourceType' not in resource:
            continue
        try:
            if identifier == resource['ResourceType']:
                return True, led_index
        except Exception as e:
            print(e, resource)

    return False, -1


def apply_stack_resources_status(stack_name: str):
    '''
    指定したスタックのリソースのステータスを確認し、LED の色を変更する
    '''
    # スタック内のリソース一覧情報を取得
    print(stack_name, ':')
    try:
        response = cfn.list_stack_resources(StackName=stack_name)
        resources = response['StackResourceSummaries']
        for resource in resources:
            is_target, led_index = is_target_resource(resource)
            if not is_target:
                continue

            led_color = get_resource_status_color(resource)

            print(f'ResourceType: {resource["ResourceType"]}, LogicalResourceId: {
                resource["LogicalResourceId"]}, ResourceStatus: {resource['ResourceStatus']}')
            # LED 状態を変更する
            change_color(led_index, led_color)

    except Exception as e:
        # スタックが存在しない場合
        print(f'スタックが存在しません: {e}')
        # 全ての LED を OFF にする
        # turn_off_all_leds()

    print('------------------')


def apply_stack_status(stack_name: str):
    '''
    指定したスタックのステータスを確認し、LED の色を変更する
    '''
    # スタック情報を取得
    led_index = get_stack_led_mapping(stack_name)
    try:
        response = cfn.describe_stacks(StackName=stack_name)
        stack = response['Stacks'][0]
        stack_status = stack['StackStatus']
        print(f'StackName: {stack_name}, StackStatus: {stack_status}')
        led_color = get_stack_status_color(stack_status)
        # LED 状態を変更する
        change_color(led_index, led_color)

    except Exception as e:
        # スタックが存在しない場合
        print(f'スタックが存在しません: {e}')
        change_color(led_index, Color.BLACK)
        # 全ての LED を OFF にする
        # turn_off_all_leds()

    print('------------------')

if __name__ == '__main__':
    cfn = boto3.client('cloudformation')

    # 定期的に処理を実行する
    while True:
        apply_stack_resources_status(BASE_STACK)
        apply_stack_resources_status(CDK_ILLUMINATIONS_STACK)
        apply_stack_status(BASE_STACK)
        apply_stack_status(CDK_ILLUMINATIONS_STACK)
        # n 秒ごとに実行
        time.sleep(10)
