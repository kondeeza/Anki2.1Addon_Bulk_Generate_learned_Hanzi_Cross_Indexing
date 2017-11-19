# -*- coding: utf-8 -*-
# Copyright: mo  <fickle_123@hotmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

# Bulk copy data in one field to another.
# TODO:
# Auto Sentence supplementary LIST
# Sync Hint field. maybe for all note that shared audio file, allowing user to mark field with ** or something to be the most recent update. or maybe just simply copy along the note field to master.
# GUI? nah
# Factorise , i.e. Move all pre validation of note field etc into prevalidate() or something. then make reporting info more informative
# Factorise , remove fuzzy shotgun coding, or maybe seperate into different python. test git commmit

##########################################################################


##########################################################################
from aqt.qt import *
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
from anki.hooks import addHook
from aqt import mw
from aqt.utils import showWarning, showInfo
import re
import platform
import re
import os
########################################################################## THIS SOLVES THE ANNOYING UNICODE ISSUE
import sys

# reload(sys) #apparently this doesn't work in python3...
# sys.setdefaultencoding('utf-8')
########################################################################## THIS SOLVES THE ANNOYING UNICODE ISSUE !!

master_modelName = ''
master_Hanzi_SrcField = ''
master_Auto_Sentence_SrcField = ''
master_Auto_SR_SrcField = ''
master_Auto_ST_SrcField = ''
master_Auto_SA_SrcField = ''
master_Auto_SentenceF_SrcField = ''
master_Auto_SR_F_SrcField = ''
master_Auto_ST_F_SrcField = ''
master_Auto_Synced_Hint_SrcField = ''
master_deckName = ''
Enable_Optional_Custom_MasterSlaveSyncFieldList = ''
Optional_Custom_MasterSlaveSyncFieldList = ''
master_Traditional_Field = 'Traditional'
master_Freq_Field = 'FrequencyRank'
master_Pinyin_Field = 'Pinyin'
master_Pinyin2_Field = 'Pinyin 2'
master_meaning_Field = 'Meaning'
Master_to_Corresponding_Slave_Field_List = ''
# if data exists in Output_SrcField, should we overwrite it?
OVERWRITE_DST_FIELD = ''

slave_Model_Sentence_SPinyin_SMeaning_SAudio_List = []


def reload_config():
    global master_modelName
    global master_Hanzi_SrcField
    global master_Auto_Sentence_SrcField
    global master_Auto_SR_SrcField
    global master_Auto_ST_SrcField
    global master_Auto_SA_SrcField
    global master_Auto_SentenceF_SrcField
    global master_Auto_SR_F_SrcField
    global master_Auto_ST_F_SrcField
    global OVERWRITE_DST_FIELD
    global slave_Model_Sentence_SPinyin_SMeaning_SAudio_List
    global master_deckName
    global master_Auto_Synced_Hint_SrcField
    global Enable_Optional_Custom_MasterSlaveSyncFieldList
    global Master_to_Corresponding_Slave_Field_List

    config = mw.addonManager.getConfig(__name__)
    master_modelName = config['01_master_modelName']
    master_Hanzi_SrcField = config['02_master_Hanzi_SrcField']
    master_Auto_Sentence_SrcField = config['03_master_Auto_Sentence_SrcField']
    master_Auto_SR_SrcField = config['04_master_Auto_SR_SrcField']
    master_Auto_ST_SrcField = config['05_master_Auto_ST_SrcField']
    master_Auto_SA_SrcField = config['06_master_Auto_SA_SrcField']
    master_Auto_SentenceF_SrcField = config['07_master_Auto_SentenceF_SrcField']
    master_Auto_SR_F_SrcField = config['08_master_Auto_SR_F_SrcField']
    master_Auto_ST_F_SrcField = config['09_master_Auto_ST_F_SrcField']
    OVERWRITE_DST_FIELD = config['15_OVERWRITE_DST_FIELD']
    master_deckName = config['10_master_deckName']
    master_Auto_Synced_Hint_SrcField = config['11_master_Auto_Synced_Hint_SrcField']
    slave_Model_Sentence_SPinyin_SMeaning_SAudio_List = config['16_slave_Model_Sentence_SPinyin_SMeaning_SAudio_List']
    Enable_Optional_Custom_MasterSlaveSyncFieldList = config['13_Enable_Optional_Custom_MasterSlaveSyncFieldList']
    Master_to_Corresponding_Slave_Field_List = config['17_Master_to_Corresponding_Slave_Field_List']


