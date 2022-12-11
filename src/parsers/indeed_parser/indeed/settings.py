
BOT_NAME = 'indeed'

SPIDER_MODULES = ['indeed.spiders']
NEWSPIDER_MODULE = 'indeed.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

## ScrapeOps API Key
SCRAPEOPS_API_KEY = '7cb6fee1-8623-442b-b044-b8745718b7e4' ## Get Free API KEY here: https://scrapeops.io/app/register/main

## Enable ScrapeOps Proxy
SCRAPEOPS_PROXY_ENABLED = True

# Add In The ScrapeOps Monitoring Extension
EXTENSIONS = {
'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
}


DOWNLOADER_MIDDLEWARES = {

    ## ScrapeOps Monitor
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    
    ## Proxy Middleware
    'indeed.middlewares.ScrapeOpsProxyMiddleware': 725,
}

# Max Concurrency On ScrapeOps Proxy Free Plan is 1 thread
CONCURRENT_REQUESTS = 1
