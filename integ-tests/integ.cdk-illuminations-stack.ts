/// !cdk-integ CdkIlluminationsStack
// eslint-disable-next-line import/no-extraneous-dependencies
import { IntegTest } from '@aws-cdk/integ-tests-alpha';
import * as cdk from 'aws-cdk-lib';
import { CloudFrontWebDistribution, OriginAccessIdentity } from 'aws-cdk-lib/aws-cloudfront';
import { Vpc } from 'aws-cdk-lib/aws-ec2';
import { Bucket } from 'aws-cdk-lib/aws-s3';
import { CdkIlluminationsStack } from '../src/lib/cdk-illuminations-stack';

const app = new cdk.App();

const baseStack = new cdk.Stack(app, 'StackIntegTest');
const vpc = new Vpc(baseStack, 'Vpc', {});
const deploymentBucket = new Bucket(baseStack, 'Bucket', {
  removalPolicy: cdk.RemovalPolicy.DESTROY,
  autoDeleteObjects: true,
});
const originAccessIdentity = new OriginAccessIdentity(baseStack, 'OriginAccessIdentity');

const distribution = new CloudFrontWebDistribution(baseStack, 'Distribution', {
  originConfigs: [{
    s3OriginSource: {
      s3BucketSource: deploymentBucket,
      originAccessIdentity,
    },
    behaviors: [{ isDefaultBehavior: true }],
  }],
});

const stack = new CdkIlluminationsStack(app, 'CdkIlluminationsStackIntegTest', {
  vpc,
  deploymentBucket,
  distribution,
});

new IntegTest(app, 'IntegTest', {
  testCases: [
    stack,
  ],
});

app.synth();
