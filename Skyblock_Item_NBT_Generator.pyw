import requests
import base64
import json
import os
import io
from mojang import API
from os.path import exists
from nbt.nbt import *
from os import path
import PySimpleGUI as ui
import traceback

fileDir = os.getcwd()
fileDir = fileDir.replace('\\', '/')
fileDir = fileDir + '/'

ui.theme('Dark')
ui.SetOptions(button_color=('#FFF', '#291f18'), background_color='#291f18')

MojangAPI = API()

button_image = 'iVBORw0KGgoAAAANSUhEUgAAAMgAAAAUCAMAAAD/eoL4AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAEgUExURQAAAP7+/fz8+fz8+vv79/v7+Pr69vf38Pb27/Pz7O7u5+rq4+bm3+Hh2tvb1NfX0dPTzM7OyMrKxMbGwMPDvcHBu729t7y8trm5tLe3sra2sbW1sLOzrrKyraaonv39/CIiHQwMCxYWE3J0bBoUDx8YE3N1bqSklyAgHB0WEiYdFykfGBENCk1OSBUVElpcVBwVETY2MTg4M1VUTdLRzOfn5CEZFCYmIXt6cBUQDEJBO4B/czM1Lzg3MmhnXvj49i0tKIKBdgkJCCwhGldYUScoJGJiWzUoH42Qhfr69RYWEmBhWhoaFpqalLy8t7u7tbi4sra2sLi4s76+uL+/ucLCvMTEvsjIws/Pydra09/f2OPj3Ofn4Ovr5CMkHQAAALGPZ7cAAABgdFJOU///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////AHNt5EMAAAAJcEhZcwAACxMAAAsTAQCanBgAAAGTSURBVFhH1ZfbVoJAFEBJ0e5pVgpC5RhUOkYWlGiZhKXZTe1+seb//6IzNKh9QZ7NggcWD3uvWcOaIzHGpiKRaFSOxePx6ZnZufmFxaVEcjm1srqWziiKoqpZTdN1fX0C4BKgouuaIMtRNyACQjZzBDn5LR4i54hhosYg+W0m7eySQpEOKWFB+HKKBbJnSfvEGO8oY+FPiXFgSYeWSantHDk2vCmVj7EQlITeZhhCK24FnrQqvsJAlQsLbxHiUFo7qVHqUDwLAksCvqE3Dzm1TNeu18/qddtFFjLyDkOchuM24MYWMvQOQ2qefW57NXQhQ28RYvu+d+L5vo0sZOQtQnzYNC5sGh9ZyMhbhMD/2HVc/j/GFTLyHob4HHjRxFNSboJv6G1eWNJla/yI0hYHgMmnLYwDjCtLIvnW+KGxjQXhG1DoXBOJkfwN9mN85JbwwQpK7tKceyDT7So9FYDxS4dL035ns/8CJtNgIuz3+2rvIfP49PzymnpLJt4/PgeDwZcsx6KRzjcJJkQm5izEMMZ+AM5B5lumv71NAAAAAElFTkSuQmCC'

CloseButton = [[ui.Button('Close', image_data=button_image, border_width=0)]]

Labels = [[ui.Text('Skyblock API Key:', background_color='#291f18')],
          [ui.Text('Username:', background_color='#291f18')],
          [ui.Text('Profile Selection:', background_color='#291f18')],
          [ui.Text('Inventory Selection:', background_color='#291f18')],
          [ui.Text('Backpack Selection:', background_color='#291f18')],
          [ui.Text('Item Slot in Inventory:', background_color='#291f18')]]
Inputs = [[ui.InputText(key='-apiKey-', tooltip='Example: 991cae91-f870-4972-b5ae-2829a2e20aac', size=(75, 1), background_color='#211914')],
          [ui.InputText(key='-username-', tooltip='Example: SyndiShanX', size=(75, 1), background_color='#211914')],
          [ui.InputText(key='-selectedProfile-', tooltip='Example: 1 (If this is empty it defaults to 1)', size=(75, 1), background_color='#211914')],
          [ui.InputText(key='-selectedInventory-', tooltip='Example: Armor', size=(75, 1), background_color='#211914')],
          [ui.InputText(key='-selectedBackpack-', tooltip='Example: 1 (Leave Blank if Backpack is not the Selected Inventory)', size=(75, 1), background_color='#211914')],
          [ui.InputText(key='-selectedSlot-', tooltip='Example: 1', size=(75, 1), background_color='#211914')]]
