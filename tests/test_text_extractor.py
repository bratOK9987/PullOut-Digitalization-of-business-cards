import pytest
from text_extractor import TextExtractor


class TestTextExtractor:
    textExtractor = TextExtractor()

    def test_available_languages(self):
        languages = self.textExtractor.available_languages()
        assert type(languages) is list
        assert len(languages) > 0
        assert 'eng' in languages
        assert 'lit' in languages

    @pytest.mark.parametrize('img_path,expected_text_entries', [
        ('card_samples/card_1.png', ['Mariana Anderson', 'Marketing Manager', '+123-456-7890', 'www.reallygreatsite.com', 'hello@reallygreatsite.com']),
        ('card_samples/card_2.png', ['MORGAN MAXWELL', 'General Manager', '+123-456-7890', 'www.reallygreatsite.com', 'hello@reallygreatsite.com']),
        ('card_samples/card_3.png', ['Claudia Alves', 'Marketing Manager', '+123-456-7890', 'www.reallygreatsite.com', 'hello@reallygreatsite.com']),
        ('card_samples/card_4.jpg', ['William H. Gam', 'Microsoft Corporation', 'One Microsoft Way', '425 882 8080', '425 936 7329', 'bilig@microsoft.com']),
        ('card_samples/card_5.jpg', ['John Couch', 'Vice President', 'Education', 'Apple', 'Cupertino', 'California', '408 974-6117', '408 974-0121', 'jcouch@apple.com', 'www.apple.com']),
        ('card_samples/card_6.jpg', ['apple computer inc', 'Cupertino', 'California', '(408) 996-1010', 'Steven Jobs',  'Vice President', 'new product development']),
        ('card_samples/card_7.png', ['Jim', 'Bob', 'Graphic Designer', "Jim's Graphics", '999-999-9999', 'www.jimsgraphics.com', 'jim@jimsgraphics.com']),
    ])
    def test_extract_text_entries(self, img_path, expected_text_entries):
        result = self.textExtractor.extract_text_entries(img_path)
        for expected_text_entry in expected_text_entries:
            assert expected_text_entry.lower() in result.lower()
