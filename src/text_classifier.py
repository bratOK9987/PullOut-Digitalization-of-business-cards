import re
import logging

# import nltk
# pip3 install nltk
# pip3 install numpy

# from nltk import ne_chunk, pos_tag, word_tokenize
# from nltk.tree import Tree


# pip3 install -U spacy
# python3 -m spacy download en_core_web_sm  - efficiency
# python3 -m spacy download en_core_web_trf - accuracy
import spacy

# pip3 install names-dataset
from names_dataset import NameDataset

# pip3 install find-job-titles
from find_job_titles import Finder as JobFinder


class TextClassifier:
    def __init__(self):
        self.job_finder = JobFinder()
        self.names_data_set = NameDataset()

    @staticmethod
    def removeSubstrings(original_str, list_of_substrings):
        output_str = original_str
        for s in list_of_substrings:
            output_str = output_str.replace(s, '')
        return output_str

    def classify(self, original_str):
        jobs = self.find_jobs(original_str)
        original_str = self.removeSubstrings(original_str, jobs)
        phones = self.find_phones(original_str)
        original_str = self.removeSubstrings(original_str, phones)
        emails = self.find_emails(original_str)
        original_str = self.removeSubstrings(original_str, emails)
        websites = self.find_websites(original_str)
        original_str = self.removeSubstrings(original_str, websites)

        names_and_orgs = self.try_spacy(original_str)
        names_and_orgs['PERSON'] += (self.find_maybe_names_by_regex(original_str))
        person = self.find_most_probable_persone_name(names_and_orgs['PERSON'])

        result = {
            'person': person,
            'org': names_and_orgs['ORG'],
            'jobs': jobs,
            'phones': phones,
            'emails': emails,
            'websites': websites
        }

        logging.info(f'RESULT: {result}')
        return result

    @staticmethod
    def enhance_text_for_spacy(text):
        new_text = text.title()
        # new_text = new_text.replace('\n', ' ')
        new_text = ' and '.join([s.strip() for s in new_text.splitlines() if len(s.strip())])
        return new_text

    def try_spacy(self, text):
        result = {
            'PERSON': [],
            'ORG': []
        }

        logging.debug(f'INPUT 1: {text.encode()}')
        text = self.enhance_text_for_spacy(text)
        logging.debug(f'INPUT 2: {text.encode()}')
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)

        for entity in doc.ents:
            # logging.info(f'{entity.label_} : {entity.text}')
            if entity.label_ == 'PERSON':
                result['PERSON'].append(entity.text.strip())
            elif entity.label_ == 'ORG':
                result['ORG'].append(entity.text.strip())
        logging.debug(f'RESULT: {result}')
        return result

    def find_jobs(self, text):
        logging.debug(f'INPUT: {text.encode()}')
        result = []
        try:
            jobs = self.job_finder.findall(text)
            if jobs is not None:
                for job in jobs:
                    result.append(job.match)
        except RuntimeError:
            pass
        logging.debug(f'RESULT: {result}')
        return result

    @staticmethod
    def find_phones(text):
        logging.debug(f'INPUT: {text.encode()}')
        result = []
        phones = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
        if phones is not None:
            result = list(phones)
        logging.debug(f'RESULT: {result}')
        return result

    @staticmethod
    def find_emails(text):
        logging.debug(f'INPUT: {text.encode()}')
        result = []
        emails = re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', text)
        if emails is not None:
            result = list([email.lower() for email in emails])
        logging.debug(f'RESULT: {result}')
        return result

    @staticmethod
    def find_websites(text):
        logging.debug(f'INPUT: {text.encode()}')
        result = []
        reg_ex = r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"
        websites = re.findall(reg_ex, text)
        if websites is not None:
            result = list([website.lower() for website in websites])
        logging.debug(f'RESULT: {result}')
        return result

    @staticmethod
    def find_maybe_names_by_regex(text):
        result = []
        new_text = text.title()
        # new_text = new_text.replace('\n', ' ')
        # new_text = ' '.join([s.strip() for s in new_text.splitlines() if len(s.strip())])

        logging.debug(f'INPUT: {new_text.encode()}')
        maybe_names = re.findall(r"[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+", new_text)
        if maybe_names is not None:
            result = list([name.strip() for name in maybe_names])
        logging.debug(f'RESULT: {result}')
        return result

    def find_most_probable_persone_name(self, list_of_maybe_names):
        stats = {name: self.get_name_validity_probability(name) for name in list_of_maybe_names}
        logging.debug(f'{stats}')
        return max(stats, key=stats.get)

    def get_name_validity_probability(self, maybe_name):
        scores = []
        chunks = maybe_name.split()

        if any(not c.isalnum() for c in maybe_name.replace(' ', '')):
            return 0

        if len(chunks) < 2:
            return 0

        for x in chunks:
            r = self.names_data_set.search(x)
            is_first_name = 0
            is_last_name = 0
            if r['first_name'] is not None:
                is_first_name = max(r['first_name']['country'].values())
                logging.debug(f"{x} is first name = {is_first_name}")
            if r['last_name'] is not None:
                is_last_name = max(r['last_name']['country'].values())
                logging.debug(f"{x} is last name = {is_last_name}")
            scores.append(max(is_first_name, is_last_name))
        return sum(scores) / len(scores) if len(scores) else 0


if __name__ == '__main__':
    pass