def validateFieldList(nids):
    # TODO: 1. validate Master & Slave Note exist, Deck exist 2. validate master and slave fields exist 3. also validate correct field list syntax input
    # TODO: if validate did not pass (i.e field not exist), prompt user and abort program. else, return true and proceed. This is for simplifying Hanzi and kanji validation compatability process
    return true


def createAnkiNote(hanziToAddNoteList, masterNoteModelFile):
    mw.checkpoint("Manual Create Note")
    mw.progress.start()

    # Get desired deck name from input box
    deckName = master_deckName
    if not deckName:
        return
    # deckName = deckName.replace('"', "")

    # Create new deck with name from input box
    deck = mw.col.decks.get(mw.col.decks.id(deckName))

    # Copy notes
    for hanziNote in hanziToAddNoteList:
        showInfo("Found note: %s" % (str(hanziNote)))
        # note = mw.col.getNote(nid)
        model = masterNoteModelFile

        # Assign model to deck
        mw.col.decks.select(deck['id'])
        mw.col.decks.get(deck)['mid'] = model['id']
        mw.col.decks.save(deck)

        # Assign deck to model
        mw.col.models.setCurrent(model)
        mw.col.models.current()['did'] = deck['id']
        mw.col.models.save(model)
        # Create new note
        note_toAdd = mw.col.newNote()
        # Copy tags and fields (all model fields) from original note
        # note_toAdd.tags = note.tags
        # note_toAdd.fields = note.fields
        note_toAdd[master_Hanzi_SrcField] = hanziNote[1]
        note_toAdd[master_Traditional_Field] = hanziNote[2]
        note_toAdd[master_Freq_Field] = str(hanziNote[0])
        note_toAdd[master_Pinyin_Field] = hanziNote[4]
        note_toAdd[master_Pinyin2_Field] = hanziNote[5]
        note_toAdd[master_meaning_Field] = hanziNote[6]
        note_toAdd[master_Auto_Sentence_SrcField] = hanziNote[8][0]
        note_toAdd[master_Auto_SR_SrcField] = hanziNote[8][1]
        note_toAdd[master_Auto_ST_SrcField] = hanziNote[8][2]
        note_toAdd[master_Auto_SA_SrcField] = hanziNote[8][3]
        note_toAdd[master_Auto_Synced_Hint_SrcField] = hanziNote[8][4]
        if len(hanziNote[8]) >= 6 and Enable_Optional_Custom_MasterSlaveSyncFieldList == True:
            note_toAdd[hanziNote[8][5][0]] = hanziNote[8][5][1]
        # Refresh note and add to database
        note_toAdd.flush()
        mw.col.addNote(note_toAdd)

    # Reset collection and main window

    mw.col.reset()
    showInfo("collection has been reset")
    mw.progress.finish()
    mw.reset()
    showInfo("All done !")


def get_Correct_Slave_Schema_List_For_Current_Note(note):
    # this will return the correct slave schema for current note input.
    # result would be from one of the list inside 17_Master_to_Corresponding_Slave_Field_List
    # for example, result could be
    # [
    #   ["HSK",
    #   ["SentenceSimplified","Auto_Sentence",true],
    #   ["SentencePinyinMarks","Auto_SR",true],
    #   ["SentenceMeaning","Auto_ST",true],
    #   ["SentenceAudio","Auto_SA",true],
    #   ["Note","Auto_Synced_Hint",true],
    #   ["Auto_SawSentenceExample","Key"]
    # ]
    result = []
    for k in Master_to_Corresponding_Slave_Field_List:
        if k[0] in note.model()['name']:
            result = k
    return result


