from tkinter import *
from tkinter import ttk
import random

button_width = 17
number_of_characters_per_row = 56
diff_for_answers = number_of_characters_per_row - 13 # da je prostor še za slikico prav/narobe

import subprocess  # poskusile 5 razlicnih modulov: pyglet, mp3play, sound in se dva pa noben ni delal


# pygame se nama zdi prevelika knjiznica za dodati za samo nekaj zvokov
def play_button_click():  # dela samo na OS X!
    subprocess.call(["afplay", "Sounds/button_click.mp3"])
    # dela prepočasi!! - ko to dela, ne dela nič drugo!

# lahko bi dodali glasbo v ozadju:
# subprocess.call(["afplay", "music.mp3"]) # vendar ce to igram, potem nic drugo ne dela dokler se glasba ne konca!

import gettext

en = gettext.translation('main', localedir='locale', languages=['en'])
en.install()



class Quiz(Tk):
    frames = {} # vsi frami z vprasanji
    number_of_questions = 5
    question_count = 0
    number_of_all_questions = 20  # per subject in SUBJECTdata.txt
    points = 0  # number of points user gets for answering the question correctly
    translation_language = "SL" # privzet jezik

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.wm_title(self, _("Maturitetni kviz"))

        self.initialize_container_frame()
        self.initialize_start_page()

        self.set_images()
        self.create_translation_button()

    def initialize_container_frame(self):
        self.container = ttk.Frame(self)  # to je frame, ki nima na sebi nič, na njega zlagama nove
        self.container.pack_propagate(0) # da ne nastavi sam velikosti ampak lahko dolocis sam
        self.container.pack(pady=10, padx=10)

        self.container.grid_rowconfigure(0, weight=1)
        # default weight je 0, kar pomeni da bo ta imel najvecji prostor ko spremenimo velikost - zaenkrat nima veze ker je sam
        self.container.grid_columnconfigure(0, weight=1)

    def initialize_start_page(self):
        start_page = StartPage(self.container, self)
        start_page.grid(row=0, column=0, sticky="nsew")
        self.frames[0] = start_page
        self.show_frame()

    def show_frame(self):
        if self.question_count <= self.number_of_questions:
            frame = self.frames.get(self.question_count, None)  # da slucajno ne pride do zrusitve programa
            if frame is not None:
                frame.tkraise()  # naloži nov frame - vprašanje
            else:
                print(_("Nekaj se je zalomilo. Vprasanja ni bilo mogoče naložiti"))
            self.question_count += 1
        else:
            self.show_result_frame()

    def set_subject(self, subject):
        self.create_random_questions(subject)
        self.show_frame()
        play_button_click()

    def create_random_questions(self, subject):
        random_question_numbers = []
        table_of_possible_question_numbers = list(
            range(1, self.number_of_all_questions + 1))  # iti more od 1 do vkljucno stevila

        # tu samo dolocimo random stevilke vprasanj, stevilka pomeni vrstica v dokumentu:
        while len(random_question_numbers) < self.number_of_questions:
            rand_number = random.choice(table_of_possible_question_numbers)
            random_question_numbers.append(rand_number)

            if rand_number in table_of_possible_question_numbers:
                table_of_possible_question_numbers.remove(rand_number)
            else:
                print(_("Pri določanju tvojih vprašanj se je zalomilo."))  # spet da slucajno ne pride do zrusitve

        # nalozimo dejanska vprasanja, prikazemo zaenkrat se nobenega:
        question_count = 1  # to ni lastnost metode self.question_count, ampak nova spremenljivka
        for number in random_question_numbers:
            question = Question(self.container, self, subject, number)
            self.frames[question_count] = question
            question_count += 1
            question.grid(row=0, column=0, sticky="nsew")

    def show_result_frame(self):
        result_page = ResultPage(self.container, self)
        result_page.grid(row=0, column=0, sticky="nsew")
        result_page.tkraise()

        # ponastavimo rezultate, ce bo slucajno igral ponovno:
        self.question_count = 0
        self.points = 0
        self.destroy_previous_frames()  # da se nam spomin ne zabase

    def destroy_previous_frames(self):
        for frame in self.frames.values():
            frame.destroy()
        self.frames = {}

    def increase_points(self):
        self.points += 1

    def set_images(self):
        self.correct_photo = PhotoImage(file="Images/correct.gif")
        Label(self, image=self.correct_photo)
        self.wrong_photo = PhotoImage(file="Images/wrong.gif")
        Label(self, image=self.wrong_photo)

    def create_translation_button(self):
        self.translation_button = ttk.Button(self, text="EN",
                                            command=self.change_translation_language,
                                            width=button_width)

    def change_translation_language(self):
        self.translation_language = "SL" if self.translation_language == "EN" else "EN"

        # Update button text:


