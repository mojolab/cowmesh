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

@cli.command()
@click.pass_context
def getclientsforgw(ctx,host,user):
    leases=cowherd.gw_get_dhcp_leases(host,user)
    print get_color_json(leases)

@cli.command()
@click.pass_context
def updategwhostnames(ctx):
    cowherd.update_gw_hostnames()

@cli.command()
@click.pass_context
def updategwroutes(ctx):
    cowherd.update_gw_routes()


@cli.command()
@click.pass_context
def updategwleases(ctx):
    cowherd.update_gw_leases()

@cli.command()
@click.pass_context
def updategwcommotion(ctx):
    cowherd.update_gw_commotion()

@cli.command()
@click.pass_context
def getpeergateways(ctx):
    cowherd.get_peer_gateways()

@cli.command()
@click.pass_context
def getnumclients(ctx):
    cowherd.get_numclients()

@cli.command()
@click.pass_context
def getclientreport(ctx):
    cowherd.get_client_report()


@click.option('--cont', is_flag=True)

@cli.command()
@click.pass_context
def buildtree(ctx,cont):
    cowherd.build_tree()
    if cont:
		while True:
			cowherd.create_config()
			cowherd.build_tree()

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
		click.secho("Key auth failes for %s as users %s" %(host,user),fg="red")

	
if __name__ == '__main__':
	cowherd=CommotionCOWHerd("~/cowherd.json")
	cli(obj=cowherd)
