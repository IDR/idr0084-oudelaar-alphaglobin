from omero.cli import CLI
from omero.gateway import BlitzGateway
import sys
import os


def printusage():
    print('''
Rename channel.

Usage: 
python set_channel_name.py [index (0 based)] [New Name] Project:[Project ID]

Only 'Project' data type supported at the moment.
          ''')
    sys.exit(1)


def rename(conn, project_id, channel_index, channel_name):
    project = conn.getObject("Project", project_id)
    for ds in project.listChildren():
        for img in ds.listChildren():
            channels = img.getChannels(noRE=True)
            lc = channels[channel_index].getLogicalChannel()
            lc.setName(channel_name)
            lc.save()


if len(sys.argv) < 4:
    printusage()
else:
    channel_index = int(sys.argv[1])
    channel_name = sys.argv[2]
    target = sys.argv[3].split(':')
    if target[0] == 'Project':
        project_id = int(target[1])
    else:
        printusage()


cli = CLI()
cli.loadplugins()
cli.onecmd('login -q')

try:
    conn = BlitzGateway(client_obj=cli.get_client())
    rename(conn, project_id, channel_index, channel_name)
finally:
    if cli:
        cli.close()
        conn.close()


