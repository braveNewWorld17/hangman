from flask import Flask
from flask import request
import random
app = Flask(__name__)

HANGMANPICS = ['''

<br>  +---+
<br>  |   |
<br>      |
<br>      |
<br>      |
<br>      |
<br>=========''', '''

<br>  +---+
<br>  |   |
<br>  O   |
<br>      |
<br>      |
<br>      |
<br>=========''', '''

<br>  +---+
<br>  |   |
<br>  O   |
<br>  |   |
<br>      |
<br>      |
<br>=========''', '''

<br>  +---+
<br>  |   |
<br>  O   |
<br> /|   |
<br>      |
<br>      |
<br>=========''', '''

<br>  +---+
<br>  |   |
<br>  O   |
<br> /|\  |
<br>      |
<br>      |
<br>=========''', '''

<br>  +---+
<br>  |   |
<br>  O   |
<br> /|\  |
<br> /    |
<br>      |
<br>=========''', '''

<br>  +---+
<br>  |   |
<br>  O   |
<br> /|\  |
<br> / \  |
<br>      |
<br>=========''']

def getRandomWord(wordList):
    # This function returns a random string from the passed list of strings.
    wordIndex = random.randint(0, len(wordList) - 1)
    return wordList[wordIndex]

def displayHtml(HANGMANPICS, missedLetters, correctLetters, secretWord, gameScore, topScore):
    print('topScore = ', topScore)    
    htmlString = '<br>'
    htmlString += 'Top Score : ' + str(topScore)
    htmlString += '<br>'
    htmlString += 'Your Score : ' + str(gameScore)
    htmlString += '<br>'
    htmlString += HANGMANPICS[len(missedLetters)]
    htmlString += '<br>'
    htmlString += 'Missed letters : '

    missedLetters = ' '
    tmpLetters = ''
    for letter in missedLetters:
        tmpLetters += letter
        tmpLetters += ' '
    missedLetters += tmpLetters + '<br>'

    blanks = ''
    for i in range(len(secretWord)): # replace blanks with correctly guessed letters
        if secretWord[i] in correctLetters:
            blanks += secretWord[i]
        else:
            blanks += '_'

    missedLetters += blanks
    missedLetters += '<br>'

    for letter in blanks: # show the secret word with spaces in between each letter
        print('letter =  ', letter, end=' ')

    htmlString += missedLetters
    return htmlString 

def displayInputAgain(flagAgain):    
    inputString = """ 
    Guess a letter!<br>
    <input type='text' name = 'guessLetter' value=''> <br>
    <input type='submit' value='Submit'>
    """
    againString = """
    Do you want to play again? <br>
    <a href="/"> <button> Again </button> </a>
    """

    if flagAgain : return againString
    else : return inputString    

def checkInputGuess(alreadyGuessed, guess):

    returnString = ''
    if len(guess) != 1:
        returnString = 'Please enter a single letter. <br>'
    elif guess in alreadyGuessed:
        returnString = 'You have already guessed that letter. Choose again. <br>'
    elif guess not in 'abcdefghijklmnopqrstuvwxyz':
        returnString = 'Please enter a LETTER.'
    else:
        return returnString

def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

# Check if the player has won
def checkCorrectAnswer(correctLetters, secretWord):
    foundAllLetters = True
    for i in range(len(secretWord)):
        if secretWord[i] not in correctLetters:
            foundAllLetters = False
            break
    return foundAllLetters

# Check if player has guessed too many times and lost
def checkWrongAnswer(missedLetters, secretWord):
    # Check if player has guessed too many times and lost
    if len(missedLetters) == len(HANGMANPICS) - 1:
        return True
    return False

def readWordList(filename):
    file = open(filename, 'r')
    str = file.read()
    file.close()
    wordList = str.split()
    return wordList

def readScoreFile(filename):
    file = open(filename, 'r')
    topScore = file.read()
    file.close()
    return int(topScore)

def doScoreProcess(gameScore, topScore):
    if gameScore > int(topScore):
       print ("Congratulations!!! You got the highest score.")
       print ("Your score is ", gameScore, ".") 
       topScore = str(gameScore)
       strScore = str(gameScore)
       file = open('./score.txt', 'w')
       file.write(strScore)
       file.close()
    else :
       print ("Your score is ", gameScore, ".") 

    return topScore
	
html = """
<center>
    H A N G M A N by soyoung677 <br>
<form action='/result' method='POST'>
{htmlString}<br>
<input type='hidden' name = 'missedLetters' value='{missedLetters}'>
<input type='hidden' name = 'correctLetters' value='{correctLetters}'>
<input type='hidden' name = 'secretWord' value='{secretWord}'>
<input type='hidden' name = 'gameScore' value='{gameScore}'>
<input type='hidden' name = 'topScore' value='{topScore}'>
</form>
"""

@app.route("/")
def init():
    missedLetters = ''
    correctLetters = ''
    guessLetter = ''
    gameSucceeded = False
    gameFailed = False
    gameScore = 0
    topScore = readScoreFile('./score.txt')
    words = readWordList('./text.txt')
    secretWord = getRandomWord(words)

    htmlString = displayHtml(HANGMANPICS, missedLetters, correctLetters, secretWord, gameScore, topScore)
    htmlString += displayInputAgain(False)

    return html.format(htmlString = htmlString, missedLetters = missedLetters, correctLetters = correctLetters, secretWord = secretWord, gameScore = '0', topScore = topScore)

@app.route("/result", methods=['POST'])
def result():
    guessLetter = request.form["guessLetter"]
    missedLetters = request.form["missedLetters"]
    correctLetters = request.form["correctLetters"]
    secretWord = request.form["secretWord"]
    gameScore = int(request.form["gameScore"])
    topScore = int(request.form["topScore"])
    
    gameSucceeded = False
    gameFailed = False

    print('missedLetters = ', missedLetters)
    print('correctLetter = ', correctLetters)
    print('secretWord = ', secretWord)

    guessString = checkInputGuess(missedLetters + correctLetters, guessLetter)

    if guessLetter in secretWord:
      correctLetters = correctLetters + guessLetter
      print('correctLetter = ', correctLetters)
      gameSucceeded = checkCorrectAnswer(correctLetters, secretWord)
      gameScore += 3
    else:
      missedLetters = missedLetters + guessLetter
      gameFailed = checkWrongAnswer(missedLetters, secretWord)
      gameScore -= 1

    htmlString = displayHtml(HANGMANPICS, missedLetters, correctLetters, secretWord, gameScore, topScore)
    
    if gameSucceeded or gameFailed:
       if gameSucceeded:
          htmlString += '<br>' + 'Yes! The secret word is ' + secretWord + '! You have won!'
          topScore = doScoreProcess(gameScore, topScore)
       else:
          htmlString += '<br>' + 'You have run out of guesses!' + '<br> After ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"'

       htmlString += displayInputAgain(True)
    else : 
       htmlString += displayInputAgain(False)

    return html.format(htmlString = htmlString, missedLetters = missedLetters, correctLetters = correctLetters, secretWord = secretWord, gameScore = '0', topScore = topScore)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2323)


