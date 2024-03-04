
from utility import load_dictionary

def forward_segment(text, dic):
    word_list = []
    i = 0
    while i < len(text):
        longest_word = text[i]                      # 當前掃描位置的單字
        for j in range(i + 1, len(text) + 1):       # 所有可能的結尾
            word = text[i:j]                        # 從當前位置到結尾的連續字串
            if word in dic:                         # 在詞典中
                if len(word) > len(longest_word):   # 並且更長
                    longest_word = word             # 則更優先輸出
        word_list.append(longest_word)              # 輸出最長詞
        i += len(longest_word)                      # 正向掃描
    return word_list


if __name__ == '__main__':
    dic = load_dictionary()
    print('原始句子:商品和服務')
    print(forward_segment('商品和服務', dic))

