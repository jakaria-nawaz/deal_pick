from multiprocessing import Process

from scrappers.mediamarkt_spider import *
from scrappers.notebooksbilliger_spider import *
from scrappers.saturn_spider import *


if __name__ == '__main__':
    # saturn_proc = Process(target=SaturnSpider().start)
    # saturn_proc.start()

    mediamarkt_proc = Process(target=MediaMarktSpider().start)
    mediamarkt_proc.start()

    # nb_proc = Process(target=NotebooksBilligerSpider().start)
    # nb_proc.start()
