import bclient as bclient
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-a", "--alert", dest="alert", help="Alert Number", metavar="ALERT", default="5")
args = vars(parser.parse_args())

client = bclient.sockClient("hacweb7")
client.sendPacket(args["alert"])
