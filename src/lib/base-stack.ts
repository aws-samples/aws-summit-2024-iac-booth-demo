import * as cdk from 'aws-cdk-lib';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';

export interface BaseStackProps extends cdk.StackProps { }

/**
 * @abstract デプロイしたままにするリソースを含むスタック
 */
export class BaseStack extends cdk.Stack {
  public readonly vpc: ec2.Vpc;
  public readonly deploymentBucket: s3.Bucket;
  public readonly distribution: cloudfront.CloudFrontWebDistribution;

  constructor(scope: Construct, id: string, props: BaseStackProps = {}) {
    super(scope, id, props);

    const deploymentBucket = new s3.Bucket(this, 'DeploymentBucket', {
      autoDeleteObjects: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      encryption: s3.BucketEncryption.S3_MANAGED,
    });

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

    const vpc = new ec2.Vpc(this, 'Vpc', {});

    this.vpc = vpc;
    this.deploymentBucket = deploymentBucket;
    this.distribution = distribution;

    new cdk.CfnOutput(this, 'DistributionDomainName', { value: distribution.distributionDomainName });
  }
}
