import logging
import re
from linkedin_api import Linkedin
from data.config import login, password

class IdGrabber:
    def __init__(self):
        self.parsed_ids = []
        logging.basicConfig(filename='IdGrabber',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

    def id_grabber(
            self,
            keywords=None,
            industries=None,
            location_name=None,
            listed_at=86400,
            limit=-1
            ):
        try:
            api = Linkedin(username=login, password=password)
            job_ids = (re.findall('\d+', job_id['dashEntityUrn'])[0] for job_id in api.search_jobs(
                                            keywords=keywords,
                                            industries=industries,
                                            location_name=location_name,
                                            listed_at=listed_at,
                                            limit=limit))
            return job_ids
        except Exception as Error:
            logging.exception(Error)