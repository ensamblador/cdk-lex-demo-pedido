from aws_cdk import (
    RemovalPolicy,
    aws_dynamodb as ddb
)
from constructs import Construct


REMOVAL_POLICY = RemovalPolicy.DESTROY

TABLE_CONFIG = dict (removal_policy=REMOVAL_POLICY, billing_mode= ddb.BillingMode.PAY_PER_REQUEST)


class Tables(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        self.interactions = ddb.Table(
            self, "Interactions", 
            partition_key = ddb.Attribute(name="custID", type=ddb.AttributeType.STRING),
            sort_key = ddb.Attribute(name="ISODatetime", type=ddb.AttributeType.STRING),
            **TABLE_CONFIG)
        
        self.interactions.add_global_secondary_index(
            index_name='channel-index',
            partition_key=ddb.Attribute(name="channel", type=ddb.AttributeType.STRING),
        )
