import re
import pytesseract
import io
from PIL import Image, ImageGrab, ImageEnhance, ImageFilter, ImageOps
import tempfile
import pyperclip
import requests
from mtgsdk import Card
import pyautogui
import time
import subprocess
import webbrowser
#need to make multiple profiles if else on image alterations if no match text.
def cardlabelExtract():
    clipboardImage = ImageGrab.grabclipboard()

    if clipboardImage:
        image = clipboardImage
        enhancer = ImageEnhance.Contrast(clipboardImage)
        image = enhancer.enhance(3)
        enhancer = ImageEnhance.Brightness(clipboardImage)
        image = enhancer.enhance(9)

        width, height = image.size
        right_crop = (width * 3) // 6
        bottom_two_thirds = (height * 2) // 3
        # cropped_image = image.crop((0, 0, width - right_crop, height - bottom_two_thirds))
        cropped_image = image.crop((0, 0, width - right_crop, height - bottom_two_thirds))
    #fixme below may meed to change to separate function
        ## sm  adjusted variable for "image" and clipboard data
        text = pytesseract.image_to_string(cropped_image, lang='eng', config='--psm 6')
        lines = text.split('\n')
        if lines:
            first_line = lines[0].strip()
        return  first_line
        print(first_line)

def cardlabelExtractTwo():
    clipboardImage = ImageGrab.grabclipboard()

    if clipboardImage:
        image = clipboardImage
        enhancer = ImageEnhance.Contrast(clipboardImage)
        image = enhancer.enhance(3)
        enhancer = ImageEnhance.Brightness(clipboardImage)
        image = enhancer.enhance(9)

        width, height = image.size
        right_crop = (width * 4) // 6
        bottom_two_thirds = (height * 5) // 6
        # cropped_image = image.crop((0, 0, width - right_crop, height - bottom_two_thirds))
        cropped_image = image.crop((0, 0, width - right_crop, height - bottom_two_thirds))
    #fixme below may meed to change to separate function
        ## sm  adjusted variable for "image" and clipboard data
        text = pytesseract.image_to_string(cropped_image, lang='eng', config='--psm 6')
        lines = text.split('\n')
        if lines:
            first_line = lines[0].strip()
        return  first_line
        print(first_line)
####
test_Extract = cardlabelExtract()
print (test_Extract)
####
def cardWords(cardName):
    alpha_words = re.sub(r'[^a-zA-Z\s]', '', cardName)
    split_words = alpha_words.split(" ")

    return split_words

   # if len(sep_words) >= 3:
       # firstWord = list(sep_words[0])
       # firstWordStr = ''.join(filter(str.isalpha, list(sep_words[0])))
       # secondWord = list(sep_words[1])
       # secondWordstr = ''.join(filter(str.isalpha, list(sep_words[1])))
        #thirdWord = list(sep_words[2])
        #thirdWordstr = ''.join(filter(str.isalpha, list(sep_words[2])))
#adjusting so that we get all 3 in a set, when i call this from another funciton i should be able to select one at a time and repeat that funciton itterating through the set. resulting in each word matches listed one  after the other
    #return firstWordStr,secondWordstr,thirdWordstr
###
#FIXME dec 12 last edit trhing to have it run a second time with different alteration  if index error or not a good text capture
stringwords = cardWords(test_Extract)

print(stringwords)
if IndexError:
    #stringwords = cardWords(test_Extract)
    test_Extract = cardlabelExtractTwo()
    stringwords = cardWords(test_Extract)
    print(test_Extract)


### cardsmatch brings a list of matching cards from the database
def cardsmatch(cardName):
    cards = Card.where(name=cardName).all()
    card_data = {}
    count = 0
# count numbers for each line for each card match found. may use this as a function down the road to select.
    for card in cards:
        card_data[count] = card
        count += 1

        print(count,
              f" ID: {card.id},"
              f"Multiverse ID: {card.multiverse_id}, Name: {card.name}, Set Name: {card.set_name}, Set: {card.set}, Image URL: {card.image_url}, "
              f"Mana Cost: {card.mana_cost}, Type: {card.type}, Supertypes: {card.supertypes}, Subtypes: {card.subtypes}, "
              f"Variations: {card.variations}, Text: {card.text}, Colors: {card.colors}, Artist: {card.artist}, "
              f"Toughness: {card.toughness}, Power: {card.power}, Set Name: {card.set_name}, Border: {card.border},mana: {card.mana_cost} , converted Mana:{card.cmc}"
              f"Rarity: {card.rarity}, colors {card.colors} "
              )
#for each card in cards are made of (card_data function on (count parameters
    for card in cards:
        card_data[count] = card
    print(cards)

url = 'https://api.magicthegathering.io/v1/cards'
response = requests.get(url)

if response.status_code == 200:
    print("Thumbs Up")

searchResultall = cardsmatch
if cardsmatch(stringwords[1]):
    searchResult = cardsmatch(stringwords[1])
    print(searchResult)
else:
    print(searchResultall)
if cardsmatch(stringwords[0]):
    searchResultwo = cardsmatch(stringwords[0])
    print(searchResultwo)
else:
    print(searchResultall)

#tested with "lava Axe" with success.

