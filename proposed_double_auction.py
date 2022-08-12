import random


class doubleAuction():

    def __init__(self):
        print("Hello double auction")

    def doubleAuction(self,informationOfIRD,informationOfISD):

        self.k = 1
        self.p_ird = 0
        self.p_isd = 0
        self.win_IRD = dict()
        self.win_ISD = dict()

        # 제약 확인

        # ---------------------------------------------------------------------------
        # 1. Natural order
        # ---------------------------------------------------------------------------
        sort_IRD = dict(sorted(informationOfIRD.items(), key=lambda x: x[1]['bid'], reverse=True))
        sort_ISD = dict(sorted(informationOfISD.items(), key=lambda x: x[1]['ask']))
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
                if sort_IRD[self.ird_index[i+1]]['bid'] < sort_ISD[self.isd_index[i+1]]['ask']:
                    self.p_ird = sort_IRD[self.ird_index[i]]['bid']
                    self.p_isd = sort_ISD[self.isd_index[i]]['ask']
                    break
            self.k += 1


        return self.win_IRD, self.win_ISD, self.p_ird, self.p_isd, self.k, remain_IRD

    def noTruthfulness(self):

        ISD_temp_ask = dict()
        for i in range(len(self.win_ISD)):
            ISD_temp_ask[self.isd_index[i]]['True_ask'] = self.win_ISD[self.isd_index[i]]['ask']
            if i % 2 == 0:
                falseAsk = round(random.uniform((self.win_ISD[self.isd_index[i]]['ask'] + 1), 10), 3)
                ISD_temp_ask[self.isd_index[i]]['False_ask'] = falseAsk
            else:
                falseAsk = round(random.uniform(3, (self.win_ISD[self.isd_index[i]]['ask'] - 1)), 3)
                ISD_temp_ask[self.isd_index[i]]['False_ask'] = falseAsk

        IRD_temp_bid = dict()
        for i in range(len(self.win_IRD)):
            IRD_temp_bid[self.ird_index[i]]['True_bid'] = self.win_IRD[self.ird_index[i]]['bid']
            if i % 2 == 0:
                falseBid = round(random.uniform((self.win_IRD[self.ird_index[i]]['bid'] + 1), 14), 3)
                IRD_temp_bid[self.ird_index[i]]['False_bid'] = falseBid
            else:
                falseBid = round(random.uniform(0, (self.win_IRD[self.ird_index[i]]['bid'] - 1)), 3)
                IRD_temp_bid[self.ird_index[i]]['False_bid'] = falseBid

        return ISD_temp_ask, IRD_temp_bid

    def noDoubleAuntion(self,informationOfIRD,informationOfISD):

        self.noTruthfulness()
        # ---------------------------------------------------------------------------
        # 1. Natural order
        # ---------------------------------------------------------------------------
        sort_IRD = dict(sorted(informationOfIRD.items(), key=lambda x: x[1]['bid'], reverse=True))
        sort_ISD = dict(sorted(informationOfISD.items(), key=lambda x: x[1]['ask']))
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

        return self.win_IRD, self.win_ISD, self.p_ird, self.p_isd, self.k, remain_IRD

    # Double Auction constraints
    def doubleAuctionConstraints(self):

        # ---------------------------------------------------------------------------
        # 1. Individual Rationality
        # ---------------------------------------------------------------------------
        self.flag_IRD_IR = True
        self.flag_ISD_IR = True
        for i in range(len(self.win_IRD)):
            if self.win_IRD[self.ird_index[i]] >= self.p_ird:
                print("satisfy IR_IRD",self.ird_index[i])
            else:
                print("not satisfy IR_IRD", self.ird_index[i])
                self.flag_IRD_IR = False
        for i in range(len(self.win_ISD)):
            if self.win_ISD[self.isd_index[i]] <= self.p_isd:
                print("satisfy IR_ISD",self.isd_index[i])
            else:
                print("not satisfy IR_ISD",self.isd_index[i])
                self.flag_ISD_IR = False

        # ---------------------------------------------------------------------------
        # 2. Weak Balanced Budget
        # ---------------------------------------------------------------------------
        self.flag_IBD = True
        IBD_Budget = self.k * (self.p_ird - self.p_isd)
        if IBD_Budget >= 0:
            print("satisfy Weak Balanced Budget")
        else:
            print("not satisfy Weak Balanced Budget")
            self.flag_IBD = False

        # ---------------------------------------------------------------------------
        # 3. Truthfulness
        # ---------------------------------------------------------------------------
        # ISD case 1 = c(true) < a(false)
        ISD_temp_ask = dict()
        for i in range(len(self.win_ISD)):
            falseAsk = round(random.uniform((self.win_ISD[self.isd_index[i]]['ask'] + 1), 10), 3)
            ISD_temp_ask[self.isd_index[i]]['True_ask'] = self.win_ISD[self.isd_index[i]]['ask']
            ISD_temp_ask[self.isd_index[i]]['False_ask for case1'] = falseAsk

        # ISD case 2 = c(true) > a(false)
        for i in range(len(self.win_ISD)):
            falseAsk = round(random.uniform(3, (self.win_ISD[self.isd_index[i]]['ask'] - 1)), 3)
            ISD_temp_ask[self.isd_index[i]]['False_ask for case2'] = falseAsk

        # IRD case 1 = v(true) < b(false) 0,14
        IRD_temp_bid = dict()
        for i in range(len(self.win_IRD)):
            falseBid = round(random.uniform((self.win_IRD[self.ird_index[i]]['bid'] + 1), 14), 3)
            IRD_temp_bid[self.ird_index[i]]['True_bid'] = self.win_IRD[self.ird_index[i]]['bid']
            IRD_temp_bid[self.ird_index[i]]['False_bid for case1'] = falseBid

        # IRD case 2 = v(true) > b(false)
        for i in range(len(self.win_IRD)):
            falseBid = round(random.uniform(0, (self.win_IRD[self.ird_index[i]]['bid'] - 1)), 3)
            IRD_temp_bid[self.ird_index[i]]['False_bid for case2'] = falseBid

