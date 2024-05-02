import { App } from 'aws-cdk-lib';
import { BaseStack } from './lib/base-stack';
import { CdkIlluminationsStack } from './lib/cdk-illuminations-stack';

const app = new App();

const baseStack = new BaseStack(app, 'BaseStack');

new CdkIlluminationsStack(app, 'CdkIlluminations', {
  vpc: baseStack.vpc,
  deploymentBucket: baseStack.deploymentBucket,
  distribution: baseStack.distribution,
});

app.synth();