def selectedCard(cardIDinput):
    url = 'https://api.magicthegathering.io/v1/cards'
    response = requests.get(url)
    #selected_count = input("Type ID of the matching card: ")
    card = Card.find(cardIDinput)
    card_list = (
        f" Magic the Gathering MTG single card {card.name}, {card.set_name}, {card.colors}, {card.rarity}"
    )
    #removed  Image URL: {card.image_url}, from card descripton to avoid mercari having an issue with the link to it
    card_description = (
        f" Magic the Gathering MTG single card {card.name} "
        f"{card.set_name}, {card.colors} ,{card.rarity},{card.set_name},"
        f"Mana Cost: {card.mana_cost}, Type: {card.type}, {card.supertypes}, {card.subtypes}, "
        f"Text: {card.text}, Colors: {card.colors}, Artist: {card.artist}, "
        f"Toughness: {card.toughness}, Power: {card.power}, Border: {card.border},mana: {card.mana_cost} , converted Mana:{card.cmc}"
    )
    card_hash = (
        f" MTG {card.name}) "
        f"{card.set_name} ,{card.colors} ,{card.rarity} ,{card.set_name}, {card.set}, "
        f"Mana Cost: {card.mana_cost}, Type: {card.type}, Subtypes: {card.subtypes}, "
        f"Text: {card.text}, Colors: {card.colors}, Artist: {card.artist}, "
        f"Toughness: {card.toughness}, Power: {card.power}, Border: {card.border},mana: {card.mana_cost} , converted Mana:{card.cmc}"
    )
    card_color = (f"{card.colors}"
                  )
    card_pricesearch = (f"{card.name},{card.set_name}"
                        )
    return card_list, card_description, card_hash, card_color, card_pricesearch
selected_count = input("Type ID of the matching card: ")
cardDatas = selectedCard(selected_count)
print("Go to Safari / Mercari and click complete draft for this image copy the adress")
def bring_safari_front(url):
    applescript = f"""
    tell application "Safari"
        activate
        tell application "Safari"
            make new document at end of documents
            set URL of document 1 to "{url}"
        end tell
    end tell
    """
    subprocess.run(["osascript", "-e", applescript])

draft_url = input("Enter the URL or press Enter to continue: ")
print (draft_url)

bring_safari_front(draft_url)

#pyautogui.press('Enter')
time.sleep(6)

def subjectfillprocess(cardDatas):
    # trying to stop it from asking input again keep 1st input
    #card_list, card_description, card_hash, card_color, card_pricesearch = selectedCard(selected_count)
    #time.sleep(2)
   #selected_card_info = f"{card_list}\n{card_description}\n{card_hash}\n{card_color}\n{card_pricesearch}"  # Writing the selected card information to a temporary file
    card_list, card_description, card_hash, card_color, card_pricesearch = cardDatas
    #load web page , then you need to click on white space in web page to position tab , this may also tab from we adress in future itterations
    time.sleep(6)
    #pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    # pyperclip.paste(file_content)
    pyperclip.copy(card_list)
    pyautogui.hotkey('command', 'v')
    time.sleep(2)
    pyautogui.press('tab')
    time.sleep(1)
    pyperclip.copy(card_description)
    pyautogui.hotkey('command', 'v')
    pyautogui.press('tab')
    time.sleep(1)
    pyperclip.copy(card_hash)
    pyautogui.hotkey('command', 'v')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.press('s')
    pyautogui.press('enter')
    pyautogui.press('tab')
    brand = "Wizards of the Coast"
    # pyperclip.copy(brand)
    # pyperclip.paste(brand)
    pyautogui.write(brand)
    pyautogui.press('down')
    pyautogui.press('enter')

    pyautogui.press('tab')  # on color box
    pyautogui.press('enter')  # opens drop down
    # test
    pyautogui.write("r")
    pyautogui.press('enter')
    pyautogui.press('tab')  # shipping box

    colors_info = card_color

    first_letter = colors_info[0]
    #test to proof first letter
    print (first_letter)

    pyautogui.write(first_letter)
    pyautogui.press('enter')

    pyautogui.press('tab')  # shipping box
    pyautogui.press('tab')  # shipping box 2
    #pyautogui.press('tab')  # shipping box 3 " buyer pays("t"")
    #pyautogui.press('enter')
    #if pyautogui.press('t'):  # test
        #print("t")  # test
    #pyautogui.press('t')

    #pyautogui.press(
      #  'enter')  #FIXME can tab strait to price and have user do shipping after this itwouls bethat last tab before tabgoes bak to top
    # or  navigage through shipping  ( !!!unsolved automation with pop ups!!)
    #pyautogui.press('shift+tab')  # back to shipping box 2
    #pyautogui.press('shift+tab')  # back to shipping box 1
    #time.sleep(2)
    # current_position = pyautogui.position()
    # pyautogui.click(current_position) #click on shipping carrier
    # pyautogui.press('tab')#tabs into pop up
    # pyautogui.press('0')#left weight lbs
    # pyautogui.press('tab')
    # pyautogui.press('1')# right weitgh oz ( over 1 oz price goes up)
    # user has to click through pop up fill weight x out  or click out second pop up
    # 2 pop ups
    #pyautogui.press(
     #   'tab')  # to price , run safari window to google price on selected card use manually chooses price
    # pricing
    # open safari window to look up price  app will auto search this card
    print(card_pricesearch)
    pyperclip.copy(card_pricesearch)
    print("type price")

#loop to keep automation in the safari window that is input
#autocheck = safariWindowCurrent()


oktofill = input("type  enter key to fill")
if not oktofill.strip():
    applescript = f"""
                tell application "Safari"
                    activate
                    end tell"""
    subprocess.run(["osascript", "-e", applescript])

    subjectfillprocess(cardDatas)




#using enter key but later plan for a button


#fixme the automation can error by clicking or tabbing through other applications or system buttons that I do not want it having access to , how can I loop a check while using pyautogui commands  so that they are only happening while the safari page is open and they do not have access to the operating system commands  or top bar menus.  ?