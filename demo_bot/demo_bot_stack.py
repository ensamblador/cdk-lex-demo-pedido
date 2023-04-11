from aws_cdk import (
    # Duration,
    Stack,
    aws_connect as connect,
    aws_secretsmanager as secretsmanager,SecretValue,
)
from constructs import Construct
from lambdas import Lambdas
from databases import Tables
from bots import (LexBotV2, LexBotV2Multi, S3BotFiles)

class DemoBotStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, secrets, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        instance_arn = secrets['INSTANCE_ARN']
    
        region = self.region
        account = self.account

        Tbl = Tables(self, 'Tbl')
        Fn  = Lambdas(self,'Fn')
        _bot_files = S3BotFiles(self, "Files", "./bots/bot_files")

        demo_bot = LexBotV2(self, "BotDemo", "demo", Fn.code_hook_demo, "demo-pedido.zip", _bot_files)        

        Fn.code_hook_demo.add_environment(key="INTERACCIONES_TABLE",value = Tbl.interactions.table_name)
        Tbl.interactions.grant_full_access(Fn.code_hook_demo)

        bot_integration_arn = f"arn:aws:lex:{region}:{account}:bot-alias/{demo_bot.bot.attr_id}/TSTALIASID"

        connect.CfnIntegrationAssociation(self, "BotIntegrationAgendar",
            instance_id=instance_arn,
            integration_type="LEX_BOT",
            integration_arn=bot_integration_arn
        )

        secrets = secretsmanager.Secret(self, "Secrets", secret_name= 'lex_bot_demo',
                                        secret_object_value = {
            'BOT_ID': SecretValue.unsafe_plain_text(demo_bot.bot.attr_id),
            'BOT_NAME': SecretValue.unsafe_plain_text(demo_bot.bot.name)
            })
