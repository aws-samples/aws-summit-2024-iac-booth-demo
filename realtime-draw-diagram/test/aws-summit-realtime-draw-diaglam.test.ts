import * as cdk from "aws-cdk-lib";
import { Template } from "aws-cdk-lib/assertions";
import * as AwsSummitRealtimeDrawDiagram from "../lib/aws-summit-realtime-draw-diagram-stack";

test("SQS Queue and SNS Topic Created", () => {
  const app = new cdk.App();
  // WHEN
  const stack =
    new AwsSummitRealtimeDrawDiagram.AwsSummitRealtimeDrawDiagramStack(
      app,
      "MyTestStack"
    );
  // THEN

  const template = Template.fromStack(stack);

  template.hasResourceProperties("AWS::SQS::Queue", {
    VisibilityTimeout: 300,
  });
  template.resourceCountIs("AWS::SNS::Topic", 1);
});
