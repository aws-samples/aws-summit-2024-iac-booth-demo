import { awscdk } from 'projen';
const project = new awscdk.AwsCdkTypeScriptApp({
  cdkVersion: '2.1.0',
  defaultReleaseBranch: 'main',
  name: 'cdk-illuminations-summit2024',
  projenrcTs: true,
  deps: ['deploy-time-build', '@aws-cdk/integ-tests-alpha@^2.137.0-alpha.0', '@aws-cdk/integ-runner@^2.137.0-alpha.0'],
  // deps: [],                /* Runtime dependencies of this module. */
  // description: undefined,  /* The description is just a string that helps people understand the purpose of the package. */
  // devDeps: [],             /* Build dependencies for this module. */
  // packageName: undefined,  /* The "name" in package.json. */
});
project.tsconfigDev.include.push('src/**/*.tsx');
project.tsconfigDev.include.push('integ-tests/*.ts');
project.addScripts({
  'integ-tests': 'integ-runner --directory ./integ-tests --parallel-regions us-east-1 --update-on-failed',
});
project.synth();