def Generate_Slave_Hanzi_Index(nids):
    mw.checkpoint("Bulk-Generate Generate_Slave_Hanzi_Index")
    mw.progress.start()
    reload_config()
    Slave_Hanzi_Dict = {}
    HanziFreqList = []
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, "HanziFrequencyList.txt"), "r", encoding="utf-8") as f:
        HanziFreqList = [line.split('\t') for line in f]
    warning_counter = 0
    warning_slaveModelNotFound = 0
    warning_slaveSentence_NotFound = 0
    info_Slave_Hanzi_indexed = 0
    info_Slave_Hanzi_not_in_Hanzi_Frequency_List = 0
    HanziOfHanziFreqList = [hanzi[1] for hanzi in HanziFreqList]
    for nid in nids:
        # showInfo ("Found note: %s" % (nid))
        note = mw.col.getNote(nid)
        cSlaveSchema = get_Correct_Slave_Schema_List_For_Current_Note(note)
        if not cSlaveSchema:
            # showInfo ("no Model matched")
            warning_counter += 1
            warning_slaveModelNotFound += 1
            continue
        src_slave_Sentence = None
        # check to see if note indeed contain the field from cSlaveSchema. This should be moved to validation() later
        # cSlaveSchema[0] will always be its note type name e.g. "My Basic Note Type"
        # cSlaveSchema[1][0] will always be slave sentence schema e.g. "Vocab Sentence Field"
        if cSlaveSchema[1][0] in note:
            src_slave_Sentence = cSlaveSchema[1]
        if not src_slave_Sentence:
            # no src_slave_Sentence field
            # showInfo ("--> Field %s not found." % (slave_Sentence_SrcField))
            warning_counter += 1
            warning_slaveSentence_NotFound += 1
            continue

        try:

            # This code turn string from slave_Sentence Field into char, then check for each char
            # whether it is in HanziOfHanziFreqList or not, if it is then that char is Hanzi character
            # and it will be indexed in Slave_Hanzi_Dict[x] where x = Hanzi
            # Slave_Hanzi_Dict[x] will return
            for x in note[src_slave_Sentence]:
                if x in HanziOfHanziFreqList:
                    cSlave_ToIndex_Note = []
                    # currentoopCount is used to skip cSlaveSchema[0], a.k.a. Slave note name, from being added into Slave_Hanzi_Dict[x]
                    currentloopCount = 0
                    for i in cSlaveSchema:
                        if currentloopCount != 0:
                            if isinstance(i, str):
                                cSlave_ToIndex_Note.append(note[i])
                            elif isinstance(i, list):
                                cSlave_ToIndex_Note.append([i[0], note[i[1]]])
                        currentloopCount += 1
                    if x not in Slave_Hanzi_Dict:
                        Slave_Hanzi_Dict[x] = [cSlave_ToIndex_Note]
                        info_Slave_Hanzi_indexed += 1
                    else:
                        Slave_Hanzi_Dict[x].append(cSlave_ToIndex_Note)
                        info_Slave_Hanzi_indexed += 1
                else:
                    info_Slave_Hanzi_not_in_Hanzi_Frequency_List += 1
                    # showInfo (str(Slave_Hanzi_Dict[x]))
                    # TextOutput = note[src1]
                    # note[dst]= str(TotalWordCount)
        except Exception as e:
            raise
        note.flush()
    # showInfo ("Completed Distinct Hanzi Count is %s" %str(len(Slave_Hanzi_List)))
    # showInfo (str(Slave_Hanzi_List))



    # showInfo (TextOutput)
    showInfo(
        "--> Generate_Slave_Hanzi_Index.\n warning_counter = %d \n warning_slaveModelNotFound = %d \n warning_slaveSentence_NotFound = %d \n info_Slave_Hanzi_indexed = %d \n info_Slave_Hanzi_not_in_Hanzi_Frequency_List = %d" % (
        warning_counter, warning_slaveModelNotFound, warning_slaveSentence_NotFound, info_Slave_Hanzi_indexed,
        info_Slave_Hanzi_not_in_Hanzi_Frequency_List))
    mw.progress.finish()
    mw.reset()
    return Slave_Hanzi_Dict


