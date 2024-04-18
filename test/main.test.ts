import { App } from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { CdkIlluminationsStack } from '../src/lib/cdk-illuminations-stack';

test('Snapshot', () => {
  const app = new App();
  const stack = new CdkIlluminationsStack(app, 'test');

  const template = Template.fromStack(stack);
  expect(template.toJSON()).toMatchSnapshot();
});
