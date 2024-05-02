/// !cdk-integ CdkIlluminationsStack
// eslint-disable-next-line import/no-extraneous-dependencies
import { IntegTest } from '@aws-cdk/integ-tests-alpha';
import * as cdk from 'aws-cdk-lib';
import { BaseStack } from '../src/lib/base-stack';

const app = new cdk.App();

const baseStack = new BaseStack(app, 'BaseStackIntegTest');

new IntegTest(app, 'IntegTest', {
  testCases: [
    baseStack,
  ],
});

app.synth();
