class environment:
    def __init__(self,totalTime,timeStep,nDealers,nNoiseCustomers,NoiseCustomerFrequencies,nInfCustomers,InformedCustomerValues,connectivity):
        #initialise system to start at time = 0
        self.current_t=0
        #how long the total simulation will be (in minutes)
        self.T=totalTime
        #size of time step....possibly consider making this very small so that
        #I can put in a time penalty for certain actions
        self.dt=timeStep
        #create list of dealers (currently, unconfigured)
        self.dealers=[dealer() for each in range(nDealers)]
        #create noise customers (currently have no set frequency, infored = 0)
        self.noiseCustomers=[noiseCustomer() for each in range(nNoiseCustomers)]
        #create informed customers (currently all are set to default level of informed 1)
        self.infCustomers=[infCustomer() for each in range(nInfCustomers)]
        #configure noise customers frequencies
        customerCount=1
        for i in range(nNoiseCustomers):
            self.noiseCustomers[i].setFreq(NoiseCustomerFrequencies[i])
            self.noiseCustomers[i].assignDealer(self.dealers[0]) ###################!!!!!!! This is just assigning one dealer, needs to be drastically changed for multiple dealers
            self.noiseCustomers[i].label(customerCount)
            customerCount=customerCount+1
        #configure informed customer levels
        for i in range(nInfCustomers):
            self.infCustomers[i].setInformedValue(InformedCustomerValues[i])
            self.infCustomers[i].assignDealer(self.dealers[0]) ###################!!!!!!! This is just assigning one dealer, needs to be drastically changed for multiple dealers
            self.infCustomers[i].label(customerCount)
            customerCount=customerCount+1


    def next_t(self):
        #run through processes
        #first customers
        for cust in self.noiseCustomers:
            cust.process(self.dt,self.current_t)
        #then dealers
        
        self.current_t=self.current_t+self.dt #go to next time step


class marketParticipant:
    def __init__(self,isCustomer):
        self.isCustomer=isCustomer
        self.tradeBook=book()
        self.ID=None
    def label(self,count):
        if isCustomer:
            self.ID='c'+str(count)
        else:
            self.ID='d'+str(count)


class customer(marketParticipant):
    #broad customer class can either be informed or uninformed
    def __init__(self,informed):
        marketParticipant.__init__(self,True) #market participant, isCustomer=True
        self.informed=informed
        self.dealers=[]
    def assignDealer(self,dealer): ########################## THIS ONLY CAN ASSIGN ONE DEALER AT A TIME
            self.dealers.append(dealer)
    def order(self,):

    



class infCustomer(customer):
    def __init__(self):
        customer.__init__(self,1) #default informed customers is 1
    def setInformedValue(self,I):
        self.informed=I

class noiseCustomer(customer):
    #uninformed customers are known as noise traders and trade at a 
    #predetermined frequency (trades per hour)
    def __init__(self):
        customer.__init__(self,0)
        self.freq=None
    def setFreq(self,freq):
        self.freq=freq
    def process(self,dt,current_t):
        from random import uniform
        makeTrade=uniform(0,1)
        if makeTrade<self.freq*dt/60.:
            if uniform(0,1)<0.5:
                #will make a buy order
                self.order(dealers,1)
            else:
                #will make a sell order   
                self.order(dealers,-1) 
        else:
            pass #make no trade

class dealer(marketParticipant):
    def __init__(self):
        marketParticipant.__init__(self,False)
        
        
        

class book:
    def __init__(self):
        self.trades=[]
    def addTrade(self,size,price,time,partnerID):
        self.trades.append([size,price,time,partnerID])

    
    
    
        


T=2 #total time
dt=1 #timeStep
nDealers=1 #number of dealers 
nNoiseCustomers=10 #number of noise customers 
NoiseCustomerFrequencies=[2 for each in range(nNoiseCustomers)] #initial frequencies 2 trades per hour
nInfCustomers=0 #number of informed customers
InformedCustomerValues=0 #not applicable for no informed customers
connectivity=[] #haven't used yet in code

simulation=environment(T,dt,nDealers,nNoiseCustomers,NoiseCustomerFrequencies,nInfCustomers,InformedCustomerValues,connectivity)