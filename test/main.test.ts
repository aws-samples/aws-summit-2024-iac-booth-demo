import { App } from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { BaseStack } from '../src/lib/base-stack';
import { CdkIlluminationsStack } from '../src/lib/cdk-illuminations-stack';


test('Snapshot', () => {
  const app = new App();
  const baseStack = new BaseStack(app, 'baseStack');
  const stack = new CdkIlluminationsStack(app, 'test', {
    vpc: baseStack.vpc,
    deploymentBucket: baseStack.deploymentBucket,
    distribution: baseStack.distribution,
  });

  const baseTemplate = Template.fromStack(baseStack);
  expect(baseTemplate.toJSON()).toMatchSnapshot();

  const template = Template.fromStack(stack);
  expect(template.toJSON()).toMatchSnapshot();
});
