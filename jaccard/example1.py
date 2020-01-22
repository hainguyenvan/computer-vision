A = ["Haruka Kudo", "Okuyama Kazusa", "Noa Tsurushima"]
B = ["Okuyama Kazusa", "Noa Tsurushima", "Chika Osaki"]
C = ["Haruka Kudo", " Sakurako Okubo", "Hiroe Igeta"]


def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return len(s1.intersection(s2)) / len(s1.union(s2))


def simple_recommender_sys(list1, list2, list3):
    j1 = jaccard_similarity(list1, list2)
    j2 = jaccard_similarity(list2, list3)
    j3 = jaccard_similarity(list3, list1)
    print("j1(A-B): ", str(j1))
    print("j2(B-C): ", str(j2))
    print("j3(C-A): ", str(j3))
    if j1 > j2:
        if j1 > j3:
            print("[", list1, ",", list2, "]")
        elif j1 == j3:
            print("[", list1, ",", list2, "],[", list1, ",", list3, "]")
        else:
            print("[", list1, ",", list3, "]")
    elif j1 == j2:
        if j1 > j3:
            print("[", list1, ",", list2, "],[", list2, ",", list3, "]")
        elif j1 == j3:
            print("[", list1, ",", list2, "],[", list2, ",",
                  list3, "], [", list1, ",", list3, "]")
        else:
            print("[", list1, ",", list3, "]")
    elif j1 < j2:
        if j2 > j3:
            print("[", list2, ",", list3, "]")
        elif j2 == j3:
            print("[", list2, ",", list3, "],[", list1, ",", list3, "]")
        else:
            print("[", list1, ",", list3, "]")


simple_recommender_sys(A, B, C)
