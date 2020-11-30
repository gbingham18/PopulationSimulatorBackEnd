from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from random import randint

app = Flask(__name__)
CORS(app)

def generateGenerations(p, q, numGens, popSize, fitAA, fitAa, fitaa, mutAa, mutaA):

    q = 1-p
    pValues = [None] * numGens
    freqAA = p*p
    freqAa = 2*p*q
    freqaa = q*q

    pValues[0] = [0, p]

    for i in range(1, numGens):

        freqAA = freqAA * fitAA
        freqAa = freqAa * fitAa
        freqaa = freqaa * fitaa

        totalLeft = freqAA + freqAa + freqaa

        freqAA = freqAA / totalLeft
        freqAa = freqAa / totalLeft
        freqaa = freqaa / totalLeft

        numAA = int(round(freqAA * popSize))
        numAa = int(round(freqAa * popSize))
        numaa = int(round(freqaa * popSize))

        numAA, numAa, numaa = randomMating(numAA, numAa, numaa)

        freqAA = numAA / popSize
        freqAa = numAa / popSize
        freqaa = numaa / popSize

        curr = [i, (freqAA + freqAa/2)]
        pValues[i] = curr

    return jsonify({'data': pValues})

@app.route('/', methods=['POST'])

def postMethod():
    if (request.method == 'POST'):
        data = request.get_json()
    p = float(data.get("p"))
    numGens = int(data.get("numGens"))
    popSize = int(data.get("popSize"))
    fitA1 = float(data.get("fitA1"))
    fitA2 = float(data.get("fitA2"))
    fitA3 = float(data.get("fitA3"))
    mutAa = float(data.get("mutAa"))
    mutaA = float(data.get("mutaA"))

    returnData = generateGenerations(p, 0, numGens, popSize, fitA1, fitA2, fitA3, mutAa, mutaA)

    return returnData.json


def randomMating(freqAA, freqAa, freqaa):

    popSize = freqAA + freqAa + freqaa
    newAA = 0
    newAa = 0
    newaa = 0

    while popSize > 0:
        allele1 = ""
        allele2 = ""
        #Select two random alleles from population (ex: Aa, AA)

        for i in range(0, 2):
            if (popSize > 0):
                x = randint(1, popSize)
                if 0 < x and x <= freqAA:
                    popSize = popSize - 1
                    if i == 0:
                        allele1 = "AA"
                        freqAA = freqAA - 1
                    else:
                        allele2 = "AA"
                        freqAA = freqAA - 1

                elif freqAA < x and x <= (freqAA + freqAa):
                    popSize = popSize - 1
                    if i == 0:
                        allele1 = "Aa"
                        freqAa = freqAa - 1
                    else:
                        allele2 = "Aa"
                        freqAa = freqAa - 1

                elif (freqAA + freqAa) < x and x <= popSize:
                    popSize = popSize - 1
                    if i == 0:
                        allele1 = "aa"
                        freqaa = freqaa - 1
                    else:
                        allele2 = "aa"
                        freqaa = freqaa - 1
        #Concatenate two allele strings into one (ex: Aa, AA => AaAA)
        #Run through process twice to generate two new offspring per pair

        for i in range(0, 2):
            if allele1 + allele2 == "AAAA":
                newAA = newAA + 1
            elif allele1 + allele2 == "aaaa":
                newaa = newaa + 1
            elif allele1 + allele2 == "Aaaa" or allele1 + allele2 == "aaAa":
                x = randint(0, 99)
                if 0 <= x and x < 50:
                    newAa = newAa + 1
                else:
                    newaa = newaa + 1
            elif allele1 + allele2 == "AAaa" or allele1 + allele2 == "aaAA":
                newAa = newAa + 1
            elif allele1 + allele2 == "AaAa":
                x = randint(0, 99)
                if 0 <= x < 25:
                    newAA = newAA + 1
                elif 25 <= x < 75:
                    newAa = newAa + 1
                elif 75 <= x < 100:
                    newaa = newaa + 1
            elif allele1 + allele2 == "AAAa" or allele1 + allele2 == "AaAA":
                x = randint(0, 99)
                if 0 <= x and x < 50:
                    newAA = newAA + 1
                else:
                    newAa = newAa + 1

    return newAA, newAa, newaa

if __name__ == '__main__':
    app.run()