##################
## Import Block ##
##################
import os
import fnmatch
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

####################
## Function Block ##
####################
def purge_toptordir(filePath):
    tmp_list = []
    for i in filePath:
        if os.environ.get('toptordir') not in i:
            tmp_list.append(i)
    return tmp_list

def find_files(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

#############################
## Client Connection Block ##
#############################
qbt_client = qbittorrentapi.Client(host=os.environ.get('qbhost'), port=os.environ.get('qbport'), VERIFY_WEBUI_CERTIFICATE=False, username=os.environ.get('qbuser'), password=os.environ.get('qbpasswd'))
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)
print(f'qBittorrent: {qbt_client.app.version}')
print(f'qBittorrent Web API: {qbt_client.app.web_api_version}\n\n')

## Prints a list of the torrent files found recursivly
## starting at the configured 'toptordir' variable dir.
print(f'Successfully Located The Following Torrent Files')
for i in find_files('*.torrent', os.environ.get('toptordir')):
    print(i)

#########################
## Adding Tor(s) Block ##
#########################
print(f'\n\nAdding Above Torrents To Staging Queue: Adds torrents to client in a paused state with categegory "staging"')
for tor in find_files('*.torrent', os.environ.get('toptordir')):
    conVar = qbt_client.torrents_add(torrent_files=tor, paused='true', category='staging', save_path=os.environ.get('qbstagingdir'))
    print("Processing: ", tor)
    if (conVar != 'Fails.'):
        print(f'{conVar} Added successfully!')
    else:
        print(f'{conVar}')
        print(f'{tor} FAILED to be added\n\n')


##########################
## Search && Seed Block ##
##########################
print(f'\n\nLocating Filepaths And Changing Save Path In Client: Creates array of newly added torrent hashes then set each save paths to where its respective files are located')
tors = qbt_client.torrents_info(category='staging')
for i in tors:
    torhash = i.hash
    torfile = qbt_client.torrents_files(torrent_hash=torhash)
    muliresult = False
    for k in range(len(torfile)):
        if (k == 0):   
            flname = torfile[k]["name"]
            print(flname) #prints filename of the first file of the tor
            ## Utilize 'locate' (shell function) to find where the file is located
            ## Make Sure To Reguarly Run 'sudo updatedb' To Maintain An Accurate Index
            flpath_blob = subprocess.run(["locate", "-b", f"\{flname}"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            flpath_list = flpath_blob.stdout.splitlines()
            flpath_list = purge_toptordir(flpath_list)
            if (flpath_blob.stdout == ''):
                print(f'{flname}\nERROR!!! ^Above File could not be found^')
                tors_lost.append(i)
            elif (len(flpath_list) > 1):
                print(f'more than one result found for: {flname}')
                tors_tmp.append(i)
                muliresult = True
            else:
                fnlength = len(flname)
                fplength = len(flpath_list[0])
                flpath = flpath_list[0][:fplength - (fnlength + 1)]
                print(f'filepath: {flpath}\nabsolute filename: {flpath_list[0]}\nfilepath length: {fplength}\nfilename length: {fnlength}')
                qbt_client.torrents_set_location(location=flpath, torrent_hashes=torhash)
                qbt_client.torrents_recheck(torrent_hashes=torhash)
                torstatus = qbt_client.torrents_info(torrent_hashes=torhash)
                print(torstatus)
        elif ((k == 1) and (muliresult == True)):
            flname = torfile[k]["name"]
            print(flname) #prints filename of the second file of the tor
            flpath_blob = subprocess.run(["locate", flname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            print(type('flpath_blob.stdout'))
            flpath_list = flpath_blob.stdout.splitlines()
            print(flpath_list)
        else:
            print(f'file#$k has been reached') # this is for third+ file of the tor
    print(f'\n')

print ("tors_tmp list contains: ")
for j in range(len(tors_tmp)):
    print (tors_tmp[j]["name"])
print(f'\n')
print ("tors_lost list contains: ")
for j in range(len(tors_lost)):
    print (tors_lost[j]["name"])

