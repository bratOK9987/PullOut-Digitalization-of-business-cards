from text_extractor import TextExtractor
from text_classifier import TextClassifier
from storage import Storage
import logging


class CardRecognizer:
    def __init__(self):
        self.text_extractor = TextExtractor()
        self.text_classifier = TextClassifier()
        self.storage = Storage()

    def action_scan(self, args):
        logging.info('>>> In scan action')
        for file in args.files:
            logging.info(f'Processind file: {file}')
            text_entries = self.text_extractor.extract_text_entries(file)
            if len(text_entries):
                cd = self.text_classifier.classify(text_entries)
                self.storage.add(cd)

    def action_list(self, args):
        logging.info('>>> In list action')
        self.storage.list_items()

