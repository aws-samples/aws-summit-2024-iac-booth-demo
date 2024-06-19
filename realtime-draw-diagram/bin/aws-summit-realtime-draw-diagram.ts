#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { AwsSummitRealtimeDrawDiagramStack } from "../lib/aws-summit-realtime-draw-diagram-stack";

const app = new cdk.App();
new AwsSummitRealtimeDrawDiagramStack(
  app,
  "AwsSummitRealtimeDrawDiagramStack"
);