Buttons = [[ui.Button('Generate Item NBT', image_data=button_image, border_width=0)]]

layout = [[ui.Text('Inventory Options:', justification='center', background_color='#291f18')],
          [ui.Text('(Armor, Equipment, Backpack, Quiver, TalismanBag, EnderChest, Wardrobe, PotionBag, Vault, Inventory, or CandyInventory):', justification='center', background_color='#291f18')],
          [ui.Column(Labels), ui.Column(Inputs)],
          [ui.Column(Buttons, justification='center')],
          [ui.Text('Output Log:', justification='left', background_color='#291f18')],
          [ui.Output(size=(100, 10), background_color='#211914')],
          [ui.Column(CloseButton, justification='center')]]

window = ui.Window('Skyblock Item NBT Generator', layout).Finalize()

def getAPIJson(API_Key, username):
  UUID = MojangAPI.get_uuid(username)

  Skyblock_Player_Data = 'null'

  Skyblock_Player_Data = requests.get(
    url='https://api.hypixel.net/skyblock/profiles',
    params={
      'key': API_Key,
      'uuid': UUID,
      'name': username
    }
  ).json()

  f = open(fileDir + 'SkyblockPlayerData.json', 'w')
  f.write(decodeString(str(Skyblock_Player_Data).replace("'", '"').replace(': True', ': "True"').replace(': False', ': "False"').replace(': None', ': "None"')))
  f.close()

def decodeString(inputString):
  string_nonASCII = inputString
  string_encode = string_nonASCII.encode('ascii', 'ignore')
  string_decode = string_encode.decode()
  return str(string_decode.strip())
def decodeInventoryData(raw):
  data = NBTFile(fileobj=io.BytesIO(base64.b64decode(raw)))
  return data

def genItem(itemID, itemCount, isUnbreakable, hideFlags, loreStrings, tintColor, displayName, extraColor, bossID, ogOwnerUUID,
            itemModifier, originTag, hypixelID, enchantmentNames, enchantmentLevels, itemUUID, anvilUses, itemTimestamp,
            itemDamage):
  nbtfile = NBTFile()

  list_i = TAG_List(name='i', type=TAG_Compound)
  compound_main = TAG_Compound()
  if itemID is not None:
    compound_main.tags.append(TAG_Short(name='id', value=itemID))
  if itemCount is not None:
    compound_main.tags.append(TAG_Byte(name='Count', value=itemCount))

  compound_tag = TAG_Compound(name='tag')

  if isUnbreakable is not None:
    compound_tag.tags.append(TAG_Byte(name='Unbreakable', value=isUnbreakable))
  if hideFlags is not None:
    compound_tag.tags.append(TAG_Int(name='HideFlags', value=int(hideFlags)))

    compound_display = TAG_Compound(name='display')

  list_lore = TAG_List(name='Lore', type=TAG_String)
  list_lore.tags.append(TAG_String(str(loreStrings[0])))
  for i in range(1, len(loreStrings)):
    list_lore.tags.extend([TAG_String(str(loreStrings[i]))])
  compound_display.tags.append(list_lore)

  if tintColor is not None:
    compound_display.tags.append(TAG_Int(name='color', value=int(tintColor)))
  if displayName is not None:
    compound_display.tags.append(TAG_String(name='Name', value=str(displayName)))
  compound_tag.tags.append(compound_display)

  compound_attributes = TAG_Compound(name='ExtraAttributes')

  if extraColor is not None:
    compound_attributes.tags.append(TAG_String(name='color', value=str(extraColor)))
  if bossID is not None:
    compound_attributes.tags.append(TAG_String(name='bossId', value=str(bossID)))
  if ogOwnerUUID is not None:
    compound_attributes.tags.append(TAG_String(name='spawnedFor', value=str(ogOwnerUUID)))
  if itemModifier is not None:
    compound_attributes.tags.append(TAG_String(name='modifier', value=str(itemModifier)))
  if originTag is not None:
    compound_attributes.tags.append(TAG_String(name='originTag', value=str(originTag)))
  if hypixelID is not None:
    compound_attributes.tags.append(TAG_String(name='id', value=str(hypixelID)))

  if len(enchantmentNames) != 0:
    compound_enchantments = TAG_Compound(name='enchantments')
    for x in range(0, len(enchantmentNames)):
      compound_enchantments.tags.append(TAG_Int(name=str(enchantmentNames[x]), value=int(enchantmentLevels[x])))
    compound_attributes.tags.append(compound_enchantments)

  if itemUUID is not None:
    compound_attributes.tags.append(TAG_String(name='uuid', value=str(itemUUID)))
  if anvilUses is not None:
    compound_attributes.tags.append(TAG_String(name='anvil_uses', value=str(anvilUses)))
  if itemTimestamp is not None:
    compound_attributes.tags.append(TAG_String(name='timestamp', value=str(itemTimestamp)))

  if itemDamage is not None:
    compound_main.tags.append(TAG_Short(name='Damage', value=itemDamage))

  compound_tag.tags.append(compound_attributes)
  compound_main.tags.append(compound_tag)
  list_i.tags.append(compound_main)
  nbtfile.tags.append(list_i)

  nbtfile.write_file(str(hypixelID).title() + '.dat')

  if path.exists(str(hypixelID).title() + '.dat') == 1:
    print('"' + str(hypixelID).title() + '.dat" Successfully Generated!')

