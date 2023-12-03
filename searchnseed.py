##################
## Import Block ##
##################
import os
import fnmatch
import argparse
import qbittorrentapi
import subprocess
from dotenv import load_dotenv

##############################
#### -- Variable Block -- ####
##############################
load_dotenv()
tors = []
tors_bad = []
tors_lost = []
tors_tmp = []


###########################
## Helper Function Block ##
###########################
## Client Connection Function
#    Creates a client connection object
#    to the qbittorrent instance
def create_client():
    client_connection = qbittorrentapi.Client(
        host=os.environ.get("qbhost"),
        port=os.environ.get("qbport"),
        VERIFY_WEBUI_CERTIFICATE=False,
        username=os.environ.get("qbuser"),
        password=os.environ.get("qbpasswd"),
    )
    try:
        client_connection.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)
    print(f"qBittorrent: {client_connection.app.version}")
    print(f"qBittorrent Web API: {client_connection.app.web_api_version}\n\n")
    return client_connection


## Purge TopTorDir Function
#    sanatizes list to NOT include the .torrent file if
#    the filename is the same as the torrent file's name
def purge_toptordir(filePath):
    tmp_list = []
    for i in filePath:
        if os.environ.get("toptordir") not in i:
            tmp_list.append(i)
    return tmp_list


## Find Tor File(s) Function
#    Prints and returns a list of the torrent files found recursivly
#    starting at the configured 'toptordir' variable dir.
def find_files(pattern, path, args):
    tor_files = []
    print(f"Successfully Located The Following Torrent Files")
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                tor_files.append(os.path.join(root, name))
                print(os.path.join(root, name))
    return tor_files


## Staging Tor(s) Function
#    Staging Tor(s) To Be Added and tagged with "staging" category
def stage_torrents(torrents, qbt_client, args):
    if args.verbose:
        print(
            f'\n\nAdding Above Torrents To Client In A Paused State With Categegory "staging"'
        )
    for tor in torrents:
        bool_tor_added = qbt_client.torrents_add(
            torrent_files=tor,
            paused="true",
            category="staging",
            save_path=os.environ.get("qbstagingdir"),
        )
        if bool_tor_added != "Fails.":
            if args.verbose:
                print(f"{bool_tor_added} Successfully Added {tor}")
        else:
            print(f"{bool_tor_added}")
            print(f"{tor} FAILED to be added\n\n")


## Sub Proccess Call To Locate
#    Utilize 'locate' (shell function via sub-proccess call) to find where the file is
#    located Make Sure To Reguarly Run 'sudo updatedb' To Maintain An Accurate Index
def loacte_sub_call(file_name, args):
    file_path_List_blob = subprocess.run(
        ["locate", file_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    print(file_name)
    return file_path_List_blob


## Setter for Tor Save Location && Checking
#    Set's the save path where the file was found
#    within the client and rechecks
def tor_set_location(qbt_client, save_path, tor_hash, args):
    qbt_client.torrents_set_location(location=save_path, torrent_hashes=tor_hash)
    qbt_client.torrents_recheck(torrent_hashes=tor_hash)
    tor_state_info = qbt_client.torrents_info(torrent_hashes=tor_hash)
    return tor_state_info


## Find Files and Check Torrents Function
#    Search for file locations &&
#    Check Torrent within client
def find_and_check_tors(qbt_client, args):
    print(f"\n\nLocating Filepaths And Changing Save Path In Client")
    tors = qbt_client.torrents_info(category="staging")
    for tor in tors:
        tor_hash = tor.hash
        tor_filename_list = qbt_client.torrents_files(torrent_hash=tor_hash)
        muliresult = False
        for filename_count in range(len(tor_filename_list)):
            if filename_count == 0:
                file_name = tor_filename_list[filename_count]["name"]
                file_path_List_blob = loacte_sub_call(file_name, args)
                file_path_List = purge_toptordir(
                    file_path_List_blob.stdout.splitlines()
                )
                if file_path_List_blob.stdout == "":
                    if args.verbose:
                        print(f"{file_name}\nERROR!!! ^Above File could not be found^")
                    tors_lost.append(tor)
                elif len(file_path_List) > 1:
                    if args.verbose:
                        print(f"more than one result found for: {file_name}")
                    tors_tmp.append(tor)
                    muliresult = True
                else:
                    filename_length = len(file_name)
                    filepath_length = len(file_path_List[filename_count])
                    save_path = file_path_List[filename_count][
                        : filepath_length - (filename_length + 1)
                    ]
                    tor_state_info = tor_set_location(
                        qbt_client, save_path, tor_hash, args
                    )
                    if args.verbose:
                        print(
                            f"filepath: {save_path}\n"
                            f"absolute filepath: {file_path_List[filename_count]}\n"
                            f"filepath length: {filepath_length}\n"
                            f"filename length: {filename_length}\n"
                            f"{tor_state_info}"
                        )
            elif (filename_count == 1) and (muliresult == True):
                file_path_List_blob = loacte_sub_call(
                    tor_filename_list, filename_count, args
                )
                if args.verbose:
                    print(type("file_path_List_blob.stdout"))
                    file_path_List = file_path_List_blob.stdout.splitlines()
                    print(file_path_List)
            else:
                if args.verbose:
                    print(
                        f"file#{filename_count} has been reached"
                    )  # this is for third+ file of the tor
        print(f"\n")


###################
## Main Function ##
###################
def main():
    parser = argparse.ArgumentParser(
        description="Qbittorrent Staging-Helper/Autoseeder Script"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose mode"
    )
    args = parser.parse_args()

    qbt_client = create_client()
    torrent_files = find_files("*.torrent", os.environ.get("toptordir"), args)
    stage_torrents(torrent_files, qbt_client, args)
    find_and_check_tors(qbt_client, args)

    if args.verbose:
        if len(tors_tmp) >= 1:
            print("tors_tmp list contains: ")
            for j in range(len(tors_tmp)):
                print(tors_tmp[j]["name"])
            print(f"\n")
        if len(tors_lost) >= 1:
            print("tors_lost list contains: ")
            for j in range(len(tors_lost)):
                print(tors_lost[j]["name"])


if __name__ == "__main__":
    main()
