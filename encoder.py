#!/usr/app/venv/bin/python
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
    try:
        vod = file_to_encode(args.streamer)[0]
    except:
        print("No files for processing.")
        return

    file_name = os.path.splitext(os.path.basename(vod))[0]
    encoded_vod = os.path.join(final_path, file_name + ".mp4")

    try:
        ffmpeg.input(vod).output(encoded_vod).run()
    except:
        print(f"File not found @ {file_name}")
        return

    print("Raw enconded.")
    os.remove(vod)
    return

if __name__ == "__main__":
    main(args)