class StartPage(ttk.Frame):  # podeduje metode in lastnosti razreda
    def __init__(self, parent, quiz_reference):  # self je container - vse se bo nalagalo na container
        ttk.Frame.__init__(self, parent)
        self.quiz_reference = quiz_reference

        self.show_frame()

    def show_frame(self):
        translation_button = self.quiz_reference.translation_lanquage

        text = _('''Pozdravljen bodoči maturant!\nPred tabo je kratek kviz iz maturitetnih predmetov\n''')
        ttk.Label(self, text=text, justify="center").pack(padx=10)

        self.show_image()

        ttk.Label(self, text=_("Izberi področje:")).pack(pady=10, padx=10)

        button_geo = ttk.Button(self, text=_("Geografija"),
                               command=lambda: self.quiz_reference.set_subject("GEO"),
                               width=button_width)
        button_geo.pack(side="bottom")
        button_mat = ttk.Button(self, text=_("Matematika"),
                               command=lambda: self.quiz_reference.set_subject("MAT"),
                               width=button_width)
        button_mat.pack(side="bottom")
        # lambda uporabimo, da lahko podamo parameter in ob tem ne sprožimo klica funkcije

    def show_image(self):
        photo = PhotoImage(file="Images/slika.gif")
        label = ttk.Label(self, image=photo)

        self.start_page_image = photo  # treba je imeti se eno povezavo, zato da je avtomatsko ne izbrise
        label.pack()


#class HowManyQuestionsPage(ttk.Frame):  # vprasa uporabnika na koliko vprašanj želi odgovoriti
#    def __init__(self, parent, quiz_reference):  # self je container - vse se bo nalagalo na container
#        ttk.Frame.__init__(self, parent)


