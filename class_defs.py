

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
        self.position=[0,0]
        self.inventory=[0]
        self.AOI=0 #age of inventory
    def addTrade(self,size,price,time,partnerID):
        self.trades.append([size,price,time,partnerID])
        self.position[0]=self.position[0]+size*1000000.0
        self.position[1]=self.position[1]-size*price*1000000.0
    def process(self,current_t):
        #add all customer trades in period to inventory
        x=self.inventory[-1]
        for item in self.trades:
            if item[2]==current_t:
                x=x+item[0]
        self.inventory.append(x)
        #inventory updated




    

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
    def order(self,buy_sell,volume,time):
        if buy_sell=="buy":
            self.dealers[0].make_trade(self,self.dealers[0].cAsk,-volume,time)
        elif buy_sell=="sell":
            self.dealers[0].make_trade(self,self.dealers[0].cBid,volume,time)
        else:
            print "not buy or sell noob"
        #NeedEdit, currently only looks at one of potentially multiple dealers
    

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
        if makeTrade<self.freq:
            if uniform(0,1)<0.5:
                #will make a buy order
                self.order("buy",1,current_t)
            else:
                self.order("sell",1,current_t)
                
        else:
            pass #make no trade

class dealer(marketParticipant):
    def __init__(self,limitOrderMkt):
        marketParticipant.__init__(self,False)
        custSpread=0.0002
        self.LOM=limitOrderMkt
        #customer spreads are same as market spreads plus small amount
        self.cBid=self.LOM.bids[0][0]-(custSpread/2.)
        self.cAsk=self.LOM.asks[0][0]+(custSpread/2.)
    def make_trade(self,counterparty,price,size,time):
        self.tradeBook.addTrade(size,price,time,counterparty.ID)
        counterparty.tradeBook.addTrade(-size,price,time,self.ID)
    def place_LO(self,bid_ask,price,volume,time):
        self.LOM.place_lim_order(bid_ask,price,time,volume,self)
    def place_MO(self,buy_sell,volume,time):
        self.LOM.place_market_order(buy_sell,volume,self,time)
    def process(self,current_t):
        #first review current situation by processing trade book
        self.tradeBook.process(current_t)
    def urgency(self,inventory):
        u=inventory^2
        #######!!!!!!!!!!!!!!!!!!!!START HERE        


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
    def place_LO(self,bid_ask,price,volume,time):
        self.LOM.place_lim_order(bid_ask,price,time,volume,self)
    def place_MO(self,buy_sell,volume,time):
        self.LOM.place_market_order(buy_sell,volume,self,time)

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

    def decrease_volume(self,bid_or_ask,order,volume):
        if bid_or_ask=="bid":
            position=self.bids.index(order)
            self.bids[position][2]=self.bids[position][2]-volume
            if self.bids[position][2]==0:
                self.bids.pop(position)
        elif bid_or_ask=="ask":
            position=self.asks.index(order)
            self.asks[position][2]=self.asks[position][2]-volume
            if self.asks[position][2]==0:
                self.asks.pop(position)

        else:
            print "not bid or ask noob"


    def find_dealer(self,dealerID):
        for dealer in self.dealers:
            if dealer.ID==dealerID:
                return dealer
                break



    def find_orders(self,buy_sell,volume):
        orders_vols=[]
        unfilled=volume
        if buy_sell=="buy":
            for entry in self.asks:
                depth=entry[2]
                if depth>=unfilled:
                    orderID=entry
                    orderVolume=unfilled
                    orders_vols.append([orderID,orderVolume])
                    unfilled=0
                    break
                elif depth<unfilled:
                    orderID=entry
                    orderVolume=entry[2]
                    orders_vols.append([orderID,orderVolume])
                    unfilled=unfilled-entry[2]
            return orders_vols



        elif buy_sell=="sell":
            for entry in self.bids:
                depth=entry[2]
                if depth>=unfilled:
                    orderID=entry
                    orderVolume=unfilled
                    orders_vols.append([orderID,orderVolume])
                    unfilled=0
                    break
                elif depth<unfilled:
                    orderID=entry
                    orderVolume=entry[2]
                    orders_vols.append([orderID,orderVolume])
                    unfilled=unfilled-entry[2]
            return orders_vols
        else:
            print "error not buy or sell noob"

    def place_market_order(self,buy_sell,volume,customer,current_t):
        orderIDs_and_volumes=self.find_orders(buy_sell,volume)
        if buy_sell=="buy":
            bid_ask="ask"
            position_direction=-1.0
        elif buy_sell=="sell":
            bid_ask="bid"
            position_direction=1.0
        else:
            print "not buy or sell noob"

        for item in orderIDs_and_volumes:
            dealer=self.find_dealer(item[0][3])
            dealer.make_trade(customer,item[0][0],position_direction*item[1],current_t)
            self.decrease_volume(bid_ask,item[0],item[1])
 
 



        


