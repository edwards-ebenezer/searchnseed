# searchnseed
Script for finding, checking and seeding files through qbittorrent (Helpful post-format utility)

## Requirememnts:
  Linux/locate

  python3

  pip3

  dotenv

  qbittorrentapi

## Install Instructions

### Manjaro 
    yay -Syu
    yay -Syu python-pip locate
    pip install --upgrade pip 
    pip install pip-tools
    pip install python-dotenv
    pip install qbittorrent-api


### Ubuntu && Ubuntu based distros
    sudo apt update 
    sudo apt install python3-pip locate
    pip3 install --upgrade pip 
    pip3 install pip-tools
    pip3 install python-dotenv
    pip3 install qbittorrent-api


## Usage
Copy the example environment file to .env and set values as needed

    cp env.example .env
    vim .env

Download, or move, all your *.torrent* files into the directory you set the ***toptordir*** variable to.<br/>
Update the searchable index, add the execute bit, run script 

    sudo updatedb
    chmod u+x searchnseed.py
    python3 searchnseed.py

    qBittorrent: v4.4.3.1
    qBittorrent Web API: 2.8.5


    Successfully Located The Following Torrent Files
    /home/user/Downloads/Tors/tmp/debian-11.4.0-amd64-netinst.iso.torrent
    /home/user/Downloads/Tors/tmp/linuxmint-21-cinnamon-64bit-beta.iso.torrent


    Adding Above Torrents To Staging Queue: Adds torrents to client in a paused state with categegory "staging"
    Processing:  /home/user/Downloads/Tors/tmp/debian-11.4.0-amd64-netinst.iso.torrent
    Ok. Added successfully!
    Processing:  /home/user/Downloads/Tors/tmp/linuxmint-21-cinnamon-64bit-beta.iso.torrent
    Ok. Added successfully!


    Locating Filepaths And Changing Save Path In Client: Creates array of newly added torrent hashes then set each save paths to where its respective files are located
    linuxmint-21-cinnamon-64bit-beta.iso
    filepath: /home/user/TMP
    absolute filename: /home/user/TMP/linuxmint-21-cinnamon-64bit-beta.iso
    filepath length: 61
    filename length: 36
    [AttrDict({'added_on': 1658343710, 'amount_left': 2438285312, 'auto_tmm': False, 'availability': 0, 'category': 'staging', 'completed': 0, 'completion_on': 18000, 'content_path': '/home/user/TMP/linuxmint-21-cinnamon-64bit-beta.iso', 'dl_limit': -1, 'dlspeed': 0, 'download_path': '', 'downloaded': 0, 'downloaded_session': 0, 'eta': 8640000, 'f_l_piece_prio': False, 'force_start': False, 'hash': '5d245b7dd411a2a7f7715357ccfaa08f31862546', 'infohash_v1': '5d245b7dd411a2a7f7715357ccfaa08f31862546', 'infohash_v2': '', 'last_activity': 1658343710, 'magnet_uri': 'magnet:?xt=urn:btih:5d245b7dd411a2a7f7715357ccfaa08f31862546&dn=linuxmint-21-cinnamon-64bit-beta.iso&tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce', 'max_ratio': -1, 'max_seeding_time': -1, 'name': 'linuxmint-21-cinnamon-64bit-beta.iso', 'num_complete': 0, 'num_incomplete': 0, 'num_leechs': 0, 'num_seeds': 0, 'priority': 2, 'progress': 0, 'ratio': 0, 'ratio_limit': -2, 'save_path': '/home/user/TMP', 'seeding_time': 0, 'seeding_time_limit': -2, 'seen_complete': 18000, 'seq_dl': False, 'size': 2438285312, 'state': 'checkingResumeData', 'super_seeding': False, 'tags': '', 'time_active': 0, 'total_size': 2438285312, 'tracker': '', 'trackers_count': 1, 'up_limit': -1, 'uploaded': 0, 'uploaded_session': 0, 'upspeed': 0})]


    debian-11.4.0-amd64-netinst.iso
    filepath: /home/user/Downloads
    absolute filename: /home/user/Downloads/debian-11.4.0-amd64-netinst.iso
    filepath length: 62
    filename length: 31
    [AttrDict({'added_on': 1658343710, 'amount_left': 397410304, 'auto_tmm': False, 'availability': 0, 'category': 'staging', 'completed': 0, 'completion_on': 18000, 'content_path': '/home/user/Downloads/debian-11.4.0-amd64-netinst.iso', 'dl_limit': -1, 'dlspeed': 0, 'download_path': '', 'downloaded': 0, 'downloaded_session': 0, 'eta': 8640000, 'f_l_piece_prio': False, 'force_start': False, 'hash': 'cc5bf72c0db84e2de95f967954441c017c5a3631', 'infohash_v1': 'cc5bf72c0db84e2de95f967954441c017c5a3631', 'infohash_v2': '', 'last_activity': 1658343710, 'magnet_uri': 'magnet:?xt=urn:btih:cc5bf72c0db84e2de95f967954441c017c5a3631&dn=debian-11.4.0-amd64-netinst.iso&tr=http%3a%2f%2fbttracker.debian.org%3a6969%2fannounce', 'max_ratio': -1, 'max_seeding_time': -1, 'name': 'debian-11.4.0-amd64-netinst.iso', 'num_complete': 0, 'num_incomplete': 0, 'num_leechs': 0, 'num_seeds': 0, 'priority': 2, 'progress': 0, 'ratio': 0, 'ratio_limit': -2, 'save_path': '/home/user/Downloads', 'seeding_time': 0, 'seeding_time_limit': -2, 'seen_complete': 18000, 'seq_dl': False, 'size': 397410304, 'state': 'checkingResumeData', 'super_seeding': False, 'tags': '', 'time_active': 0, 'total_size': 397410304, 'tracker': '', 'trackers_count': 1, 'up_limit': -1, 'uploaded': 0, 'uploaded_session': 0, 'upspeed': 0})]


    tors_tmp list contains: 


    tors_lost list contains: 
    [Finished in 246ms]



## Notes
Currently this script utilizes 'locate' (shell function through subprocess call) to find where the file(s) are located.<br/>
Thus make sure to **regularly** run 'sudo updatedb' to maintain an accurate index.
