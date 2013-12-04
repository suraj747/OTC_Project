class environment:
    def __init__(totalTime,timeStep,nDealers,nNoiseCustomers,NoiseCustomerFrequencies,nInfCustomers,InformedCustomerValues,connectivity):
        #initialise system to start at time = 0
        self.current_t=0
        #how long the total simulation will be (in minutes)
        self.T=totalTime
        #size of time step....possibly consider making this very small so that
        #I can put in a time penalty for certain actions
        selt.dt=timeStep
        #create list of dealers (currently, unconfigured)
        self.dealers=[dealer() for each in range(nDealers)]
        #create noise customers (currently have no set frequency, infored = 0)
        self.noiseCustomers=[noiseCustomer() for each in range(nNoiseCustomers)]
        #create informed customers (currently all are set to default level of informed 1)
        self.infCustomers=[infCustomer() for each in range(nInfCustomers)]
        #configure noise customers frequencies
        for i in range(nNoiseCustomers):
            self.noiseCustomers[i].setFreq(NoiseCustomerFrequencies[i])
        #configure informed customer lvels
        for i in range(nInfCustomers):
            self.infCustomers[i].setInformedValue(InformedCustomerValues[i])

    def next_t(self):
        #run through processes
        #first customers
        #then dealers
        
        self.current_t=self.current_t+self.dt #go to next time step


class customer:
    #broad customer class can either be informed or uninformed
    def __init__(self,informed):
        self.informed=informed

class infCustomer(customer):
    def __init__(self):
        customer.__init__(self,1) #default informed customers is 1
    def setInformedValue(I):
        self.informed=I

class noiseCustomer(customer):
    #uninformed customers are known as noise traders and trade at a 
    #predetermined frequency (trades per hour)
    def __init__(self):
        customer.__init__(self,0)
    #    self.freq=None
    #def decide(self):
    #    from random import uniform
    #    makeTrade=uniform(0,1)
    #    if makeTrade<self.freq*self.dt/60.0:

class dealer:
    def __init__(self):
        pass


