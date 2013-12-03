class environment:
    def __init__(totalTime,timeStep,nDealers,nNoiseCustomers,NoiseCustomerFrequencies,nInfCustomers,InformedCustomerValues,connectivity):
        self.current_t=0
        self.T=totalTime
        selt.dt=timeStep
        self.dealers=[dealer() for each in range(nDealers)]
        self.noiseCustomers=[noiseCustomer() for each in range(nNoiseCustomers)]
        self.infCustomers=[infCustomer() for each in range(nInfCustomers)]
        for i in range(nNoiseCustomers):
            self.noiseCustomers[i].setFreq(NoiseCustomerFrequencies[i])
        for i in range(nInfCustomers):
            self.infCustomers[i].setInformedValue(InformedCustomerValues[i])

    #def next_t(self):
    #    self.current_t=self.current_t+self.dt


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


