from typing import List

class VideoMetadata:
    """
    A class to store metadata about a TikTok video including job and creator information.
    """
    def __init__(
            self,
            job_title: str,
            video_url: str,
            video_title: str,
            creator_url: str,
            creator_contact_info: List[str],
            downloadable_video_url: str
            ) -> None:
        self.job_title: str = job_title
        self.video_url: str = video_url
        self.video_title: str = video_title
        self.creator_url: str = creator_url
        self.creator_contact_info: List[str] = creator_contact_info
        self.downloadable_video_url = downloadable_video_url

    def __str__(self):
        return f"job_title='{self.job_title}',\nvideo_url='{self.video_url}',\nvideo_title='{self.video_title}',\ncreator_url='{self.creator_url}',\ncreator_contact_info={self.creator_contact_info},\ndownloadable_video_url={self.downloadable_video_url}\n"
