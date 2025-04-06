from aiogram_dialog.api.entities import MediaAttachment


class NeedUpdate(Exception):
    def __init__(self, media_id: str, media_attachment: MediaAttachment | None = None):
        self.message = "Had to unload the media, so update it!"
        self.media_id = media_id
        self.media_attachment = media_attachment
