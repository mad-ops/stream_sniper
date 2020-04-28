import os
import argparse
import ffmpeg

scriptdir = os.path.dirname(os.path.abspath(__file__))
encode_path = os.path.join(scriptdir, "Videos", "encode_ready")
final_path = os.path.join(scriptdir, "Videos", "finished")
os.makedirs(encode_path, exist_ok=True)
os.makedirs(final_path, exist_ok=True)

parser = argparse.ArgumentParser(prog='Sniper',description='Snipe some streams.')
parser.add_argument('streamer', metavar='u/n', help='username, found in TTV URL')
args = parser.parse_args()

def file_to_encode( streamer ):
    tsfiles = [os.path.join(encode_path,f) for f in os.listdir(encode_path) if os.path.isfile(os.path.join(encode_path, f))]  
    return list(filter(lambda x: bool(streamer in x) & x.endswith("ts"), tsfiles))

def main( args ):
    vod = file_to_encode(args.streamer)[0]
    file_name = os.path.basename(vod)
    ffmpeg.input(vod).output(os.path.join(final_path, file_name)).run()
    return

if __name__ == "__main__":
    main(args)
