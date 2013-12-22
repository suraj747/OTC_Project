

class environment:
    def __init__(self,totalTime,timeStep,nDealers,nNoiseCustomers,NoiseCustomerFrequencies,nInfCustomers,InformedCustomerValues,limitOrderMkt,connectivity):
        #initialise system to start at time = 0
        self.current_t=0.
        #how long the total simulation will be (in minutes)
        self.T=totalTime
        #size of time step....possibly consider making this very small so that
        #I can put in a time penalty for certain actions
        self.dt=timeStep
        self.LOM=limitOrderMkt
        #create list of dealers (currently unconfigured but have a limit order market)
        self.dealers=[dealer(self.LOM) for each in range(nDealers)]
        #add dealers to limit order market
        self.LOM.add_dealers(self.dealers)
        #create noise customers (currently have no set frequency, infored = 0)
        self.noiseCustomers=[noiseCustomer() for each in range(nNoiseCustomers)]
        #create informed customers (currently all are set to default level of informed 1)
        self.infCustomers=[infCustomer() for each in range(nInfCustomers)]


        #configure noise customers frequencies
        customerCount=1
        for i in range(nNoiseCustomers):
            self.noiseCustomers[i].setFreq(NoiseCustomerFrequencies[i],self.dt)
            self.noiseCustomers[i].assignDealer(self.dealers[0]) ###################!!!NeedEdit!!!! This is just assigning one dealer, needs to be drastically changed for multiple dealers
            self.noiseCustomers[i].label(customerCount)
            customerCount=customerCount+1
        #configure informed customer levels
        for i in range(nInfCustomers):
            self.infCustomers[i].setInformedValue(InformedCustomerValues[i])
            self.infCustomers[i].assignDealer(self.dealers[0]) ###################!!!!!NeedEdit!! This is just assigning one dealer, needs to be drastically changed for multiple dealers
            self.infCustomers[i].label(customerCount)
            customerCount=customerCount+1

        #configure dealers
        dealerCount=1
        for i in range(nDealers):
            self.dealers[i].label(dealerCount)
            dealerCount=dealerCount+1


    def next_t(self):
        #run through processes
        #first customers
        for cust in self.noiseCustomers:
            cust.process(self.current_t)
        #then dealers
        
        self.current_t=self.current_t+self.dt #go to next time step

class book:
    def __init__(self):
        self.trades=[]
    def addTrade(self,size,price,time,partnerID):
        self.trades.append([size,price,time,partnerID])

class marketParticipant:
    def __init__(self,isCustomer):
        self.isCustomer=isCustomer
        self.tradeBook=book()
        self.ID=None
    def label(self,count):
        if self.isCustomer:
            self.ID='c'+str(count)
        else:
            self.ID='d'+str(count)


class customer(marketParticipant):
    #broad customer class can either be informed or uninformed
    def __init__(self,informed):
        marketParticipant.__init__(self,True) #market participant, isCustomer=True
        self.informed=informed
        self.dealers=[]
    def assignDealer(self,dealer): ########################## THIS ONLY CAN ASSIGN ONE DEALER AT A TIME NeedEdit
            self.dealers.append(dealer)
    #def order(!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!):
     #   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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
    def setFreq(self,freq,dt):
        self.freq=freq*dt
    def process(self,current_t):
        from random import uniform
        makeTrade=uniform(0,1)
        if makeTrade<self.freq/60.:
            if uniform(0,1)<0.5:
                pass#will make a buy order
                #self.order(!!!!!!!!!!!!!!NeedEdit!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!)
            else:
                pass#will make a sell order   
                #self.order(!!!!!!!!!!!!!!!!!!!!!!NeedEdit!!!!!!!!!!!!!!!!!!!!!!!!!!) 
        else:
            pass #make no trade

class dealer(marketParticipant):
    def __init__(self,limitOrderMkt):
        marketParticipant.__init__(self,False)
        custSpread=2
        self.LOM=limitOrderMkt
        #customer spreads are same as market spreads plus small amount
        self.cBid=self.LOM.bids[0][0]-(custSpread/2.)
        self.cAsk=self.LOM.asks[0][0]+(custSpread/2.)
    def make_trade(self,counterparty,price,size,time):
        self.tradeBook.addTrade(size,price,time,counterparty.ID)
        counterparty.tradeBook.addTrade(-size,price,time,self.ID)
    def place_LO(self,bid_ask,price,time,volume):
        self.LOM.place_lim_order(bid_ask,price,time,volume,self)

#NeedEdit this is a special type of dealer
class sinkDealer(marketParticipant):
    def __init__(self,limitOrderMkt):
        marketParticipant.__init__(self,False)
        custSpread=2
        self.LOM=limitOrderMkt
        #customer spreads are same as market spreads plus small amount
        self.cBid=99
        self.cAsk=101
    def make_trade(self,counterparty,price,size,time):
        self.tradeBook.addTrade(size,price,time,counterparty.ID)
        counterparty.tradeBook.addTrade(-size,price,time,self.ID)
    def place_LO(self,bid_ask,price,time,volume):
        self.LOM.place_lim_order(bid_ask,price,time,volume,self)

