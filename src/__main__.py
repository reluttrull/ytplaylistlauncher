from ytmusicapi import YTMusic
from random import randint # for -r mode
import webbrowser
import sys
import os # for colors on windows
from termcolor import colored

def main():
    os.system('color')
    if len(sys.argv) < 2: # prompt mode (e.g. ytplaylistlauncher)
        search = input("What kind of music do you want to listen to? ")
        search_playlists(search)
    elif sys.argv[1] in ["-h", "--help"]:
        show_help()
    else:
        search = sys.argv[1]
        search_playlists(search)
        
def show_help():
    print("Usage: ytplaylistlauncher [keywordtosearchnospaces] [OPTIONS]")
    print("")
    print("Examples:")
    print("ytplaylistlauncher chill")
    print("     gives you five random YT music playlists found with the keyword \"chill\" to choose from")
    print("ytplaylistlauncher party -r")
    print("     opens a random YT music playlist found with the keyword \"party\"")
    print("")
    print("Options:")
    print("-h, --help     Show this message")
    print("-r             Open a random playlist based on the specified search term")
        
def search_playlists(search):
    playlisturlprefix = "https://music.youtube.com/playlist?list="
    singleurlprefix = "https://www.youtube.com/watch?v="
    ytmusic = YTMusic()
    print("...Loading options...")
    limit = 5
    playlists = ytmusic.search(query=search, filter="playlists")
    randomStart = randint(0, len(playlists)-limit-1)
    top_playlists = playlists[randomStart:randomStart+limit]
    if len(sys.argv) >= 3 and sys.argv[2] == "-r": # random mode (e.g. ytplaylistlauncher chill -r)
        index = randint(0, len(top_playlists)-1 if len(top_playlists) < limit else limit)
    else: # standard mode (e.g. ytplaylistlauncher workout)
        for i in range(0,5):    
            t = ytmusic.get_playlist(top_playlists[i]["browseId"])["tracks"][0]
            if i%2==0: clr = "light_blue" 
            else: clr = "light_red"
            print(colored("[{}] \"{}\"".format(i+1, top_playlists[i]["title"]), clr))
            print("    " + colored("p1. \"{}\" by {}".format(t["artists"][0]["name"], t["title"]), clr))
        userIndex = input("Which one sounds best?  Select your number 1-{}: ".format(limit))
        if userIndex.isdigit():
            index = int(userIndex)-1
        else:
            index = -1 # force error safely
    if index >= 0 and index < limit:
        top_playlist_id = top_playlists[index]["browseId"]
        top_playlist = ytmusic.get_playlist(top_playlist_id)
        print("...Loading webpage...")
        webbrowser.open_new(playlisturlprefix+top_playlist["id"])
    else:
        print("Index not in range.  Do better next time and follow directions!")
if __name__ == "__main__":
    main()