#!/usr/bin/python
import click
import sys,datetime
sys.path.append("../lib")
from libcommotion import *

@click.group()
@click.option('--debug/--no-debug', default=False)

@click.pass_context
def cli(ctx, debug):
    click.clear()
    click.secho("Cowherd running...",fg="green")
    cowherd=ctx.obj

	
@cli.command()
@click.pass_context
def showconfig(ctx):
    cowherd.show_config()


@cli.command()
@click.pass_context
def createconfig(ctx):
    cowherd.create_config()

@cli.command()
@click.pass_context
def showconfig(ctx):
    cowherd.show_config()

@click.argument("user",nargs=1,default="root")
@click.argument("host",nargs=1)
@click.argument("command",nargs=1)

@cli.command()
@click.pass_context
def runremote(ctx,command,host,user):
	click.echo(click.style("Trying to run command ",fg="yellow")+click.style(command,fg="cyan")+click.style(" on host ",fg="yellow")+click.style(host,fg="green")+click.style(" as user ",fg="yellow")+click.style(user,fg="green"))
		
	op=cowherd.runremote(command,host,user) 
	click.echo(click.style("Output from host ",fg="yellow")+click.style(host,fg="green"))
	click.secho("---------------------------------------------------------------------",fg="yellow")
	click.echo(op)
	click.secho("---------------------------------------------------------------------",fg="yellow")
@click.argument("user",nargs=1,default="root")
@click.argument("host",nargs=1)

@cli.command()
@click.pass_context	
def testkeyauth(ctx,host,user):
	click.echo(click.style("Trying to log in with our key ",fg="yellow")+click.style(" to host ",fg="yellow")+click.style(host,fg="green")+click.style(" as user ",fg="yellow")+click.style(user,fg="green"))
	
	keyauth=cowherd.test_key_auth(host,user)
	if keyauth:
		click.secho("Key auth successful for %s as user %s" %(host,user),fg="green")
	else:
		print "Key auth failes for %s as users %s" %(host,user)

	
if __name__ == '__main__':
	cowherd=CommotionCOWHerd("~/cowherd.json")
	cli(obj=cowherd)