def getItemDetails(itemSource, itemIndex, profileIndex, backpackIndex, username):
  UUID = MojangAPI.get_uuid(username)

  SkyblockPlayerData = open(fileDir + 'SkyblockPlayerData.json')
  SkyblockPlayerJson = json.load(SkyblockPlayerData)

  if itemSource.lower() == 'armor':
    selectedSource = SkyblockPlayerJson['profiles'][int(profileIndex)]['members'][str(UUID)]['inv_armor']['data']
  elif itemSource.lower() == 'equipment':
    selectedSource = SkyblockPlayerJson['profiles'][int(profileIndex)]['members'][str(UUID)]['equippment_contents']['data']
  elif itemSource.lower() == 'backpack':
    selectedSource = SkyblockPlayerJson['profiles'][int(profileIndex)]['members'][str(UUID)]['backpack_contents'][backpackIndex]['data']
  elif itemSource.lower() == 'quiver':
    selectedSource = SkyblockPlayerJson['profiles'][int(profileIndex)]['members'][str(UUID)]['quiver']['data']
  elif itemSource.lower() == 'talismanbag':
    selectedSource = SkyblockPlayerJson['profiles'][int(profileIndex)]['members'][str(UUID)]['talisman_bag']['data']
  elif itemSource.lower() == 'enderchest':
    selectedSource = SkyblockPlayerJson['profiles'][int(profileIndex)]['members'][str(UUID)]['ender_chest_contents']['data']
  elif itemSource.lower() == 'wardrobe':
    selectedSource = SkyblockPlayerJson['profiles'][int(profileIndex)]['members'][str(UUID)]['wardrobe_contents']['data']
  elif itemSource.lower() == 'potionbag':
    selectedSource = SkyblockPlayerJson['profiles'][int(profileIndex)]['members'][str(UUID)]['potion_bag']['data']
  elif itemSource.lower() == 'vault':
    selectedSource = SkyblockPlayerJson['profiles'][int(profileIndex)]['members'][str(UUID)]['personal_vault_contents']['data']
  elif itemSource.lower() == 'inventory':
    selectedSource = SkyblockPlayerJson['profiles'][int(profileIndex)]['members'][str(UUID)]['inv_contents']['data']
  elif itemSource.lower() == 'candyinventory':
    selectedSource = SkyblockPlayerJson['profiles'][int(profileIndex)]['members'][str(UUID)]['candy_inventory_contents']['data']

  if len(str(selectedSource).split('H4sIAAAAAAAAAONiYOBkYMzkYmBg')) == 2:
    print('Selected Source is Empty')
  else:
    itemNBT = decodeInventoryData(selectedSource)
    item = itemNBT['i'][int(itemIndex)]
    itemTag = item.get('tag')
    if item.get('id') is not None:
      itemID = item.get('id').value
    else:
      itemID = None
    if item.get('Count') is not None:
      itemCount = item.get('Count').value
    else:
      itemCount = None
    if itemTag.get('Unbreakable') is not None:
      isUnbreakable = itemTag.get('Unbreakable').value
    else:
      isUnbreakable = None
    if itemTag.get('HideFlags') is not None:
      hideFlags = itemTag.get('HideFlags').value
    else:
      hideFlags = None
    lore = item.get('tag').get('display').get('Lore')
    loreStrings = []
    for i in range(0, len(lore)):
      loreStrings.append(lore[i])
    if item.get('tag').get('display').get('color') is not None:
      tintColor = item.get('tag').get('display').get('color').value
    else:
      tintColor = None
    displayName = item.get('tag').get('display').get('Name')
    if item.get('tag').get('ExtraAttributes').get('color') is not None:
      extraColor = item.get('tag').get('ExtraAttributes').get('color').value
    else:
      extraColor = None
    if item.get('tag').get('ExtraAttributes').get('bossId') is not None:
      bossID = item.get('tag').get('ExtraAttributes').get('bossId').value
    else:
      bossID = None
    if item.get('tag').get('ExtraAttributes').get('spawnedFor') is not None:
      ogOwnerUUID = item.get('tag').get('ExtraAttributes').get('spawnedFor').value
    else:
      ogOwnerUUID = None
    itemModifier = item.get('tag').get('ExtraAttributes').get('modifier')
    originTag = item.get('tag').get('ExtraAttributes').get('originTag')
    hypixelID = item.get('tag').get('ExtraAttributes').get('id')
    if item.get('tag').get('ExtraAttributes').get('enchantments') is not None:
      enchantments = item.get('tag').get('ExtraAttributes').get('enchantments')
      enchantmentNames = []
      enchantmentLevels = []
      for x in range(0, len(enchantments)):
        enchantmentNames.append(enchantments[x].name)
        enchantmentLevels.append(enchantments[x].value)
    else:
      enchantmentNames = []
      enchantmentLevels = []
    itemUUID = item.get('tag').get('ExtraAttributes').get('uuid')
    if item.get('tag').get('ExtraAttributes').get('anvil_uses') is not None:
      anvilUses = item.get('tag').get('ExtraAttributes').get('anvil_uses').value
    else:
      anvilUses = None
    itemTimestamp = item.get('tag').get('ExtraAttributes').get('timestamp')
    itemDamage = item.get('Damage').value
    genItem(itemID, itemCount, isUnbreakable, hideFlags, loreStrings, tintColor, displayName, extraColor, bossID, ogOwnerUUID,
            itemModifier, originTag, hypixelID, enchantmentNames, enchantmentLevels, itemUUID, anvilUses, itemTimestamp,
            itemDamage)

