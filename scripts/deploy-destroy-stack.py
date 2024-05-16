# スタックを定期的に作成・削除を繰り返すプログラム

import time
import boto3
import subprocess

target_stack_name = 'CdkIlluminations'

# 作成が完了したとみなすスタックステータス
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/client/describe_stacks.html
complete_status = ['CREATE_COMPLETE', 'UPDATE_COMPLETE']

# 作成中とみなすスタックステータス
in_progress_status = ['CREATE_IN_PROGRESS', 'UPDATE_IN_PROGRESS']


def check_stack_status_complete(cfn: boto3.client):
    '''
    スタックの作成が完了しているかを確認する
    '''
    try:
        stack = cfn.describe_stacks(StackName=target_stack_name)
    except Exception as e:
        # スタックが存在しない場合
        return False

    return stack['Stacks'][0]['StackStatus'] in complete_status


def check_target_stack_exist(cfn: boto3.client):
    '''
    スタックが存在するかを確認する
    '''
    try:
        stack = cfn.describe_stacks(StackName=target_stack_name)
    except Exception as e:
        # スタックが存在しない場合
        return False

    return True


# entrypoint
if __name__ == '__main__':
    cfn = boto3.client('cloudformation')

    # スタックの作成・削除を繰り返す
    while True:
        is_exist = check_target_stack_exist(cfn)
        if not is_exist:
            print('スタックの作成を開始します')
            try:
                result = subprocess.run(
                    ['npx', 'projen', 'deploy', target_stack_name, '--require-approval', 'never'], text=True, check=True)
            except Exception as e:
                print(e.stderr)
            continue

        if check_stack_status_complete(cfn):
            # スタックのデプロイが完了している場合は削除を開始する
            print('スタックの作成が完了しました')
            print('スタックの削除を開始します')
            try:
                result = subprocess.run(
                    ['npx', 'projen', 'destroy', target_stack_name, '-f'], text=True, check=True)
            except Exception as e:
                print(e.stderr)
            continue

        print('スタックの作成が完了していません')
        time.sleep(30)
