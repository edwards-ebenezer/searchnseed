# searchnseed
Script for finding, checking and seeding files through qbittorrent (Helpful post-format utility)

## Requirememnts:
  Linux

  python3

  pip3

  dotenv

  qbittorrentapi

  locate

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



## Notes
Currently this script utilizes 'locate' (shell function through subprocess call) to find where the file(s) are located.<br/>
Thus make sure to **regularly** run 'sudo updatedb' to maintain an accurate index.
