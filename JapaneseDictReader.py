import json


with open('kanjidic2.json', 'r', encoding="utf-8") as obj:
    data = json.load(obj)

KanjiDict = {}

for i in range(len(data["kanjidic2"]["character"])):
    KanjiDict[data["kanjidic2"]["character"][i]["literal"]] = data["kanjidic2"]["character"][i]

def getKanjiDefinition_v2(kanjiInput):
    """Significantly faster than v1"""
    #print(KanjiDict.get(kanjiInput))

    KanjiResultDict = {}
    KanjiDefition_Result = KanjiDict.get(kanjiInput)
    KanjiDefition_character = ''
    KanjiDef_stroke_count = ''
    KanjiDef_freq = ''
    KanjiDef_jlpt = ''
    KanjiDef_grade = ''
    KanjiDef_nelson_n = ''
    KanjiDef_heisig = ''
    KanjiDef_meaning = ''
    KanjiDef_Pinyin = ''
    KanjiDef_Reading_On = ''
    KanjiDef_Reading_Kun = ''

    if KanjiDefition_Result:
        # only run if result not None i.e input is actually kanji
        if 'literal' in KanjiDefition_Result:
            KanjiDefition_character = KanjiDefition_Result['literal']
        if 'stroke_count' in KanjiDefition_Result['misc']:
            KanjiDef_stroke_count = KanjiDefition_Result['misc']['stroke_count']
        if 'freq' in KanjiDefition_Result['misc']:
            KanjiDef_freq = KanjiDefition_Result['misc']['freq']
        if 'jlpt' in KanjiDefition_Result['misc']:
            KanjiDef_jlpt = KanjiDefition_Result['misc']['jlpt']
        if 'grade' in KanjiDefition_Result['misc']:
            KanjiDef_grade = KanjiDefition_Result['misc']['grade']
        if 'dic_number' in KanjiDefition_Result:
            if 'dic_ref' in KanjiDefition_Result['dic_number']:
                # nelson_n = [elem['#text'] for elem in KanjiDefition_Result['dic_number']['dic_ref'] if elem["-dr_type"] == 'nelson_n']
                if isinstance(KanjiDefition_Result['dic_number']['dic_ref'], list):
                    KanjiDef_nelson_n_tem = [elem['#text'] for elem in KanjiDefition_Result['dic_number']['dic_ref'] if
                                         elem['-dr_type'] == 'nelson_n']
                    if bool(KanjiDef_nelson_n_tem):
                        KanjiDef_nelson_n = KanjiDef_nelson_n_tem[0]
                    # KanjiDef_heisig = [elem['#text'] for elem in KanjiDefition_Result['dic_number']['dic_ref'] if elem['-dr_type'] == 'heisig'][0]  . Old version that gave error if 'heisig' dict did not exist because you are trying to read 'heisig'][0]
                    KanjiDef_heisig_tem = [elem['#text'] for elem in KanjiDefition_Result['dic_number']['dic_ref'] if
                                       elem['-dr_type'] == 'heisig']
                    if bool(KanjiDef_heisig_tem):
                        KanjiDef_heisig = KanjiDef_heisig_tem[0]


        if 'rmgroup' in KanjiDefition_Result['reading_meaning']:
            if 'meaning' in KanjiDefition_Result['reading_meaning']['rmgroup']:
                for mList in KanjiDefition_Result['reading_meaning']['rmgroup']['meaning']:
                    # english meaning is in str type whereas other meaning is in list type
                    if isinstance(mList, str):
                        KanjiDef_meaning = KanjiDef_meaning + mList + ', '
            if 'reading' in KanjiDefition_Result['reading_meaning']['rmgroup']:
                for readingList in KanjiDefition_Result['reading_meaning']['rmgroup']['reading']:
                    if readingList.get('-r_type') == 'pinyin':
                        KanjiDef_Pinyin = KanjiDef_Pinyin + readingList.get('#text') + ', '
                    elif readingList.get('-r_type') == 'ja_on':
                        KanjiDef_Reading_On = KanjiDef_Reading_On + readingList.get('#text') + ', '
                    elif readingList.get('-r_type') == 'ja_kun':
                        KanjiDef_Reading_Kun = KanjiDef_Reading_Kun + readingList.get('#text') + ', '

    KanjiResultDict["character"] = KanjiDefition_character
    KanjiResultDict["stroke_count"] = KanjiDef_stroke_count
    KanjiResultDict["freq"] = KanjiDef_freq
    KanjiResultDict["jlpt"] = KanjiDef_jlpt
    KanjiResultDict["grade"] = KanjiDef_grade
    KanjiResultDict["nelson_n"] = KanjiDef_nelson_n
    KanjiResultDict["heisig"] = KanjiDef_heisig
    KanjiResultDict["meaning"] = KanjiDef_meaning
    KanjiResultDict["Pinyin"] = KanjiDef_Pinyin
    KanjiResultDict["Reading_On"] = KanjiDef_Reading_On
    KanjiResultDict["Reading_Kun"] = KanjiDef_Reading_Kun

    if not KanjiResultDict["character"]:
        KanjiResultDict = ''

    #print(KanjiDefition_Result.keys())
    #print("")
    #print(KanjiDefition_Result)
    #print(KanjiResultDict)
    return KanjiResultDict


#print(data["kanjidic2"]["character"][0]["literal"])
#print(data["kanjidic2"]["character"][0])
#print(len(data["kanjidic2"]["character"]))


print (KanjiDict.get('擧'))
test_result = getKanjiDefinition_v2('女')
print (test_result)
print ("")
test_result = getKanjiDefinition_v2('邂')
print (test_result)
print ("")
print (KanjiDict.get('靑'))



"""
for x in range(0,1000):
    getKanjiDefinition_v2('模')
    getKanjiDefinition_v2('垬')
    getKanjiDefinition_v2('幣')
    getKanjiDefinition_v2('藍')
    getKanjiDefinition_v2('獻')
    getKanjiDefinition_v2('萊')
    getKanjiDefinition_v2('譯')
    getKanjiDefinition_v2('奪')
    getKanjiDefinition_v2('燒')
    getKanjiDefinition_v2('觸')
    getKanjiDefinition_v2('課')
    getKanjiDefinition_v2('牆')
    getKanjiDefinition_v2('襲')
    getKanjiDefinition_v2('罰')
    getKanjiDefinition_v2('俠')
    getKanjiDefinition_v2('廳')
    getKanjiDefinition_v2('側')
    getKanjiDefinition_v2('韓')
    getKanjiDefinition_v2('債')
    getKanjiDefinition_v2('慣')
    getKanjiDefinition_v2('猶')
    getKanjiDefinition_v2('掛')
    getKanjiDefinition_v2('奬')
    getKanjiDefinition_v2('紹')
    getKanjiDefinition_v2('縱')
    getKanjiDefinition_v2('訊')
    getKanjiDefinition_v2('徹')
    getKanjiDefinition_v2('烏')
    getKanjiDefinition_v2('瑪')
    getKanjiDefinition_v2('鏡')
    getKanjiDefinition_v2('煩')
    getKanjiDefinition_v2('簽')
    getKanjiDefinition_v2('癥')
    getKanjiDefinition_v2('傾')
    getKanjiDefinition_v2('鳥')
    getKanjiDefinition_v2('轟')

"""