class limit_market():
    def __init__(self):
        self.dealers=[]
        self.bids=[]
        self.asks=[]
        self.current_orderID=0
    def add_dealers(self,dealers):
        self.dealers=dealers
    def place_lim_order(self,bid_ask,price,time,volume,dealer):
        self.current_orderID=self.current_orderID+1
        if bid_ask=="bid":
            if len(self.bids)==0:
                self.bids.append([price,time,volume,dealer.ID,self.current_orderID])
            else:
                for i in range(len(self.bids)):
                    if price>self.bids[i][0]:
                        self.bids.insert(i,[price,time,volume,dealer.ID,self.current_orderID])
                        break
                    elif price==self.bids[i][0]:
                        if i+1==len(self.bids):
                            self.bids.append([price,time,volume,dealer.ID,self.current_orderID])
                            break
                        elif self.bids[i+1][0]<price:
                            self.bids.insert(i+1,[price,time,volume,dealer.ID,self.current_orderID])
                            break
                        else:
                            pass
                    elif i+1==len(self.bids):
                        self.bids.append([price,time,volume,dealer.ID,self.current_orderID])
                        break

        elif bid_ask=="ask":
            if len(self.asks)==0:
                self.asks.append([price,time,volume,dealer.ID,self.current_orderID])
            else:
                for i in range(len(self.asks)):
                    if price<self.asks[i][0]:
                        self.asks.insert(i,[price,time,volume,dealer.ID,self.current_orderID])
                        break
                    elif price==self.asks[i][0]:
                        if i+1==len(self.asks):
                            self.asks.append([price,time,volume,dealer.ID,self.current_orderID])
                            break
                        elif self.asks[i+1][0]>price:
                            self.asks.insert(i+1,[price,time,volume,dealer.ID,self.current_orderID])
                            break
                        else:
                            pass
                    elif i+1==len(self.asks):
                        self.asks.append([price,time,volume,dealer.ID,self.current_orderID])
                        break

    def decrease_volume(bid_or_ask,orderID,volume):
        if bid_or_ask=="bid":
            for order in EBS.bids:
                if order[4]==orderID:
                    order[2]=order[2]-volume
                    if order[2]==0:
                        
                    break
                else:
                    pass
        elif bid_or_ask=="ask":
            for order in EBS.asks:
                if order[4]==orderID:
                    order[2]=order[2]-volume
                    break
                else:
                    pass



        elif bid_or_ask=="ask":


    def find_orders(self,buy_sell,volume):
        orders=[]
        unfilled=volume
        if buy_sell=="buy":
            for entry in self.asks:
                depth=entry[2]
                if depth>=unfilled:
                    orders.append(entry[4])
                    entry[2]=entry[2]-unfilled
                    unfilled=0
                    break
                elif depth<unfilled:
                    orders.append(entry[4])
                    unfilled=unfilled-entry[2]
                    entry[2]=0
            return orders



        elif buy_sell=="sell":
            pass
        else:
            print "error not buy or sell noob"

    def place_market_order(self,buy_sell,volume,customer,current_t):
        if buy_sell=="buy":
            if volume<self.asks[0][2]:
                self.asks[0][2]=self.asks[0][2]-volume
                for dealer in self.dealers:
                    if dealer.ID==self.asks[0][3]:
                        counterparty=dealer
                        break
                    else:
                        pass
                customer.make_trade(counterparty,self.asks[0][0],volume,current_t)
            else:
                #what to do if order is larger than limit order at best price
                #this shouldn't currently be an issue but NeedEdit
                pass
        elif buy_sell=="sell":
            if volume<self.bids[0][2]:
                self.bids[0][2]=self.bids[0][2]-volume
                for dealer in self.dealers:
                    if dealer.ID==self.bids[0][3]:
                        counterparty=dealer
                        break
                    else:
                        pass
                customer.make_trade(counterparty,self.bids[0][0],volume,current_t)
            else:
                #what to do if order is larger than limit order at best price
                #this shouldn't currently be an issue but NeedEdit
                pass






 



    
    
    
from random import uniform        


#T=2 #total time
#dt=1. #timeStep
#nDealers=2 #number of dealers 
#nNoiseCustomers=10 #number of noise customers 
#NoiseCustomerFrequencies=[2. for each in range(nNoiseCustomers)] #initial frequencies 2 trades per hour
#nInfCustomers=0 #number of informed customers
#InformedCustomerValues=0 #not applicable for no informed customers
#EBS=limit_market()
#connectivity=[] #haven't used yet in code
#
#simulation=environment(T,dt,nDealers,nNoiseCustomers,NoiseCustomerFrequencies,nInfCustomers,InformedCustomerValues,EBS,connectivity)

EBS=limit_market()
sink=sinkDealer(EBS) #sink dealer must be created before normal dealer because sink dealer can create a price without order book
sink.label(2) #although created first, I think I have coded in such a way that only the first dealer will be assigned to customers
                #therefore I have labeled sink as dealer 2

sink.place_LO("bid",sink.cBid,1,1000)
sink.place_LO("ask",sink.cAsk,1,1000)
suraj=dealer(EBS)
suraj.label(1)

for i in range(10):
    sink.place_LO("bid",sink.cBid-round(uniform(0,10),2),1+i,10)
    sink.place_LO("ask",sink.cAsk+round(uniform(0,10),2),i+1,10)