#T=2 #total time
#dt=1. #timeStep
#nDealers=2 #number of dealers 
#nNoiseCustomers=10 #number of noise customers 
#NoiseCustomerFrequencies=[2. for each in range(nNoiseCustomers)] #initial frequencies 2 trades per hour
#nInfCustomers=0 #number of informed customers
#InformedCustomerValues=0 #not applicable for no informed customers
#EBS=limit_market()
#connectivity=[] #haven't used yet in code

#simulation=environment(T,dt,nDealers,nNoiseCustomers,NoiseCustomerFrequencies,nInfCustomers,InformedCustomerValues,EBS,connectivity)

#EBS=limit_market()
#sink=sinkDealer(EBS) #sink dealer must be created before normal dealer because sink dealer can create a price without order book
#sink.label(2) #although created first, I think I have coded in such a way that only the first dealer will be assigned to customers
                #therefore I have labeled sink as dealer 2



#for i in range(10):
#    sink.place_LO("bid",sink.cBid-i,1+i,10)
#    sink.place_LO("ask",sink.cAsk+i,i+1,10)
    #sink.place_LO("bid",sink.cBid-round(uniform(0,10),2),1+i,10)
    #sink.place_LO("ask",sink.cAsk+round(uniform(0,10),2),i+1,10)

#suraj=dealer(EBS)
#suraj.label(1)
#EBS.add_dealers([suraj,sink])

from random import uniform
import matplotlib.pyplot as plt
import numpy as np

current_t=0.
total_T=1
dt=1/3600. #1second in hours
nCustomers=10
frequencies=1
nSteps=int(total_T/dt)
tArray=np.linspace(0,total_T,nSteps+1)

initial_price=1.0000
customers1=[noiseCustomer() for i in range(nCustomers)]
customers2=[noiseCustomer() for i in range(nCustomers)]
EBS=limit_market()
sink=sinkDealer(EBS)
sink.label(2)
sink.place_LO("bid",initial_price-0.0001,100,current_t)
sink.place_LO("ask",initial_price+0.0001,100,current_t)
dealer1=dealer(EBS)
dealer2=dealer(EBS)
dealer1.label(0)
dealer2.label(1)

EBS.add_dealers([dealer1,dealer2,sink])


for each in customers1:
    each.label(customers1.index(each))
    each.assignDealer(dealer1)
    each.setFreq(frequencies,dt)
for each in customers2:
    each.label(len(customers1)+customers2.index(each))
    each.assignDealer(dealer2)
    each.setFreq(frequencies,dt)


current_t=0
for t in range(0,nSteps):
    current_t=current_t+dt
    for each in customers1:
        each.process(current_t)
    for each in customers2:
        each.process(current_t)
    if uniform(0,1)<0.5:
        dealer1.process(current_t)
        dealer2.process(current_t)
    else:
        dealer2.process(current_t)
        dealer1.process(current_t)
    

    
#plotting outputs

fig,ax=plt.subplots()
ax.plot(tArray,dealer1.tradeBook.inventory,tArray,dealer2.tradeBook.inventory,lw=2)
plt.grid(True)
ayMax=max([abs(i) for i in dealer1.tradeBook.inventory])
byMax=max([abs(i) for i in dealer2.tradeBook.inventory])
trueyMax=max([ayMax,byMax])
plt.ylim([-trueyMax-1,trueyMax+1])

plt.show()