while True:
  event, values = window.read()
  if event in (ui.WIN_CLOSED, 'Close'):
    break
  if event == 'Generate Item NBT':
    try:
      if int(values['-selectedSlot-']) - 1 < 0:
        selectedSlot = 0
      else:
        selectedSlot = int(values['-selectedSlot-']) - 1
      try:
        try:
          if int(values['-selectedProfile-']) - 1 < 0:
            selectedProfile = 0
          else:
            selectedProfile = int(values['-selectedProfile-']) - 1
        except IndexError:
          print('Error: Selected Profile does Not Exist')
      except ValueError:
        None
      if type(values['-selectedProfile-']) == str:
        getAPIJson(values['-apiKey-'], values['-username-'])
        SkyblockPlayerData = open(fileDir + 'SkyblockPlayerData.json')
        SkyblockPlayerJson = json.load(SkyblockPlayerData)
        for x in range(0, len(SkyblockPlayerJson['profiles'])):
          if SkyblockPlayerJson['profiles'][x]['cute_name'] == values['-selectedProfile-']:
            selectedProfile = x
      try:
        getItemDetails(values['-selectedInventory-'], selectedSlot, selectedProfile, values['-selectedBackpack-'], values['-username-'])
      except NameError:
        print('Profile Name "' + values['-selectedProfile-'] + '" Not Found')
    except IndexError:
      print('Error: Selected Slot does Not Exist')
    except KeyError:
      traceback.print_exc()
      print('Error: Selected Backpack does Not Exist')
window.close()