import { App } from 'aws-cdk-lib';
import { CdkIlluminationsStack } from './lib/cdk-illuminations-stack';

const app = new App();

new CdkIlluminationsStack(app, 'CdkIlluminations');

app.synth();
