from yt_stickers_backup.core import YTStickersBackup
from yt_stickers_backup.exceptions import ChannelNotFoundError, SponsorIsNotActivatedError
import argparse

parser = argparse.ArgumentParser(description="Supports command-line arguments.")
parser.add_argument("--user-profile-dir", "-u", dest="user_profile_dir", type=str, help="Directory path of a Chrome user profile (logged in to YouTube)")
parser.add_argument("--channel-handles", "-c", dest="channel_handles", type=str, help="Specify the channel handle (e.g. @YTStickersBackup,@YTStickersBackupSub)")
parser.add_argument("--download-root-dir", "-d", dest="download_root_dir", type=str, help="Specify the download root directory path (e.g. ./downloads)")
args = parser.parse_args()
    
if args.user_profile_dir == None:
    user_profile_dir = input("Please enter directory path of a Chrome user profile (logged in to YouTube) e.g. C:\\Users\\Rilm2525\\AppData\\Local\\Google\\Chrome\\User Data: ")
else:
    user_profile_dir = args.user_profile_dir

if args.channel_handles == None:
    channel_handles = input("Please enter your Channel Handle. e.g. @YTStickersBackup: ")
else:
    channel_handles = args.channel_handles

if args.download_root_dir == None:
    download_root_dir = input("Please enter path of download root directory. e.g. ./downloads: ")
else:
    download_root_dir = args.download_root_dir
download_root_dir = download_root_dir.replace("\\", "/").rstrip("/")

ytsb = YTStickersBackup(user_profile_dir=user_profile_dir)

for channel_handle in channel_handles.split(","):
    channel_name, badges_and_stickers = ytsb.get_badges_and_stickers(channel_handle)
    ytsb.download(f"{download_root_dir}/{channel_name}", badges_and_stickers)

ytsb.close()