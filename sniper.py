#!/usr/bin/env python
import os
import time
import argparse
import streamlink

parser = argparse.ArgumentParser(prog='Sniper',description='Snipe some streams.')
parser.add_argument('streamer', metavar='u/n', help='username, found in TTV URL')
args = parser.parse_args()

scriptdir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(scriptdir, "Videos", "in_progress"), exist_ok=True)
os.makedirs(os.path.join(scriptdir, "Videos", "encode_ready"), exist_ok=True)
encode_path = os.path.join(scriptdir, "Videos", "encode_ready")
capture_path = os.path.join(scriptdir, "Videos", "in_progress")

def findUrl( streamer ):
    # Check for Livestream
    try:
        streams = streamlink.streams(f"https://www.twitch.tv/{ streamer }/")
    except:
        print("Stream not found.")
        return

    if "best" not in streams:
        print("No URLs returned.")
        return

    return streams["best"]

def file_list( path ,  type ):
    onlyfiles = [os.path.join(path,f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]  
    return list(filter(lambda x: x.endswith(type) , onlyfiles))

def lock_encoder( streamer ):
    open(f"/tmp/encoder_{streamer}.lck", 'a').close()


def unlock_encoder( streamer ):
    try:
        os.remove(f"/tmp/encoder_{streamer}.lck")
    except:
        pass

    return

def ship_ts( streamer ):
    #should only return 1
    vods = [f for f in file_list(capture_path, ".ts") if streamer in f]
    pretty_time = time.strftime("%Y-%m-%d-%H")
    [os.rename(vod, os.path.join(encode_path, f"{args.streamer}_{pretty_time}.ts") ) for vod in vods]
    return

def main( args ):
    url = findUrl(args.streamer)

    # I found this randomly, i don't know how to get the stream size from best
    # I should also confirm the size of a frame
    chunkSize = 1920 * 1080 *  3  # read length*width*3 bytes (= 1 frame)

    # lets only run for 15 minutes at a time -- cause im scared
    timeout_start = time.time()
    timeout = 15
    
    try:
        fd = url.open()
    except:
        print("Could not open stream.")
        #Move file
        ship_ts(args.streamer)
        unlock_encoder(args.streamer)
        return

    ship_ts(args.streamer)

    print("Lock encoder.")
    lock_encoder(args.streamer)
    file_name = os.path.join(scriptdir, "Videos", "in_progress", f"{args.streamer}.ts")
    
    with open(file_name, "ab") as ts:
        while time.time() < timeout_start + timeout:
            data = fd.read(chunkSize)
            ts.write(data)

    fd.close
    print("Stream sniped.")

if __name__ == "__main__":
    main(args)
