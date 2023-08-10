from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from yt_stickers_backup.exceptions import *
import os
import requests

class YTStickersBackup:
    def __init__(self, user_profile_dir: str = None) -> None:
        options = Options()
        options.add_argument(f"--user-data-dir={user_profile_dir}")
        options.add_argument("--disable-extensions")
        options.add_argument('--headless')
        self.__driver = webdriver.Chrome(options=options)
        self.__driver.get("about:blank")

    def close(self) -> None:
        self.__driver.quit()

    def get_badges_and_stickers(self, channel_handle: str) -> tuple[str, list[dict]]:
        if not channel_handle.startswith("@"):
            channel_handle = "@" + channel_handle
        try:
            self.__driver.get(f"https://www.youtube.com/{channel_handle}")
            try:
                sponsor_button = self.__driver.find_element(By.ID, "sponsor-button")
            except NoSuchElementException:
                raise ChannelNotFoundError(channel_handle)

            try:
                sponsor_button.click()
            except ElementNotInteractableException:
                raise SponsorIsNotActivatedError(channel_handle)

            try:
                sponsor_renderer_element = WebDriverWait(self.__driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "ytd-sponsorships-offer-renderer")))
            except TimeoutException:
                raise SponsorTierLoadError()
            
            channel_name = self.__driver.find_element(By.ID, "channel-name").find_element(By.TAG_NAME, "yt-formatted-string").text
            
            scrollable_element = sponsor_renderer_element.find_element(By.ID, "scrollable")
            self.__driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollable_element)
            
            badges_and_stickers_elements = sponsor_renderer_element.find_element(By.ID, "tier").find_elements(By.TAG_NAME, "img")

            result = []

            for badges_and_stickers_element in badges_and_stickers_elements:
                result.append({
                        "title": badges_and_stickers_element.get_attribute("alt"),
                        "url": badges_and_stickers_element.get_attribute("src").rsplit("=", 1)[0]
                    })

            return channel_name, result

        finally:
            self.__driver.get("about:blank")
        
    def download(self, download_roor_dir:str, title_url_pair_dict_list: list) -> None:
        download_roor_dir = download_roor_dir.replace("\\", "/").rstrip("/")

        os.makedirs(download_roor_dir, exist_ok=True)

        for dl_info in title_url_pair_dict_list:
            with requests.get(dl_info["url"]) as req:
                download_path = f"{download_roor_dir}/{dl_info['title']}.png"
                already_exist_count = 0
                while os.path.isfile(download_path):
                    already_exist_count += 1
                    download_path = f"{download_roor_dir}/{dl_info['title']} ({already_exist_count}).png"
                with open(download_path, mode="wb") as f:
                    f.write(req.content)