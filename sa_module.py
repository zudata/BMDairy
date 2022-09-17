import numpy as np
import json
import re


from konlpy.tag import * ; okt = Okt()


class diary:
    def __init__(self, text):
        self.text = text
        self.stop = 0
        self.word_scores = []

    def prep(self):
        self.text = re.sub('[.!]', ' ', self.text)
        self.test = re.sub('[^가-힣0-9a-zA-Z\\s]', '', self.text)
        self.text = re.sub(' +', ' ', self.text)

        return self.text

    def tokenizer(self):
        self.word_list = okt.morphs(self.text)
        self.word_list = [notoneword for notoneword in self.word_list if not len(notoneword) == 1]

        return self.word_list

    def get_score(self):
        with open('./SentiWord_info.json', encoding='utf-8-sig', mode='r') as f:
            data = json.load(f)
        score = 0

        for word in self.word_list:
            for i in range(0, len(data)):
                if data[i]['word'] == word:
                    s_word = data[i]['polarity']
                    self.word_scores.append(int(s_word))

        return self.word_scores

    def get_ratio(self):
        ent_score = 0

        ent_score = np.sum(self.word_scores)
        length = np.log10(len(self.word_scores)) + 1

        try:
            self.ratio = round(ent_score / length, 2)
        except:
            self.ratio = 0

        return self.ratio

def result(text):
    res = diary(text)
    res.prep()
    token = res.tokenizer()
    res.get_score()
    ratio = res.get_ratio()

    if ratio < -1: feel = 'Dark'
    elif ratio >1: feel = 'Bright'
    else: feel = 'Mid'

    # ---
    words = ['바다', '비', '비행기', '드라이브', '기차', '산', '계곡', '카페', '페스티벌', '공원']
    count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(0, len(words)):
        for j in range(0, len(token)):
            if words[i] in token[j]: count[i] += 1

    try: noise = words[np.argmax(count)]
    except: noise = 'nomal'

#     print('\n', ratio, '의 정도로 ', feel, '이다.', '\n', '그리고 noise는', noise, '이다.')

    return feel, noise
