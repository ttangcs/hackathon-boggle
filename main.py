import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import string
import time


class TrieNode:
  def __init__(self, value = "", isRoot=False):
      self.childNodes = []
      self.char = value
      self.isRoot = isRoot
      self.isEndOfWord = False

  def getChildNode(self, string):
    if len(string) > 1:
      try:
        return self.getChildNode(self.childNodes[[ node.char for node in self.childNodes ].index(string[:1])], string[1:])
      except:
        return self

    try:
      return self.childNodes[[ node.char for node in self.childNodes ].index(string)]
    except:
      return self

class Trie:
  def __init__(self):
    self.root = TrieNode(isRoot=True)

  def _contains(self, childNodes, char):
    for node in childNodes:
      if (node.char == char):
        return True
    return False

  def insertWord(self, word):
    currentNode = self.root
    for char in list(word.lower()):
      if not self._contains(currentNode.childNodes, char):
        currentNode.childNodes.append(TrieNode(char))
      currentNode = currentNode.childNodes[[ node.char for node in currentNode.childNodes].index(char)]
    currentNode.isEndOfWord = True
    


# Build Word Trie
trie = Trie()
file = open("./words.txt", "r")
wordLines = file.read().splitlines()
allowedChars = set(string.ascii_lowercase)

for word in wordLines:
  if len(word) >= 3 and set(word) <= allowedChars:
    trie.insertWord(word)



driver = webdriver.Chrome()
driver.get("http://flooreight.com/boggle/")

# Start the game
startElement = driver.find_element(By.XPATH, "//button[text()='Start']")
inputElement = driver.find_element(By.TAG_NAME, "input")
enterElement = driver.find_element(By.XPATH, "//button[text()='Ok']")

grid = []
gridRowElements = driver.find_elements(By.CLASS_NAME, "boggle-board__row")

startElement.click()

def getRowCharacters(rowElement):
  characterArray = []
  for colElement in rowElement.find_elements(By.CLASS_NAME, "boggle-board__cell"):
    characterArray.append(colElement.text.lower())

  return characterArray

def inBoundsAndNotVisited(rowIdx, columnIdx, usedGrid):
  if not 0 < rowIdx < maxRows:
    return False
  if not 0 < columnIdx < maxColumns:
    return False
  if usedGrid[rowIdx][columnIdx]:
    return False
  return True


def searchWord(currentNode, rowIdx, columnIdx, usedGrid, wordString, words):
  # print(wordString)
  # print("currentNode", currentNode.char, currentNode.isEndOfWord)
  # print("currentNode children", [node.char for node in currentNode.childNodes])
  # usedGrid[rowIdx][columnIdx] = True
  if currentNode.isEndOfWord:
    words.add(wordString)

  # usedGrid[rowIdx][columnIdx] = True # Set the letter visited
  if inBoundsAndNotVisited(rowIdx - 1, columnIdx - 1, usedGrid): # Up and Left
    character = grid[rowIdx - 1][columnIdx - 1]
    childNode = currentNode.getChildNode(character)
    if childNode != currentNode:
      words.update(searchWord(childNode, rowIdx - 1, columnIdx - 1, usedGrid, wordString + character, words))

  if inBoundsAndNotVisited(rowIdx - 1, columnIdx, usedGrid): # Up
    character = grid[rowIdx - 1][columnIdx]
    childNode = currentNode.getChildNode(character)
    if childNode != currentNode:
      words.update(searchWord(childNode, rowIdx - 1, columnIdx, usedGrid, wordString + character, words))

  if inBoundsAndNotVisited(rowIdx - 1, columnIdx + 1, usedGrid): # Up and Right
    character = grid[rowIdx - 1][columnIdx + 1]
    childNode = currentNode.getChildNode(character)
    if childNode != currentNode:
      words.update(searchWord(childNode, rowIdx - 1, columnIdx + 1, usedGrid, wordString + character, words))

  if inBoundsAndNotVisited(rowIdx, columnIdx - 1, usedGrid): # Left
    character = grid[rowIdx][columnIdx - 1]
    childNode = currentNode.getChildNode(character)
    if childNode != currentNode:
      words.update(searchWord(childNode, rowIdx, columnIdx - 1, usedGrid, wordString + character, words))

  if inBoundsAndNotVisited(rowIdx, columnIdx + 1, usedGrid): # Right
    character = grid[rowIdx][columnIdx + 1]
    childNode = currentNode.getChildNode(character)
    if childNode != currentNode:
      words.update(searchWord(childNode, rowIdx, columnIdx + 1, usedGrid, wordString + character, words))

  if inBoundsAndNotVisited(rowIdx + 1, columnIdx - 1, usedGrid): # Down and Left
    character = grid[rowIdx + 1][columnIdx - 1]
    childNode = currentNode.getChildNode(character)
    if childNode != currentNode:
      words.update(searchWord(childNode, rowIdx + 1, columnIdx - 1, usedGrid, wordString + character, words))

  if inBoundsAndNotVisited(rowIdx + 1, columnIdx, usedGrid): # Down
    character = grid[rowIdx + 1][columnIdx]
    childNode = currentNode.getChildNode(character)
    if childNode != currentNode:
      words.update(searchWord(childNode, rowIdx + 1, columnIdx, usedGrid, wordString + character, words))

  if inBoundsAndNotVisited(rowIdx + 1, columnIdx + 1, usedGrid): # Down and Right
    character = grid[rowIdx + 1][columnIdx + 1]
    childNode = currentNode.getChildNode(character)
    if childNode != currentNode:
      words.update(searchWord(childNode, rowIdx + 1, columnIdx + 1, usedGrid, wordString + character, words))
  return words
  
# Get the grid
for rowElement in gridRowElements:
  grid.append(getRowCharacters(rowElement))

maxRows = len(grid)
maxColumns = len(grid[0])
words = set()

for rowIndex in range(maxRows):
  for columnIndex in range(maxColumns):
    wordString = ""
    usedGrid = [[False] * (maxColumns)] * (maxRows)
    searchWord(trie.root.getChildNode(grid[rowIndex][columnIndex]), rowIndex, columnIndex, usedGrid, wordString + grid[rowIndex][columnIndex], words)


printString = ""
print(words)

print(grid)


for word in words:
  inputElement.send_keys(word)
  enterElement.click()
  if inputElement.get_attribute("class") == "invalid":
    inputElement.clear()

while (EC.)