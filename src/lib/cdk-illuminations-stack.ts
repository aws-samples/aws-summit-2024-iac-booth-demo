import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';

export interface CdkIlluminationsStackProps extends cdk.StackProps {}

export class CdkIlluminationsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: CdkIlluminationsStackProps = {}) {
    super(scope, id, props);
  }
}
