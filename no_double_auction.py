import random


class noDoubleAuction():
    
    # double auction 제약을 만족하지 않고 경매를 진행했을 경우
    def __init__(self):
        print("Hello no double auction")

    def noDoubleAuntion(self, informationOfIRD, informationOfISD):
        self.k = 1
        self.p_ird = 0
        self.p_isd = 0
        self.win_IRD = dict()
        self.win_ISD = dict()

        ISD_temp_ask, IRD_temp_bid = self.noTruthfulness(informationOfIRD,informationOfISD)
        # ---------------------------------------------------------------------------
        # 1. Natural order
        # ---------------------------------------------------------------------------
        sort_IRD = dict(sorted(IRD_temp_bid.items(), key=lambda x: x[1]['bid'], reverse=True))
        sort_ISD = dict(sorted(ISD_temp_ask.items(), key=lambda x: x[1]['ask']))
        self.ird_index = list(sort_IRD.keys())
        self.isd_index = list(sort_ISD.keys())
        remain_IRD = sort_IRD.copy()

        if len(sort_IRD) >= len(sort_ISD):
            double_auction_iter = len(sort_ISD)
        else:
            double_auction_iter = len(sort_IRD)
        # ---------------------------------------------------------------------------
        # 2. Searching breakeven index(equilibrium price)
        # ---------------------------------------------------------------------------
        for i in range(double_auction_iter - 1):
            if sort_IRD[self.ird_index[i]]['bid'] >= sort_ISD[self.isd_index[i]]['ask']:
                # ---------------------------------------------------------------------------
                # 3. Double Auction winner set
                # ---------------------------------------------------------------------------
                self.win_IRD[self.ird_index[i]] = sort_IRD[self.ird_index[i]]
                self.win_ISD[self.isd_index[i]] = sort_ISD[self.isd_index[i]]
                # ---------------------------------------------------------------------------
                # 4. Remaining IRD in Double Auction
                # ---------------------------------------------------------------------------
                remain_IRD.pop(self.ird_index[i])
                if sort_IRD[self.ird_index[i + 1]]['bid'] < sort_ISD[self.isd_index[i + 1]]['ask']:
                    self.p_ird = sort_IRD[self.ird_index[i]]['bid']
                    self.p_isd = sort_ISD[self.isd_index[i]]['ask']
                    break
            self.k += 1
            
        self.win_ISD, self.win_IRD = self.notIR(self.win_ISD,self.win_IRD)

        return self.win_IRD, self.win_ISD, self.p_ird, self.p_isd, self.k, remain_IRD

    def notIR(self,ISD,IRD):
        for (key,value) in list(ISD.items()):
            if self.p_isd - value['True_ask'] < 0:
                ISD.pop(key)
        for (key,value) in list(IRD.items()):
            if value['True_bid'] - self.p_ird < 0:
                IRD.pop(key)
        resultISD = ISD
        resultIRD = IRD

        return resultISD, resultIRD


    def noTruthfulness(self, informationOfIRD, informationOfISD):

        ISD_temp_ask = dict()
        for index,(key,value) in enumerate(informationOfISD.items()):
            ISD_temp_ask.setdefault(key,{'True_ask':informationOfISD[key]['ask']})
            #ISD_temp_ask[key]['True_ask'] = informationOfISD[key]['ask']
            if index % 2 == 0:
                falseAsk = round(random.uniform((informationOfISD[key]['ask'] + 1), 10), 3)
                ISD_temp_ask[key]['ask'] = falseAsk
            else:
                falseAsk = round(random.uniform(3, (informationOfISD[key]['ask'] - 1)), 3)
                ISD_temp_ask[key]['ask'] = falseAsk

        IRD_temp_bid = dict()
        for index,(key,value) in enumerate(informationOfIRD.items()):
            IRD_temp_bid.setdefault(key,{'True_bid':informationOfIRD[key]['bid']})
            #IRD_temp_bid[key]['True_bid'] = informationOfIRD[key]['bid']
            if index % 2 == 0:
                falseBid = round(random.uniform((informationOfIRD[key]['bid'] + 1), 14), 3)
                IRD_temp_bid[key]['bid'] = falseBid
            else:
                falseBid = round(random.uniform(0, (informationOfIRD[key]['bid'] - 1)), 3)
                IRD_temp_bid[key]['bid'] = falseBid

        return ISD_temp_ask, IRD_temp_bid




