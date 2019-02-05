class Argentina:

    def getPresident(self):
        president = self.whoisinpower()
        return "The current president is {}".format(president)

    def whoisinpower(self):
        return "Mauricio Macri"

    def getPopulation(self):
        return "45 Million"

    def getCapital(self):
        return "Buenos Aires"


def describe():

    population = Argentina.getPopulation()
    capital = Argentina.getCapital()
    president = Argentina.getPresident()

    return "Argentina is a beautiful country with a population of {}, \n whose capital is {} and whose president is {}".format(population, capital, president)



