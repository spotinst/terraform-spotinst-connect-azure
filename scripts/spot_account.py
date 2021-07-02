import time
import click
import json

from spotinst_sdk2 import SpotinstSession
from spotinst_sdk2.models.admin import *
from spotinst_sdk2.models.setup.azure import *

@click.group()
@click.pass_context
def cli(ctx, *args, **kwargs):
    ctx.obj = {}
    session = SpotinstSession()
    ctx.obj['client'] = session.client("admin")
    ctx.obj['client2'] = session.client("setup_azure")


@cli.command()
@click.argument('name')
@click.pass_context
def create(ctx, *args, **kwargs):
    """Create a new Spot Account"""
    account_name = "'" + kwargs.get('name') + "'"
    result = ctx.obj['client'].create_account(kwargs.get('name'))
    time.sleep(10)
    click.echo(json.dumps(result))


@cli.command()
@click.argument('account-id')
@click.pass_context
def delete(ctx, *args, **kwargs):
    """Delete a Spot Account"""
    try:
        response = ctx.obj['client'].delete_account(kwargs.get('account_id'))
        print(json.dumps(response))
    except:
        print("did not delete")
        print(json.dumps(response))


@cli.command()
@click.option('--account-id', required=True)
@click.option('--client-id', required=True)
@click.option('--client-secret', required=True)
@click.option('--tenant-id', required=True)
@click.option('--subscription-id', required=True)
@click.pass_context
def set_cloud_credentials(ctx, *args, **kwargs):
    """Set Azure credentials to Spot Account"""
    ctx.obj['client2'].account_id = kwargs.get('account_id')
    azurecredentials = AzureCredentials(kwargs.get('client_id'), kwargs.get('client_secret'), kwargs.get('tenant_id'), kwargs.get('subscription_id'))
    try:
        response = ctx.obj['client2'].set_credentials(azurecredentials)
        print(json.dumps(response))
    except:
        print(json.dumps(response))


@cli.command()
@click.option(
    '--filter',
    required=False,
    help='Return matching records. Syntax: key=value'
)
@click.option(
    '--attr',
    required=False,
    help='Return only the raw value of a single attribute'
)
@click.pass_context
def get(ctx, *args, **kwargs):
    """Returns ONLY the first match"""
    ctx.obj['client'].account_id = kwargs.get('account_id')
    result = ctx.obj['client'].get_accounts()
    if kwargs.get('filter'):
        k, v = kwargs.get('filter').split('=')
        result = [x for x in result if x[k] == v]
    if kwargs.get('attr'):
        if result:
            result = result[0].get(kwargs.get('attr'))
            click.echo(result)
    else:
        if result:
            click.echo(json.dumps(result[0]))


if __name__ == "__main__":
    cli()
