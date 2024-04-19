import * as path from 'path';
import * as cdk from 'aws-cdk-lib';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import { ApplicationLoadBalancedFargateService } from 'aws-cdk-lib/aws-ecs-patterns';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';
// eslint-disable-next-line import/no-extraneous-dependencies
import { NodejsBuild } from 'deploy-time-build';




export interface CdkIlluminationsStackProps extends cdk.StackProps { }

export class CdkIlluminationsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: CdkIlluminationsStackProps = {}) {
    super(scope, id, props);

    const deploymentBucket = new s3.Bucket(this, 'DeploymentBucket', {
      autoDeleteObjects: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      encryption: s3.BucketEncryption.S3_MANAGED,
    });
    const deploymentPath = '/';

    const originAccessIdentity = new cloudfront.OriginAccessIdentity(this, 'OriginAccessIdentity');

    const distribution = new cloudfront.CloudFrontWebDistribution(this, 'Distribution', {
      originConfigs: [{
        s3OriginSource: {
          s3BucketSource: deploymentBucket,
          originAccessIdentity,
        },
        behaviors: [{ isDefaultBehavior: true }],
      }],
    });

    // TODO: この Lambda と DynamoDB は現時点では何もしない。
    // いい感じのロジックが思いついたら更新する。
    const writeFunction = new lambda.Function(this, 'WriteFunction', {
      code: lambda.Code.fromAsset(path.join(__dirname, '../../lambda/')),
      handler: 'write_function.handler',
      runtime: lambda.Runtime.PYTHON_3_12,
    });

    const readFunction = new lambda.Function(this, 'ReadFunction', {
      code: lambda.Code.fromAsset(path.join(__dirname, '../../lambda/')),
      handler: 'read_function.handler',
      runtime: lambda.Runtime.PYTHON_3_12,
    });

    const dynamoTable = new dynamodb.Table(this, 'DynamoTable', {
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });
    dynamoTable.grantReadData(readFunction);
    dynamoTable.grantReadWriteData(writeFunction);

    const vpc = new ec2.Vpc(this, 'Vpc', {});
    const cluster = new ecs.Cluster(this, 'Cluster', { vpc });
    const loadBalancedFargateService = new ApplicationLoadBalancedFargateService(this, 'Service', {
      cluster,
      taskImageOptions: {
        image: ecs.ContainerImage.fromRegistry('amazon/amazon-ecs-sample'),
      },
    });

    const api = new apigateway.RestApi(this, 'RestApi');
    api.root.addMethod(
      'ANY',
      new apigateway.MockIntegration({
        integrationResponses: [{ statusCode: '200' }],
        requestTemplates: {
          'application/json': '{ "statusCode": 200 }',
        },
      }),
      {
        methodResponses: [{ statusCode: '200' }],
      },
    );
    const apiCount = api.root.addResource('count');
    apiCount.addMethod('GET', new apigateway.LambdaIntegration(readFunction));
    apiCount.addMethod('POST', new apigateway.LambdaIntegration(writeFunction));

    const assetPath = path.join(__dirname, '../assets');
    new NodejsBuild(this, 'Build', {
      assets: [
        {
          path: assetPath,
          exclude: ['node_modules'],
        },
      ],
      destinationBucket: deploymentBucket,
      destinationKeyPrefix: deploymentPath,
      outputSourceDirectory: 'dist',
      distribution,
      buildCommands: ['npm ci', 'npm run build'],
      buildEnvironment: {
        VITE_API_ENDPOINT: api.url,
        VITE_ALB_ENDPOINT: loadBalancedFargateService.loadBalancer.loadBalancerDnsName,
      },
      nodejsVersion: 20,
    });

    new cdk.CfnOutput(this, 'DistributionDomainName', { value: distribution.distributionDomainName });
  }
}
