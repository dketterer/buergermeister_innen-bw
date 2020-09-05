from .crawler import Crawler
import argparse
import logging


def parse_args():
    parser = argparse.ArgumentParser('Crawl Bürgermeister Baden-Württemberg')
    parser.add_argument('--save', '-s', type=str, required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=logging.INFO)
    crawler = Crawler()
    crawler.start()
    crawler.save(args.save)


if __name__ == '__main__':
    main()
