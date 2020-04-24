# This code is based on tutorial by slicktechies modified as needed to use oauth token from Twitch.
# You can read more details at: https://www.junian.net/2017/01/how-to-record-twitch-streams.html
# original code is from https://slicktechies.com/how-to-watchrecord-twitch-streams-using-livestreamer/

import time
import argparse
import streamlink

parser = argparse.ArgumentParser(prog='Sniper',description='Snipe some streams.')
parser.add_argument('streamer', metavar='u/n', help='username, found in TTV URL')
args = parser.parse_args()

def findUrl( streamer ):
    # Check for Livestream
    try:
        streams = streamlink.streams(f"https://www.twitch.tv/{ streamer }/")
    except:
        print("Stream not found.")
        return

    if "best" not in  streams:
        print("No URLs returned.")
        return

    return streams["best"]

def main( args ):
    url = findUrl(args.streamer)

    # I found this randomly, i don't know how to get the stream size from best
    # I should also confirm the size of a frame
    chunkSize = 1920 * 1080 *  3  # read length*width*3 bytes (= 1 frame)

    # lets only run for 30 minutes at a time -- cause im scared
    timeout_start = time.time()
    pretty_time = time.strftime("%Y-%m-%d-%H:%M")
    timeout = 30 * 60
    
    try:
        fd = url.open()
    except:
        print("Could not open stream.")
        return

    with open(f"{args.streamer}__{pretty_time}.ts", "wsb") as ts:
        while time.time() < timeout_start + timeout:
            data = fd.read(chunkSize)
            ts.write(data)

    fd.close

if __name__ == "__main__":
    main(args)

#oh shit use a lockfile so i don't dl and encode at the same time