import {
    Stack,
    StackProps,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda,
    aws_appintegrations,
} from "aws-cdk-lib";
import { Construct } from "constructs";
import * as apig from "@aws-cdk/aws-apigatewayv2-alpha";
import * as apig_integrations from "@aws-cdk/aws-apigatewayv2-integrations-alpha";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class UnihackBackendStack extends Stack {
    constructor(scope: Construct, id: string, props?: StackProps) {
        super(scope, id, props);

        const DEFAULT_APPOINTMENT_TIME_MINS = "10";

        const queueTable = new dynamodb.Table(this, "UnihackQueueTable", {
            partitionKey: {
                name: "entryId",
                type: dynamodb.AttributeType.STRING,
            },
            sortKey: {
                name: "timeCreated",
                type: dynamodb.AttributeType.NUMBER,
            },
            billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
        });

        const createTaskFunction = new lambda.Function(
            this,
            "createTaskFunction",
            {
                runtime: lambda.Runtime.PYTHON_3_9,
                handler: "app.handler",
                code: lambda.Code.fromAsset("lib/src/createtask"),
                architecture: lambda.Architecture.ARM_64,
                environment: {
                    TABLE_NAME: queueTable.tableName,
                    APPOINTMENT_TIME: DEFAULT_APPOINTMENT_TIME_MINS,
                },
            }
        );
        queueTable.grantReadWriteData(createTaskFunction);

        const processTaskFunction = new lambda.Function(
            this,
            "processTaskFunction",
            {
                runtime: lambda.Runtime.PYTHON_3_9,
                handler: "app.handler",
                code: lambda.Code.fromAsset("lib/src/processtask"),
                architecture: lambda.Architecture.ARM_64,
                environment: {
                    TABLE_NAME: queueTable.tableName,
                    APPOINTMENT_TIME: DEFAULT_APPOINTMENT_TIME_MINS,
                },
            }
        );
        queueTable.grantReadWriteData(processTaskFunction);

        const getStatusFunction = new lambda.Function(
            this,
            "getStatusFunction",
            {
                runtime: lambda.Runtime.PYTHON_3_9,
                handler: "app.handler",
                code: lambda.Code.fromAsset("lib/src/getstatus"),
                architecture: lambda.Architecture.ARM_64,
                environment: {
                    TABLE_NAME: queueTable.tableName,
                    APPOINTMENT_TIME: DEFAULT_APPOINTMENT_TIME_MINS,
                },
            }
        );
        queueTable.grantReadData(getStatusFunction);

        const unihackAPI = new apig.HttpApi(this, "UnihackHTTPAPI");

        unihackAPI.addRoutes({
            integration: new apig_integrations.HttpLambdaIntegration(
                "createTaskIntegration",
                createTaskFunction
            ),
            path: "/createtask",
            methods: [apig.HttpMethod.POST],
        });

        unihackAPI.addRoutes({
            integration: new apig_integrations.HttpLambdaIntegration(
                "processTaskIntegration",
                processTaskFunction
            ),
            path: "/processtask",
            methods: [apig.HttpMethod.POST],
        });

        unihackAPI.addRoutes({
            integration: new apig_integrations.HttpLambdaIntegration(
                "getstatusintegration",
                getStatusFunction
            ),
            path: "/getstatus",
            methods: [apig.HttpMethod.GET],
        });

        // example resource
        // const queue = new sqs.Queue(this, 'UnihackBackendQueue', {
        //   visibilityTimeout: cdk.Duration.seconds(300)
        // });
    }
}
