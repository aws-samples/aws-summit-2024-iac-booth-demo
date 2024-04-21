/// !cdk-integ CdkIlluminationsStack
// eslint-disable-next-line import/no-extraneous-dependencies
import { IntegTest } from '@aws-cdk/integ-tests-alpha';
import * as cdk from 'aws-cdk-lib';
import { CdkIlluminationsStack } from '../src/lib/cdk-illuminations-stack';

const app = new cdk.App();

new IntegTest(app, 'IntegTest', {
  testCases: [
    new CdkIlluminationsStack(app, 'CdkIlluminationsStackIntegTest')
  ],
});

app.synth();