def BulkGenerateLearned_Hanzi_Cross_Indexing(nids):
    mw.checkpoint("Bulk-Generate TotalWordCount")
    mw.progress.start()
    reload_config()
    # HanziFreqList contains the list of 10k Hanzi Frequency as: [freq,HanS,HanT,Index,PinY,Meaning,index2]
    HanziFreqList = []
    HanziFreqDict = {}
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, "HanziFrequencyList.txt"), "r", encoding="utf-8") as f:
        HanziFreqList = [line.split('\t') for line in f]

    # showInfo ("Beginning BulkGenerateLearned_Hanzi_Cross_Indexing with this config:\n master_modelName: %s \n master_Hanzi_SrcField: %s \n master_Auto_Sentence_SrcField: %s \n master_Auto_SR_SrcField: %s \n master_Auto_ST_SrcField: %s \n master_Auto_SA_SrcField: %s \n master_Auto_SentenceF_SrcField: %s \n master_Auto_SR_F_SrcField: %s \n master_Auto_ST_F_SrcField: %s \n OVERWRITE_DST_FIELD: %s \n slave_Model_Sentence_SPinyin_SMeaning_SAudio_List: %s " %(master_modelName,master_Hanzi_SrcField,master_Auto_Sentence_SrcField,master_Auto_SR_SrcField,master_Auto_ST_SrcField,master_Auto_SA_SrcField,master_Auto_SentenceF_SrcField,master_Auto_SR_F_SrcField,master_Auto_ST_F_SrcField,OVERWRITE_DST_FIELD, str(slave_Model_Sentence_SPinyin_SMeaning_SAudio_List) ))
    showInfo(
        "Begins BulkGenerateLearned_Hanzi_Cross_Indexing with this config:\n master_modelName: %s \n master_Hanzi_SrcField: %s \n Master_to_Corresponding_Slave_Field_List %s \n OVERWRITE_DST_FIELD: %s" % (
        master_modelName, master_Hanzi_SrcField, str(slave_Model_Sentence_SPinyin_SMeaning_SAudio_List),
        OVERWRITE_DST_FIELD))
    validateFieldList(nids)
    # TODO: add abort clause if validate return false
    Master_Hanzi_Dict = {}
    Slave_Hanzi_Dict = Generate_Slave_Hanzi_Index(nids)
    info_Distinct_Hanzi_In_Slave_Deck = len(Slave_Hanzi_Dict)
    info_Hanzi_In_Master_Card_but_Not_in_Slave = 0
    info_Total_Changes_Made_To_Master_Card = 0
    masterNoteModelFile = ''
    showInfo("--> Now on final part. Binding final output to dst !")
    ########################################
    # for Sla_H in Slave_Hanzi_Dict
    ###########################################
    for nid in nids:
        # showInfo ("Found note: %s" % (nid))
        note = mw.col.getNote(nid)
        if master_modelName not in note.model()['name']:
            continue
        # showInfo(str(note.model()))
        # showInfo(str(note._model))
        if not masterNoteModelFile:
            masterNoteModelFile = note._model
        if master_Hanzi_SrcField in note:
            # showInfo ("No issue with master_Hanzi_SrcField")
            print("No issue with master_Hanzi_SrcField")
        else:
            # no master_Hanzi_SrcField field
            # showInfo ("--> Field %s not found." % (master_Hanzi_SrcField))
            continue
        if master_Auto_Sentence_SrcField in note:
            # showInfo ("--> Field %s is found!" % (master_Auto_Sentence_SrcField))
            print("--> Field %s is found!" % (master_Auto_Sentence_SrcField))
        else:
            # showInfo ("--> Field %s not found!" % (master_Auto_Sentence_SrcField))
            # no dst field
            continue
        if note[master_Auto_Sentence_SrcField] and not OVERWRITE_DST_FIELD:
            # already contains data, skip
            # showInfo ("--> %s not empty. Skipping!" % (master_Auto_Sentence_SrcField))
            continue
        try:
            a = Slave_Hanzi_Dict.get(note[master_Hanzi_SrcField])
            if not a:
                # showInfo ("--> cannot find cross ref for %s Skipping!" % note[master_Hanzi_SrcField])
                info_Hanzi_In_Master_Card_but_Not_in_Slave += 1
                continue
            del Slave_Hanzi_Dict[note[master_Hanzi_SrcField]]
            # showInfo ("for Hanzi" + note[master_Hanzi_SrcField] + "We will use" + str(a))
            # showInfo ("a[0] = %s" %str(a[0]))
            note[master_Auto_Sentence_SrcField] = a[0][0]
            note[master_Auto_SR_SrcField] = a[0][1]
            note[master_Auto_ST_SrcField] = a[0][2]
            note[master_Auto_SA_SrcField] = a[0][3]
            note[master_Auto_Synced_Hint_SrcField] = a[0][4]
            if len(a[0]) >= 6 and Enable_Optional_Custom_MasterSlaveSyncFieldList == True:
                note[a[0][5][0]] = a[0][5][1]

            info_Total_Changes_Made_To_Master_Card += 1
            # note[master_Auto_SentenceF_SrcField] = 'Auto_SentenceF'
            # note[master_Auto_SR_F_SrcField] = 'Auto_SR_F'
            # note[master_Auto_ST_F_SrcField] = 'Auto_ST_F'
        except Exception as e:
            raise
        note.flush()

    # Now to deal with slave hanzi that does not exist in master deck
    info_Hanzi_In_Slave_Card_but_Not_in_Master = len(Slave_Hanzi_Dict)
    showInfo(
        "--> Everything should have worked.\n info_Hanzi_In_Master_Card_but_Not_in_Slave = %d \n info_Total_Changes_Made_To_Master_Card = %d \n info_Distinct_Hanzi_In_Slave_Deck = %d \n info_Hanzi_In_Slave_Card_but_Not_in_Master = %d" % (
        info_Hanzi_In_Master_Card_but_Not_in_Slave, info_Total_Changes_Made_To_Master_Card,
        info_Distinct_Hanzi_In_Slave_Deck, info_Hanzi_In_Slave_Card_but_Not_in_Master))
    # convert frequency list to dict

    SlaveNoteToAdd = []
    for Slave_Hanzi_Not_in_Master in Slave_Hanzi_Dict:
        for HanziF in HanziFreqList:
            if HanziF[1] == Slave_Hanzi_Not_in_Master:
                SlaveNoteToAdd.append(HanziF + Slave_Hanzi_Dict.get(Slave_Hanzi_Not_in_Master))
                break

    showInfo("List of Hanzi_In_Slave_Card_but_Not_in_Master: %s" % str(Slave_Hanzi_Dict.keys()))
    showInfo("Now test add note")
    showInfo("note to add = %s " % str(SlaveNoteToAdd))
    # dummyNoteToAdd = [[6352,"糗","",99.98774599,"qiǔ","","(surname)/dryprovisions",36],[6353,"鸮","鴞",99.9877646,
    # "xiāo","","",36],[6354,"蕰","",99.9877832,"wēn","","",36],[6355,"坼","",99.9878018,"chè","","tocrack/split/break/tochap",36]]
    createAnkiNote(SlaveNoteToAdd, masterNoteModelFile)
    mw.progress.finish()
    mw.reset()


def setupMenu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('Bulk_Generate_learned_Hanzi_Cross_Indexing')
    a.triggered.connect(lambda _, b=browser: onBulkGenerateLearned_Hanzi_Cross_Indexing(b))


def onBulkGenerateLearned_Hanzi_Cross_Indexing(browser):
    BulkGenerateLearned_Hanzi_Cross_Indexing(browser.selectedNotes())


addHook("browser.setupMenus", setupMenu)
