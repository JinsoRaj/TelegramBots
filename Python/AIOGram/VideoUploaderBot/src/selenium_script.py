import random
import os
import asyncio
import aiofiles

from __init__ import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class SeleniumScript:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TITLE_FILE_PATH = os.path.join(BASE_DIR, "text_files/titles.txt")
    DESCRIPTION_FILE_PATH = os.path.join(BASE_DIR, "text_files/descriptions.txt")
    TAGS_FILE_PATH = os.path.join(BASE_DIR, "text_files/tags.txt")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def get_element_location_by_selector(self, selector):
        """
        Finds an element by its CSS selector.

        Args:
            selector (str): The CSS selector of the element.

        Returns:
            WebElement: The WebElement if found, otherwise False.
        """

        try:
            element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            logger.info(f"Element with selector: {selector} found")
            return element
        except (NoSuchElementException, TimeoutException):
            logger.error(f"Element with selector: {selector} wasn't found")
            return False

    def get_element_location_by_id(self, element_id):
        """
        Finds an element by its ID.

        Args:
            element_id (str): The ID of the element.

        Returns:
            WebElement: The WebElement if found, otherwise False.
        """

        try:
            element = self.wait.until(EC.presence_of_element_located((By.ID, element_id)))
            logger.info(f"Element with id: {element_id} found")
            return element
        except (NoSuchElementException, TimeoutException):
            logger.error(f"Element with id: {element_id} wasn't found")
            return False

    def get_element_location_by_class(self, element_class):
        """
        Finds an element by its class name.

        Args:
            element_class (str): The class name of the element.

        Returns:
            WebElement: The WebElement if found, otherwise False.
        """

        try:
            element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, element_class)))
            logger.info(f"Element with class name: {element_class} found")
            return element
        except (NoSuchElementException, TimeoutException):
            logger.error(f"Element with class name: {element_class} wasn't found")
            return False

    def get_element_location_by_xpath(self, xpath):
        """
        Finds an element by its XPath.

        Args:
            xpath (str): The XPath of the element.

        Returns:
            WebElement: The WebElement if found, otherwise False.
        """

        try:
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            logger.info(f"Element with XPath: {xpath} found")
            return element
        except (NoSuchElementException, TimeoutException):
            logger.error(f"Element with XPath: {xpath} wasn't found")
            return False

    async def _break_between_actions(self):
        """
        Pauses the execution for a random period between 2 and 4 seconds.
        """
        await asyncio.sleep(random.randint(2, 4))

    async def _sendkeys_break(self):
        """
        Pauses the execution for a random period between 0.5 and 1 second.
        """
        await asyncio.sleep(random.uniform(0.5, 1.0))

    async def _auto_text_paste(self, text, textbox):
        """
        Automatically pastes text into a textbox by typing each character with a delay.

        Args:
            text (str): The text to be typed into the textbox.
            textbox (WebElement): The textbox WebElement where the text will be entered.
        """

        for symbol in text:
            await asyncio.to_thread(textbox.send_keys, symbol)
            await self._sendkeys_break()

    async def _read_lines_from_file(self, file_path):
        """
        Reads lines from a file asynchronously.

        Args:
            file_path (str): The path to the file.

        Returns:
            list: A list of lines from the file.
        """

        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            lines = await f.readlines()
            return [line.strip() for line in lines]

    async def _choose_random_line(self, file_path):
        """
        Chooses a random line from a file asynchronously.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: A random line from the file.
        """

        lines = await self._read_lines_from_file(file_path)
        random_line = random.choice(lines)
        return random_line.strip()

    async def _get_random_title(self):
        """
        Gets a random title from the titles file.

        Returns:
            str: A random title from the file.
        """

        return await self._choose_random_line(self.TITLE_FILE_PATH)

    async def _get_random_description(self):
        """
        Gets a random description from the descriptions file.

        Returns:
            str: A random description from the file.
        """

        return await self._choose_random_line(self.DESCRIPTION_FILE_PATH)

    async def _get_random_tags(self):
        """
        Gets a random set of tags from the tags file.

        Returns:
            str: A random set of tags from the file.
        """

        return await self._choose_random_line(self.TAGS_FILE_PATH)

    async def _scroll_to_element(self, element):
        """
        Scrolls the page to bring the specified element into view.

        Args:
            element (WebElement): The element to scroll to.
        """

        await asyncio.to_thread(self.driver.execute_script, "arguments[0].scrollIntoView();", element)
        await self._break_between_actions()

    async def upload_video(self, video_path):
        """
        Automates the video upload process to YouTube, filling in title, description, tags, etc.

        Args:
            video_path (str): The path to the video file to upload.

        Returns:
            bool: True if the video was successfully uploaded, otherwise False.
        """

        await asyncio.to_thread(self.driver.get, 'https://www.youtube.com/upload')
        await self._break_between_actions()

        select_files_button = await asyncio.to_thread(self.get_element_location_by_selector, 'input[type="file"]')
        if not select_files_button:
            return False

        await asyncio.to_thread(select_files_button.send_keys, str(video_path))
        await self._break_between_actions()

        title_textbox = await asyncio.to_thread(self.get_element_location_by_xpath,
                                                 '//div[@class="input-container title style-scope ytcp-video-metadata-editor-basics"]//*[@id="textbox"]')
        if not title_textbox:
            return False

        # await self.random_move_and_click(title_textbox)
        await asyncio.to_thread(title_textbox.click)

        for i in range(0, len(title_textbox.text)):
            await asyncio.to_thread(title_textbox.send_keys, Keys.BACKSPACE)
            await self._sendkeys_break()

        title = await self._get_random_title()
        await self._auto_text_paste(title, title_textbox)

        await self._break_between_actions()

        description_textbox = await asyncio.to_thread(self.get_element_location_by_xpath,
                                                      '//div[@class="input-container description style-scope ytcp-video-description"]//*[@id="textbox"]')
        if not description_textbox:
            return False

        await asyncio.to_thread(description_textbox.click)
        description = await self._get_random_description()
        await self._auto_text_paste(description, description_textbox)

        await self._break_between_actions()

        radio_not_for_kids_button = await asyncio.to_thread(self.get_element_location_by_xpath,
                                                            '//*[@name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]//*[@id="radioContainer"]')
        if not radio_not_for_kids_button:
            return False

        await self._scroll_to_element(radio_not_for_kids_button)
        await asyncio.to_thread(radio_not_for_kids_button.click)

        await self._break_between_actions()

        show_more_button = await asyncio.to_thread(self.get_element_location_by_xpath,
                                                   '//*[@class="toggle-section style-scope ytcp-video-metadata-editor"]//*[@id="toggle-button"]')
        if not show_more_button:
            return False

        await asyncio.to_thread(show_more_button.click)

        await self._break_between_actions()

        tags_button = await asyncio.to_thread(self.get_element_location_by_xpath,
                                              '//*[@id="tags-container"]//*[@id="text-input"]')
        if not tags_button:
            return False

        await self._scroll_to_element(tags_button)
        await asyncio.to_thread(tags_button.click)
        tags = await self._get_random_tags()
        await self._auto_text_paste(tags, tags_button)

        await self._break_between_actions()

        language_select_button = await asyncio.to_thread(self.get_element_location_by_xpath,
                                                         '//*[@id="language-input"]//*[@id="right-icon"]')
        if not language_select_button:
            return False

        await asyncio.to_thread(language_select_button.click)

        await self._break_between_actions()

        english_pick = await asyncio.to_thread(self.get_element_location_by_xpath,
                                               '//*[@id="paper-list"]//*[normalize-space(text())="English (United States)"]')
        if not english_pick:
            return False

        await self._scroll_to_element(english_pick)
        await asyncio.to_thread(english_pick.click)

        await self._break_between_actions()

        next_button = await asyncio.to_thread(self.get_element_location_by_xpath,
                                              '//*[@id="next-button"]//*[@class="yt-spec-touch-feedback-shape yt-spec-touch-feedback-shape--touch-response-inverse"]')
        if not next_button:
            return False

        await asyncio.to_thread(next_button.click)

        await self._break_between_actions()

        await asyncio.to_thread(next_button.click)

        await self._break_between_actions()

        await asyncio.to_thread(next_button.click)

        await self._break_between_actions()

        public_privacy_button = await asyncio.to_thread(self.get_element_location_by_xpath,
                                                        '//*[@id="privacy-radios"]//*[@name="PUBLIC"]')
        if not public_privacy_button:
            return False

        await asyncio.to_thread(public_privacy_button.click)

        await self._break_between_actions()

        publish_button = await asyncio.to_thread(self.get_element_location_by_xpath,
                                                 '//*[@id="done-button"]//*[@aria-label="Publish"]')
        if not publish_button:
            return False

        await asyncio.to_thread(publish_button.click)

        await self._break_between_actions()

        close_button = await asyncio.to_thread(self.get_element_location_by_xpath,
                                               '//*[@id="close-button"]//*[@aria-label="Close"]')
        if not close_button:
            return False

        await asyncio.to_thread(close_button.click)

        self.driver.quit()

        return True