class Question(ttk.Frame):
    question = ""
    correct_answer = ""
    possible_answers = {} # mozno vprasanje : Radio button reference
    chosen_answer = ""
    is_confirm_button_showing = False

    def __init__(self, parent, quiz_reference, subject, number):  # ko imama stevilko, poiscema vprasanje, odgovor in mozne odgovore iz datoteke
        ttk.Frame.__init__(self, parent)

        self.quiz_reference = quiz_reference
        self.subject = subject
        self.number = number
        self.get_data()

        self.show_frame_widgets()

    def show_frame_widgets(self):
        self.show_the_question()
        self.show_possible_answers()

    def show_the_question(self):
        '''prikaze vprasanje na label widgetu'''
        ttk.Label(self, text=_(self.question)).pack(pady=15, padx=10, side="top")

    def check_if_text_too_long(self, unedited_text, allowed_number_of_chars=number_of_characters_per_row):
        '''vrne primerno preurejen text z novimi vrsticami, ce je trenutno predolg'''
        unedited_text = _(unedited_text) # translate the text
        if len(unedited_text) <= allowed_number_of_chars: return unedited_text  # je ze ok

        text = ''''''  # vecvrsticni string
        num_of_chars = 0  # in current row

        for word in unedited_text.split(" "):
            num_of_chars += len(word)
            if num_of_chars < allowed_number_of_chars:
                text += word + " "
            else:
                text = text + word + "\n"
                num_of_chars = 0
        return text.strip("\n")

    def show_possible_answers(self):
        self.radio_buttons = {}
        self.var = StringVar()
        for possible_answer in self.possible_answers:

            R = ttk.Radiobutton(self,
                                compound="right",
                                text=possible_answer,
                                variable=self.var,
                                value=possible_answer,
                                command=self.set_chosen_answer)
            # Ko uporabnik izbere odgovor, se mu prikaze gumb za potrditev, ko stisne nanj se preveri pravilnost izbire
            self.radio_buttons[possible_answer] = R
            R.pack(anchor='w', padx=15)

    def set_chosen_answer(self):
        if not self.is_confirm_button_showing: self.show_confirm_button()

    def show_confirm_button(self):
        self.confirm_button = ttk.Button(self, text=_("Potrdi izbiro"),
                                         command=self.check_the_answer,
                                         width=button_width)
        self.confirm_button.pack(pady=8, side="bottom")
        self.is_confirm_button_showing = True

    def check_the_answer(self):
        self.chosen_answer = self.var.get() # var je StringVar ne String!
        if self.chosen_answer == self.correct_answer: self.quiz_reference.increase_points()
        self.change_text_on_confirm_button()
        play_button_click()

    def change_text_on_confirm_button(self):
        self.confirm_button.destroy()
        self.next_q_button = ttk.Button(self,
                                        text=_("Naprej"),
                                        command=self.confirm_button_pressed,
                                        width=button_width)
        self.next_q_button.pack(pady=8, side="bottom", anchor="e")

        # prepreci da stisne na gumbe:
        for text, radio_button in self.radio_buttons.items():
            if text == self.chosen_answer:
                appropriate_image = self.quiz_reference.correct_photo if self.chosen_answer == self.correct_answer \
                    else self.quiz_reference.wrong_photo
                radio_button.configure(command=lambda: None, image=appropriate_image) # po tem še sicer pusti označiti
                # druge odgovore, vendar shrani jih več ne

    def confirm_button_pressed(self):
        play_button_click()
        self.quiz_reference.show_frame()


    def get_data(self):
        data =  "TextFiles/" + self.subject + "data.txt"

        with open(data, "r") as file:
            lines = [line.strip() for line in file]
            currentLine = lines[self.number]
            # zapisano v obliki Vprasanje;odg1:odg2:odg3;odgovorPravilen
            data = currentLine.split(";")
            self.question = self.check_if_text_too_long(data[0])
            self.correct_answer = self.check_if_text_too_long(data[2], diff_for_answers)
            self.possible_answers = [self.check_if_text_too_long(answer, diff_for_answers) for answer in data[1].split(":")]


class ResultPage(ttk.Frame):
    def __init__(self, parent, quiz_reference):  # ko imama stevilko, poiscema vprasanje, odgovor in mozne odgovore iz datoteke
        ttk.Frame.__init__(self, parent)
        self.quiz_reference = quiz_reference
        self.show_frame_widgets()

    def show_frame_widgets(self):
        points = self.quiz_reference.points
        all_points = self.quiz_reference.number_of_questions
        ttk.Label(self, text=_("Tvoj rezultat je: {} od {} točk!").
                  format(points, all_points)).pack(pady=10, padx=10)

        text_message = self.appropriate_message(points)
        ttk.Label(self, text=text_message).pack(pady=10, padx=10)

        appropriate_image = "Images/failure.gif" if points <= all_points // 2 else "Images/bravo.gif"

        photo = PhotoImage(file=appropriate_image)
        label = ttk.Label(self, image=photo)

        self.congratulation_photo = photo
        label.pack(pady=15)

        ttk.Button(self, text=_("Igraj ponovno!"),
                   command=self.quiz_reference.initialize_start_page,
                   width=button_width).pack(side="bottom")

    def appropriate_message(self, user_points):
        """Prikaze sporocilo glede na rezultat"""
        all_points = self.quiz_reference.number_of_questions
        if user_points in range(all_points // 2 + 1):
            message = _("Tvoje znanje je nezadostno!")
        elif user_points in range(all_points // 2 + 1, all_points // 4):
            message = _("Tvoje znanje je zadovoljivo.")
        elif user_points in range(all_points // 4, all_points):
            message = _("Čestitam, dosegel si skoraj vse točke!")
        else:
            message = _("Bravo, tvoje znanje je izjemno!!!")  # dosegel je vse točke
        return message


app = Quiz()

app.geometry("500x250")
color = '#%02x%02x%02x' % (231, 231, 231)
app.configure(bg=color)  # sicer bi bil rob beli

app.resizable(0, 0)  # da v nobeno smer ni resizable
app.mainloop()
