class marketParticipant:
        T=2*60.0 #time in mins
        dt=1
        inventory=[]


class customer(marketParticipant):
    #broad customer class can either be informed or uninformed
    def __init__(self,dealer,informed):
        self.dealer=dealer
        if informed==0:
            self.informed=False
        if informed>0:
            self.informed=True

class noiseCustomer(customer):
    #uninformed customers are known as noise traders and trade at a 
    #predetermined frequency (trades per hour)
    def __init__(self,dealer,freq):
        customer.__init__(self,dealer,0)
        self.freq=freq
    def decide(self):
        from random import uniform
        makeTrade=uniform(0,1)
        if makeTrade<self.freq*self.dt/60.0:


class dealer(marketParticipant):
    def __init__(self,customerList):
        dealer.customerList=customerList
        dealer.customerBid
        dealer.customerAsk
    def IncOrder(self,buy_or_sell,origin,time):
        if origin==customer:
            if buy_or_sell==0:
                pass
            elif buy_or_sell=='buy':
                self.inventory.append([-1,customerAsk,time,origin])
        else:
            pass