import logging
import re
from linkedin_api import Linkedin
from data.config import login, password


class DictGrabber:
    def __init__(self):
        self.parsed_ids = []
        logging.basicConfig(filename='DictGrabber',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

    def dict_grabber(
            self,
            keywords=None,
            location_name=None,
            listed_at=86400,
            limit=-1
    ):
        try:
            job_dicts = []
            api = Linkedin(username=login, password=password)
            temp_dicts = api.search_jobs(keywords=keywords,
                                         location_name=location_name,
                                         listed_at=listed_at,
                                         limit=limit)
            for temp_dict in temp_dicts:
                try:
                    salary = temp_dict['salaryInsights']['compensationBreakdown']
                except:
                    salary = [{
                        'minSalary': '0',
                        'maxSalary': '0'
                    }]

                try:
                    job_dicts.append({
                        'location': temp_dict['formattedLocation'],
                        'title': temp_dict['title'],
                        'listedAt': temp_dict['listedAt'],
                        'id': re.findall('\d+', temp_dict['dashEntityUrn'])[0],
                        'minSalary': salary[0]['minSalary'],
                        'maxSalary': salary[0]['maxSalary']
                    })
                except Exception as Error:
                    logging.exception(Error)
            return job_dicts
        except Exception as Error:
            logging.exception(Error)
