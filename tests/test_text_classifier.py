import pytest
from text_classifier import TextClassifier


class TestTextClassifier:
    text_classifier = TextClassifier()

    def test_removeSubstrings(self):
        input_str = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        substrings_to_remove = ['ipsum', 'amet', 'elit']
        output_str = self.text_classifier._removeSubstrings(input_str, substrings_to_remove)
        for substring in substrings_to_remove:
            assert substring not in output_str

    def test_enhance_text_for_spacy(self):
        input_str = 'Lorem ipsum\n\ndolor sit amet,\n\nconsectetur adipiscing elit.'
        output_str = self.text_classifier._enhance_text_for_spacy(input_str)
        expected_output_srt = 'Lorem Ipsum and Dolor Sit Amet, and Consectetur Adipiscing Elit.'
        assert output_str == expected_output_srt

    @pytest.mark.parametrize('input_text,expected_result', [
        ('Bill Gates is CEO of Microsoft Corporation.', {'PERSON': ['Bill Gates'], 'ORG': ['Microsoft Corporation']}),
        ('Jensen Huang is a founder of Nvidia Corporation.', {'PERSON': ['Jensen Huang'], 'ORG': ['Nvidia Corporation']})
    ])
    def test_try_spacy(self, input_text, expected_result):
        result = self.text_classifier._try_spacy(input_text)
        assert result == expected_result

    @pytest.mark.parametrize('maybe_job,expected_result', [
        ('Marketing Manager', True),
        ('Electrical Engineer', True),
        ('Vice President', True),
        ('Dog', False),
        ('Something', False)
    ])
    def test_find_jobs(self, maybe_job, expected_result):
        result = self.text_classifier._find_jobs(maybe_job)
        assert (maybe_job in result) == expected_result

    @pytest.mark.parametrize('maybe_phone,expected_result', [
        ('212 456 7890', True),
        ('+12124567890', True),
        ('+1 212.456.7890', True),
        ('(212)456-7890', True),
        ('(212)4a56-a78a90', False),
    ])
    def test_find_phones(self, maybe_phone, expected_result):
        result = self.text_classifier._find_phones(maybe_phone)
        assert (maybe_phone in result) == expected_result

    @pytest.mark.parametrize('maybe_email,expected_result', [
        ('hello@reallygreatsite.com', True),
        ('some123@apple.com', True),
        ('some123apple.com', False),
    ])
    def test_find_emails(self, maybe_email, expected_result):
        result = self.text_classifier._find_emails(maybe_email)
        assert (maybe_email in result) == expected_result

    @pytest.mark.parametrize('maybe_website,expected_result', [
        ('www.microsoft.com', True),
        ('google.com', True),
        ('some12@3apple.com', False),
    ])
    def test_find_websites(self, maybe_website, expected_result):
        result = self.text_classifier._find_websites(maybe_website)
        assert (maybe_website in result) == expected_result

    @pytest.mark.parametrize('list_of_maybe_names,expected_result', [
        (['Bob Fisher', 'Police Department', 'Apple', 'Walk Abroad'], 'Bob Fisher'),
        (['Sand Five', 'Harry Potter', 'Ignore Someting'], 'Harry Potter'),
    ])
    def test_find_most_probable_person_name(self, list_of_maybe_names, expected_result):
        result = self.text_classifier._find_most_probable_person_name(list_of_maybe_names)
        assert result == expected_result

    @pytest.mark.parametrize('input_str,expected_result', [
        ('Mariana Anderson\nMarketing Manager\n+123-456-7890\nwww.reallygreatsite.com\nhello@reallygreatsite.com',
         {
             'person': 'Mariana Anderson',
             'org': [],
             'jobs': ['Marketing Manager'],
             'phones': ['+123-456-7890'],
             'emails': ['hello@reallygreatsite.com'],
             'websites': ['www.reallygreatsite.com']
         }
         ),

        ('Liceria & Co.\nReal Estate\nMORGAN MAXWELL\nGeneral Manager\n+123-456-7890\hello@reallygreatsite.com\nwww.reallygreatsite.com\n',
         {
             'person': 'Morgan Maxwell',
             'org': ['Liceria & Co.', 'Real Estate', 'Morgan Maxwell'],
             'jobs': ['General Manager'],
             'phones': ['+123-456-7890'],
             'emails': ['hello@reallygreatsite.com'],
             'websites': ['www.reallygreatsite.com']
         }
         ),

        (
        'John Couch\nVice President\nApple\n408 974-6117 phone\n408 974-0121 fax\njcouch@apple.com\nwww.apple.com\n\n',
        {
            'person': 'John Couch',
            'org': ['Apple'],
            'jobs': ['Vice President'],
            'phones': ['408 974-6117', '408 974-0121'],
            'emails': ['jcouch@apple.com'],
            'websites': ['www.apple.com']
        }
        ),

    ])
    def test_classify(self, input_str, expected_result):
        result = self.text_classifier.classify(input_str)
        assert type(result) is dict
        assert len(result) > 0
        assert result == expected_result
