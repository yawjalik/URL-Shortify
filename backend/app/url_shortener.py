# Methods for URL shortening (credits to chkhong)

from db import Database
from utils.HashIds import HashIds
from utils.OutputHandler import std_content
from loguru import logger
import traceback
from typing import Tuple, Dict
import urllib.request

class URLShortener:
    def __init__(self, db:Database=None, hostname:str=""):
        logger.debug("Initializing URLShortener class")
        self.db = db
        self.hostname = hostname

    def shorten(self, args:dict, hashids:HashIds) -> Tuple[int, Dict[str,dict]]:
        """ Takes a long url and return the shortened url
    
        Args:
            args (dict): dictionary of arguments
            hashids (Hashids): hashids object
        Returns:
            status_code (int): status code of the response
            content (std_content): response object containing hash
        """
        logger.info("="*100)
        logger.info("shorten() running...")
        status_code = 500
        content = std_content()

        try:
            original_url = args['url'].strip()
            if not original_url:
                status_code = 400
                content['message'] = 'Original URL input is blank'
                content['data'] = {}
            elif self.validate_url(original_url) == "":
                status_code = 400
                content['message'] = 'Invalid URL'
                content['data'] = {}
            else:
                hash = self.find_matching_hash(original_url)
                if not hash:
                    status_code = 201
                    hash = self.insert(hashids, original_url)
                shortened_url = f"http://{self.hostname}/{hash}"
                status_code = 200
                content['data'] = {'original_url': original_url, 'shortened_url': shortened_url}
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
        finally:
            return status_code, content

    def insert(self, hashids:HashIds, original_url:str) -> str:
        """ Insert original url and shortened url into database and returns generated hash
        
        Args:
            hashids (Hashids): hashids object
            ori (str): original url
        Returns:
            hash (str): generated hash
        """
        logger.info("-"*100)
        logger.info("insert() running...")
        hash = ""

        try:
            rows = self.db.execute('INSERT INTO url(shortened_url, original_url) VALUES(%s, %s)', ('', original_url))
            last_id = self.db.retrieve('SELECT LAST_INSERT_ID()')[0]['LAST_INSERT_ID()']
            hash = hashids.encode(last_id)
            rows2 = self.db.execute('UPDATE url SET shortened_url=%s WHERE id=%s', (hash, last_id))
            rows3 = self.db.execute("INSERT INTO url_stats(shortened_url, time_accessed, datetime_created) VALUES (%s, '', now())", hash)
            rows = rows and rows2 and rows3
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
        finally:
            return hash

    def retrieve(self, hash:str) -> str:
        """ Retrieve original URL by hash

        Args:
            hash (str): hash of the shortened URL
        Returns:
            result (str): string of the original URL
        """
        logger.info("-"*100)
        logger.info("retrieve() running...")
        result = ""

        try:
            res = self.db.retrieve('SELECT original_url FROM url WHERE shortened_url = %s', hash)
            if res:
                result = res[0]['original_url']
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
        finally:
            return result

    def validate_url(self, url:str) -> str: # copypasted
        """ validate url

        Args:
            url (str): url to be validated
        Returns:
            url (str): un/edited url if valid, nothing if invalid
        """

        logger.info("-"*100)
        logger.info("validate_url() running...")
        valid_url = ""

        try:
            if url[0:7] != "http://" and url[0:8] != "https://":
                prefixes = ["http://", "http://www.", "https://", "https://www."]
                for prefix in prefixes:
                    test_url = prefix + url
                    if urllib.request.urlopen(test_url).getcode() == 200: # test url
                        valid_url = test_url
                        break
            elif urllib.request.urlopen(url).getcode() == 200: # test original url
                valid_url = url
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
        finally:
            return valid_url

    def url_access(self, hash:str) -> None:
        """ Update time_accessed on url_stats table 
            Args:
                hash (str): hash of the shortened URL
        """
        logger.info("-"*100)
        logger.info("url_access() running...")
        new_res = ""
        try:
            sql_now = self.db.retrieve('SELECT now()')[0]['now()']
            curr_datetime = sql_now.strftime("%d/%m/%Y %H:%M:%S")
            res = self.db.retrieve('SELECT time_accessed FROM url_stats WHERE shortened_url = %s', hash)
            if not res[0]['time_accessed']:
                new_res = curr_datetime
            else:
                new_res = res[0]['time_accessed'] + '@' + curr_datetime
            self.db.execute('UPDATE url_stats SET time_accessed = %s WHERE shortened_url = %s', (new_res, hash))
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())

    def find_matching_hash(self, url:str) -> str:
        """find matching hash value if original url exist
            Args:
                url (str): original url
            Returns:
                hash (str): matching hash value or nothing
        """
        logger.info("-"*100)
        logger.info("find_matching_hash() running...")
        hash = ""

        try:
            row = self.db.retrieve('SELECT shortened_url FROM url WHERE original_url = %s', url)
            if row:
                hash = row[0]['shortened_url']
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
        finally:
            return hash

    def get_stats_by_hash(self, hash:str) -> Tuple[int,Dict[str,dict]]:
        """ Get stats of a URL by hash

            Args:
                hash (str): hash (shortened url)
            Returns:
                status_code (int): status code of the response
                content (std_content): response object containing stats
        """
        logger.info("="*100)
        logger.info("get_stats_by_hash() running...")
        status_code = 500
        content = std_content()
        try:
            row = self.db.retrieve('SELECT url.shortened_url, url.original_url, url_stats.datetime_created, url_stats.time_accessed, FROM url INNER JOIN url_stats ON url.shortened_url = url_stats.shortened_url WHERE url.shortened_url = %s', hash)
            if row:
                time_accessed = row[0]['time_accessed'].split('@')
                num_click = 0
                if not time_accessed[0]:
                    time_accessed = []
                else:
                    num_click = len(time_accessed)

                content['data'] = {
                    'url': row[0]['original_url'],
                    'shortened_url': f"https://{self.hostname}/{row[0]['shortened_url']}",
                    'datetime_created': row[0]['datetime_created'].strftime("%d/%m/%Y %H:%M:%S"),
                    'number_of_clicks': num_click,
                    'datetime_accessed': time_accessed
                }
                status_code = 200
            else:
                status_code = 404
                content['message'] = 'Not found'
                content['data'] = {}
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
        finally:
            status_code, content

    def get_stat_by_original_url(self, args:dict) -> Tuple[int,Dict[str,dict]]:
        """ return stats by original url
        Args:
            args (dict): dictionary of arguments
        Returns:
            status_code (int): status code of the response
            content (std_content): response object containing stats
        """
        logger.info("="*100)
        logger.info("get_stats_by_original_url() running...")
        status_code = 500
        content = std_content()
        try:
            original_url = args['url'].strip()
            row = self.retrieve('SELECT url.shortened_url, url.original_url, url_stats.datetime_created, url_stats.time_accessed FROM url INNER JOIN url_stats ON url.shortened_url = url_stats.shortened_url WHERE url.original_url = %s', original_url)
            if row:
                time_accessed = row[0]['time_accessed'].split('@')
                num_click = 0
                if not time_accessed[0]:
                    time_accessed = []
                else:
                    num_click = len(time_accessed)
                
                content['data'] = {
                    'url': row[0]['original_url'],
                    'shortened_url': f'https://{self.hostname}/{row[0]["shortened_url"]}',
                    'datetime_created': row[0]['datetime_created'].strftime('%d/%m/%Y %H:%M:%S'),
                    'number_of_clicks': num_click,
                    'datetime_accessed': time_accessed
                }
                status_code = 200
            else:
                status_code = 404
                content['message'] = 'Not found'
                content['data'] = {}
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
        finally:
            return status_code, content

    def get_all_stats(self) -> Tuple[int,Dict[str,list]]:
        ''' get basic info of all shortened urls
            Returns:
                status_code (int): status code of the response
                content (std_content): response object containing basic info
        '''
        logger.info('='*100)
        logger.info('get_all() running...')
        status_code = 500
        content = std_content("",[])
        try:
            rows = self.db.retrieve('SELECT url.shortened_url, url.original_url, url_stats.datetime_created FROM url INNER JOIN url_stats ON url.shortened_url = url_stats.shortened_url')
            if rows:
                for row in rows:
                    short_url = f'https://{self.hostname}/{row["shortened_url"]}'
                    content['data'].append({'url': row['original_url'], 'shortened_url': short_url, 'datetime_created': row['datetime_created'].strftime('%d/%m/%Y %H:%M:%S')})
                status_code = 200
            else:
                status_code = 404
                content['message'] = 'Not found'
                content['data'] = {}
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
        finally:
            return status_code, content

    def redirect(self, hash:str) -> str:
        """ Redirect to original URL
            Args:
                hash (str): hash of the shortened URL
            Returns:
                string of the original URL
        """
        logger.info("="*100)
        logger.info("redirect() running...")
        
        try:
            url = self.retrieve(hash)
            self.url_access(hash)
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
        finally:
            return self.validate_url(url)

    def clear_tables(self) -> None:
        """ Clear all tables in database
            For development purpose only, don't use in production
        """
        try:
            self.db.execute("DELETE FROM url_stats")
            self.db.execute("DELETE FROM url")
        except Exception as e:
            logger.error(f"error: {e}")
            logger.error(traceback.format_exc())
