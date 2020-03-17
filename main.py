from api import *
import argparse
parser=argparse.ArgumentParser(description='Download pictures from webpage')

parser.add_argument('link',type=str,help='The webpage to download')
parser.add_argument('-p','--save_dir',default='./save',type=str,help='The directory to save images. Default "./save"')
parser.add_argument(
    '-ms','--min_size',type=float,default=20,
    help='The minimum size of images. Default 20. All pictures whose size is below min_size will not be downloaded'
)
parser.add_argument('-v','--verbose',type=str,default=True,help='Whether to show information in the process')

args = parser.parse_args()
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Unsupported value encountered.')
verbose=str2bool(args.verbose)


d=download()
d.setting(
    url=args.link,
    save_dir=args.save_dir,
    min_size=args.min_size,
    verbose=verbose,
)
d.main()
