### Katarzyna Pióro, Elektronika rok 2, AGH, WdTS
### Projekt na Raspberry Pi: Zagadka
from Gyroscope import read_turn
from screen import write_text
from time import sleep  # import
import random
#https://www.raspberrypi.org/documentation/usage/gpio/python/README.md
from gpiozero import LED, Button

#Lista dostępnych opcji
def switchCase(caseNum):
    turns = {
        1: "Up",
        2: "Down",
        3: "Right",
        4: "Left",
        5: "Nothing",
        6: "Do Nothing",
        7: "Not Up",
        8: "Not Down",
        9: "Not Right",
        10: "Not Left",
        11: "Not Nothing",
        12: "Not Not Up",
        13: "Not Not Down",
        14: "Not Not Right",
        15: "Not Not Left",
        16: "Not Not Nothing",
        17: "Whatever"
    }
    return turns.get(caseNum)

#Klucz do ułożenia kodu odpowiedzi
def findCorrect(display):
    turns = {
        "Up": "Up",
        "Down": "Down",
        "Right": "Right",
        "Left": "Left",
        "Nothing": "Nothing",
        "Do Nothing": "Nothing",
        "Not Up": "Up", ##WYMAGA ZAPRZECZENIA
        "Not Down": "Down", ##WYMAGA ZAPRZECZENIA
        "Not Right": "Right", ##WYMAGA ZAPRZECZENIA
        "Not Left": "Left", ##WYMAGA ZAPRZECZENIA
        "Not Nothing": "Nothing", ##WYMAGA ZAPRZECZENIA
        "Not Not Up": "Up",
        "Not Not Down": "Down",
        "Not Not Right": "Right",
        "Not Not Left": "Left",
        "Not Not Nothing": "Nothing",
        "Whatever": "Nothing"  ##WYMAGA ZAPRZECZENIA
    }
    return turns.get(display)

#Świecenie diod
def LEDs(int):
    led_r = []
    led_g = []
    led_r.append(LED(17)) #czerwone
    led_r.append(LED(27)) #czerwone
    led_g.append(LED(22)) #zielone
    led_g.append(LED(23)) #zielone
    j=0
    while j<9000:
        for i in range(2):
            if(int==1):
                led_g[i].on()
            elif(int==2):
                led_r[i].on()
        j=j+1
    led_g[i].off()
    led_r[i].off()


negative = ["Not Up", "Not Down", "Not Right", "Not Left", "Not Nothing", "Whatever"] #Polecenia dla których inny jest klucz/zasada odczytywania kodu
randNum = []
randomArray_display = []
randomArray_code = []
button = []
restart = True
#---------------------------------Nowa gra---------------------------------
#Nieskończona pętla dopóki użytkownik nie odmówi zagrania w kolejną grę
while(restart==True):
    for j in range(8):
        randNum.append(random.randint(1,17)) #generowanie losowego kodu
        randomArray_display.append(switchCase(randNum[j])) #odczytanie polecen do gry wyświetlanych na ekranie przypisanych do liczb
        randomArray_code.append(findCorrect(randomArray_display[j])) #stworzenie kodu poprawnych odpowiedzi


    i = 0
    stop1=False
    dobrze=False

    #Reagowanie na czynności użytkownika i porównywanie ich z kodem
    while(stop1==False):
        write_text("", 0, True) #czysczenie ekranu
        write_text(randomArray_display[i], 8, True)

        ruch = read_turn()

        ## Porównywanie wykonanego ruchu z kodem
        #klucz1 do kodu
        if (randomArray_display[i] == randomArray_code[i]): #czy display i code sa takie same
            if (ruch == randomArray_code[i]): #TAK - kod i ruch użytkownika mają taką samą nazwę
                dobrze = True
            else:
                dobrze = False #Wykonano niepoprawny ruch
                # koniec
        else: # NIE - sprawdzmy czy klucz do kodu sie zmieni
            stop2 = False
            for k in range(5):
                if(randomArray_display[i] == negative[k]):#czy wyświetlane polecenie należy do "podchwytliwych"
                    # klucz2 do kodu
                    if (ruch != randomArray_code[i]):  # TAK - podchywytliwe polecenie: wykonano jakikolwiek ruch oprócz zapisanego w kodzie
                        dobrze = True
                        stop2 = True
                        break
            if (stop2 != True) and (ruch == randomArray_code[i]): # NIE - polecenie nie należy do "podchwytliwych", polecenie powinno byc identyczne jak kod
                # klucz1 do kodu
                dobrze = True
                # koniec
            elif (stop2 != True): #Wykonano niepoprawny ruch
                dobrze = False
                # koniec

        if dobrze==True:
            write_text("Correct!", 16, True)
            LEDs(1) #świecenie diod zielonych /Ciąg dalszy
            #grasz dalej
        else:
            write_text("Game over", 16, True) #świecenie diod czerwonych /Przegrana
            LEDs(2)
            stop1 = True
            break

        #Jeśli nie przegrano, to sprawdź warunek zakończenia
        if i==7: #Maksymalnie 8 prób w ciagu jednej gry
            break
        else:
            i=i+1


    #Czy chcesz zagrać ponownie?
    write_text("Play again?", 8, False)
    sleep(1)
    write_text("B1=Yes, B4=No", 16, False)
    sleep(2)
    #Przypisanie przycisków na listę zmiennych
    button.append(Button(6))
    button.append(Button(13))
    button.append(Button(19))
    button.append(Button(26))
    #Nieskonczona pętla, ktora moze zostać przerwana tylko przycisnięciem odpowiedniego przycisku
    while True:
        if button[0].is_pressed: #przycisk B1
            restart = True
            break
        elif button[3].is_pressed: #przycisk B4
            restart = False
            write_text(" ", 0, True)  # czysczenie ekranu
            break

