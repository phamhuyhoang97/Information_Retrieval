import pymysql



############ Jaccard
def separate_word(sentence1):
    List = []

    flag = 0
    for i in range(len(sentence1)):
        if sentence1[i] == ' ':
            List.append(sentence1[flag:i])
            flag = i+1
        if i == len(sentence1)-1:
            List.append(sentence1[flag:i+1])
    return List

def create_shingles(List, n_gram):
    shingles_list = []

    for i in range(len(List) - n_gram):
        shingle_element = List[i:i+n_gram]
        if shingle_element not in shingles_list :
            shingles_list.append(shingle_element)

    return shingles_list + [List[-2:]]

def jaccard_similarity(sentence1, sentence2, n_gram):
    num = 0
    total = 0

    list1 = separate_word(sentence1)
    list2 = separate_word(sentence2)

    shingles_list1 = create_shingles(list1, n_gram)
    shingles_list2 = create_shingles(list2, n_gram)
    
    total += len(shingles_list1)

    for i in range(len(shingles_list2)):
        flag = True
        for j in range(len(shingles_list1)):
            if shingles_list2[i] == shingles_list1[j]:
                num += 1
                flag = False

        if flag == True:
            total += 1
    
    return num/total

# check one with others all, return True => is similar
def jaccard_one_with_all(sentence, All, n_gram, threshold):
    max_jaccard = 0

    for i in range(len(All)):
        jaccard_number = jaccard_similarity(sentence, All[i], n_gram)
        if jaccard_number > max_jaccard:
            max_jaccard = jaccard_number

    return max_jaccard > threshold


if __name__ == "__main__":
    # test for all 
    n_gram = 2
    threshold = 0.5
    sentence = "Dàn diễn viên trong bộ phim truyền hình đang gây nhỏ thời gian qua \"Về nhà đi con\" đều là những gương mặt nhận được rất nhiều sự quan tâm từ khán giả."
    sentence_array = [
        "Jack London traveled to the city of Oakland",
        "Jack traveled from Oakland to London"
    ]

    # result2 = jaccard_one_with_all(sentence, sentence_array, n_gram, threshold)
    # print(result2)

    con = pymysql.connect('localhost', 'root', '', 'IR')

    with con: 
        cur = con.cursor()
        cur.execute("SELECT short_content FROM news1")
        rows = cur.fetchall()
    x = []
    for item in rows:
        x.extend(item)
    result2 = jaccard_one_with_all(sentence, x, n_gram, threshold)
    print(type(x))
    print(result2)