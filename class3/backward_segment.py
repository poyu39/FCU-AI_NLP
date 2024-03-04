
from utility import load_dictionary

def backward_segment(text, dic):
    word_list = []
    i = len(text) - 1
    while i >= 0:                                   # 掃描位置作為終點
        longest_word = text[i]                      # 掃描位置的單字
        for j in range(0, i):                       # 遍歷[0, i]區間作為待查詢詞語的起點
            word = text[j: i + 1]                   # 取出[j, i]區間作為待查詢單詞
            if word in dic:
                if len(word) > len(longest_word):   # 越長優先順序越高
                    longest_word = word
                    break
        word_list.insert(0, longest_word)           # 逆向掃描，所以越先查出的單詞在位置上越靠後
        i -= len(longest_word)
    return word_list


if __name__ == '__main__':
    dic = load_dictionary()
    print('原始句子:項目的研究')
    print(backward_segment('項目的研究', dic))

