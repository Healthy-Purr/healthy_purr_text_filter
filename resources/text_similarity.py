from re import M, S
import re
from unicodedata import normalize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from syltippy import syllabize


ingredients_dictionary = {
  "HUE VO": "Huevo",
  "CAR NE": "Carne",
  "CER DO": "Cerdo",
  "POR CI NO": "Cerdo",
  "LE CHE": "Leche",
  "SO JA": "Soja",
  "PO LLO": "Pollo",
  'PES CA DO': "Pescado",
  'QUE SO': "Queso",
  'CO LO RAN TE': "Colorante"
}

measure_dictionary = {
  "PRO TE I NA": "Proteina",
  "CE NI ZA": "Ceniza",
  "GRA SA": "Grasa",
  "HU ME DAD": "Humedad",
  "FI BRA": "Fibra",
  "CAL CIO": "Calcio",
  "FOS FO RO": "Fosforo",
  'TAU RI NA': "Taurina"
}

#
core_words = ['CE NI ZA', 'PRO TE I NA', 'GRA SA', 'HU ME DAD', 'FI BRA', 'CAL CIO', 'FOS FO RO', 'TAU RI NA', 'HUE VO', 'CAR NE', 'CER DO', 'LE CHE', 'SO JA', 'PO LLO', 'PES CA DO', 'QUE SO', 'CO LO RAN TE', 
    'POR CI NO']
guaranteed_analysis_list = ['PRO TE I NA', 'GRA SA', 'HU ME DAD', 'FI BRA', 'CAL CIO', 'FOS FO RO', 'CE NI ZA']
ingredients_list = ['HUE VO', 'CAR NE', 'CER DO', 'LE CHE', 'SO JA', 'PO LLO', 'PES CA DO', 'QUE SO', 'CO LO RAN TE', 'POR CI NO']
vowels = 'AEIOU'
consts = 'BCDFGHJKLMNPQRSTVWXYZ'
consts = consts + consts.lower()
vowels = vowels + vowels.lower()

def is_vowel(letter):
    return letter in vowels 

def is_const(letter):
    return letter in consts

def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False

def clean_value(value):
    value = value.replace('96', '%')
    value = value.replace('Min.', '')
    value = value.replace('Max.', '')
    measure = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", value)[0]
    return float(measure) / 100

def format(measure):
    measure = measure / 100
    return measure

def get_lines_text(textData):
    textData = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", textData), 0, re.I
    )
    sentences = textData.splitlines()
    guaranteed_analysis = {'Grasa': 0.0, 'Proteina': 0.0, 'Fibra': 0.0, 'Humedad': 0.0, 'Fosforo': 0.0, 'Calcio': 0.0, 'Ceniza' : 0.0, 'Carbohidratos': 0.0}
    has_taurine = {'Taurina' : 0.0}
    ingredients = {'Huevo': 0.0, 'Pollo': 0.0, 'Carne': 0.0, 'Cerdo': 0.0, 'Leche': 0.0, 'Pescado': 0.0, 'Soja': 0.0, 'Queso': 0.0, 'Colorante': 0.0}
    for index, line in enumerate(sentences):
        for word in line.split():
            text_evaluated = find_core_word(divide_word_syllable(word))
            if(text_evaluated == 'TAU RI NA'):
                has_taurine[measure_dictionary[text_evaluated]] = 1.0
            else:
                if(text_evaluated in guaranteed_analysis_list and guaranteed_analysis[measure_dictionary[text_evaluated]] == 0.0):
                    guaranteed_analysis[measure_dictionary[text_evaluated]] = get_value(sentences[index - 1], sentences[index].split(word)[1], sentences[index + 1])
                else:
                    if(text_evaluated in ingredients_list):
                        ingredients = update_ingredients(text_evaluated, ingredients)

    guaranteed_analysis['Carbohidratos'] = 1 - (guaranteed_analysis['Grasa'] + guaranteed_analysis['Proteina'] + guaranteed_analysis['Fibra'] + guaranteed_analysis['Humedad'] + guaranteed_analysis['Fosforo'] + guaranteed_analysis['Calcio'] + guaranteed_analysis['Ceniza'])
    return guaranteed_analysis, has_taurine, ingredients

def update_ingredients(evaluated_text, ingredient_food_list):
    for key, value in ingredient_food_list.items():
        ingredient_to_evaluate = ingredients_dictionary[evaluated_text]
        if(ingredient_to_evaluate == key):
            ingredient_food_list[ingredient_to_evaluate] = 1.0
            break
    return ingredient_food_list

def get_value(previous_value, actual_value ,next_value):
    for word_a in actual_value.split():
        if(containsNumber(word_a)):
            return clean_value(word_a)
    for word_n in next_value.split():
        if(containsNumber(word_n)):
            return clean_value(word_n)
    for word_p in previous_value.split():
        if(containsNumber(word_p)):
            return clean_value(word_p)

def find_core_word(word):
    final_word = ""
    max_similarity = 0.0
    max_aux = 0.0
    for core in core_words:
        max_aux = compare_text(word, core)
        if(max_aux > max_similarity and max_aux > 0.6):
            max_similarity = max_aux
            final_word = core
            
    return final_word


def divide_word_syllable(word):
    syllables, stress = syllabize(word)
    #print(u' '.join(s if stress != i else s.upper() for (i, s) in enumerate(syllables)))

    return u' '.join(s.upper() for (i, s) in enumerate(syllables))



def compare_text(text1, text2):
    data = [text1, text2]
    count_vectorizer = CountVectorizer()
    vector_matrix = count_vectorizer.fit_transform(data)
    
    vector_matrix
    vector_matrix.toarray()

    return cosine_similarity(vector_matrix)[0][1]


##text = divide_word_syllable('Fösforo')

#sentenceList =  "Ricocat\nRintisa\nTe oyudamos?\nT359 14 08|359 00 44\nu8sarintsa.com\nWwW.ritisa.com\nANÁLISIS GARANTIZADO\nGrasa\nMin. 3.59%\nCalcio\n|Mín. 02%\nHumedad\nMác. 85%\nProteina\nMin. 8\nFibra\nMáL 1%\nFósforo\nMin. 0.29%6\nTABLA"

#sentenceList = "LLGARANTZADA\nProteina Min 10% Grasa Min, 4% | Humedad Ma. 79%\nCeniza Mac 3.5% | Fibra Máx 15% | Calcio Min. 0.3% I Fotos Wie &2\nNAEDENTES Cane ylo derivados de polo, Agua sufciente para elgrnces\nWs, Pescado. Aroz, Proteina aislada de soys., Almid6a nodheate &\nllesfats de sodio, Cloruro de potasio, Saly Sabor Saimin. Vitamias)\nSisD1, Vitanina E. Vitamina K, Tiamins (Vitamina 8), Ribslavna\nWlots Pateténico (Vitamina 85),.Piridoxina (Vitamina B6), BitisalV\nan82), Acido Folico (Vitamina 89), Taurina, Mangane50,Hiera,\ntte Vtanina Cy Colorantes.\nEAYUDAMOS?\nR\n135914 06|359 00 44\nGonsultas@rintisa.com\nWww.intiSs.com\nleto y balanceado\nals ylolo onel envase"


#print(get_lines_text(sentenceList))

