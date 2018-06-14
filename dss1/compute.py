import numpy as np
from celery import task

def charint(num):
    num = num.split(',')
    num=list(map(int,num))
    num=np.array(num)
    return num
@task    
def compute(total_rakes,demand,initial_stock_level,storage_capacity,terminal_capacity,max_allotment,weekly_penalty,comb_matrix):
    first = 1
    total_warehouses = 8
    total_weeks = 4
    demand = charint(demand)
    temp = demand
    initial_stock_level = charint(initial_stock_level)
    storage_capacity = charint(storage_capacity)
    terminal_capacity = charint(terminal_capacity)
    max_allottment = charint(max_allotment)

    rake_penalty_h =20;
    rake_penalty_f = 50;

    weekly_penalty =  charint(weekly_penalty)
    weekly_penalty = weekly_penalty.reshape(8,4)

    k_shift = 135
    k_reset = 575
    k_terminate = 7450
    comb_matrix =  charint(comb_matrix)
    comb_matrix = comb_matrix.reshape(8,8)
    def capacity_utilization_pf(a):
        n = np.ma.size(a)
        b = np.zeros((n))
        for i in range(0,n):
            b[i] = storage_capacity[i]/(initial_stock_level[i]+demand[i])
            b[i] = 10*b[i]
        return b

    # def surplus_allocation(demand):
    #     excess = np.array(np.nonzero(demand>4))
    #     num = np.size(excess)
    #     excess = excess.reshape(num,)
    #     for i in excess:
    #         dem = demand[i]
    #         while(dem > 8-demand[i]):
    #             w = np.random.randint(0,4)
    #             if(rake_allocated[i][w]==0):
    #                 rake_allocated[i][w] += 2
    #                 allocated += 2
    #                 dem -= 2
    final_weekly_distribution = 0
    final_total_penalty = 0
    final_rake_penalty = 0
    final_week_penalty = 0
    final_cup = 0
    final_comb = 0
    for i in range(0,100):
        demand = temp
        rake_allocated = np.zeros((8,4))
        total_demand = sum(demand)
        surplus = total_rakes - total_demand
        dv1 = np.random.randint(0,10)
        available_space = storage_capacity - initial_stock_level

        while (surplus>0 and dv1<5):
            max_cupf = capacity_utilization_pf(initial_stock_level+demand)
            available = np.minimum(max_allottment,available_space) - demand
            max_cupf_ind= max_cupf.argmax()
            max_possible_addition = min(available[max_cupf_ind],surplus)
            addition = np.random.randint(1,max_possible_addition+1)
            demand[max_cupf_ind] += addition
            surplus -= addition
        while (surplus>0 and dv1>=5):
            available = np.minimum(max_allottment,available_space) - demand
            rand = 0
            selected = 0
            while (selected == 0):
                rand = np.random.randint(0,8)
                selected = available[rand]
            max_possible_addition = min(available[rand],surplus)
            addition = np.random.randint(1,max_possible_addition+1)
            demand[rand] += addition
            surplus -= addition

        comb = np.zeros((8,8,4))
        monthly_allotment = demand
        allocated1 = sum(rake_allocated)
        allocated = sum(allocated1)
        excess = np.array(np.nonzero(demand>4))
        num = np.size(excess)
        excess = excess.reshape(num,)
        for i in excess:
            dem = demand[i]
            while(dem > 8-demand[i]):
                w = np.random.randint(0,4)
                if(rake_allocated[i][w]==0):
                    rake_allocated[i][w] += 2
                    allocated += 2
                    dem -= 2

        k = 1
        while allocated<total_rakes:
            j = np.random.randint(0,8)
            w = np.random.randint(0,4)
            selected_row = rake_allocated[j,:]
            sum3 = sum(selected_row)
            sum4 = sum3
            dv2 = np.random.randint(0,10)
            iteration = 1;
            while (sum4<monthly_allotment[j]) and (iteration<2):
                if(rake_allocated[j][w]==0):
                    comb_row = comb_matrix[j,:]
                    if(sum(comb_row)>0):
                        combwh = np.array(np.nonzero(comb_row==1))
                        num = np.size(combwh)
                        combwh = combwh.reshape(num,)
                        rv = np.random.randint(0,num)
                        cw = combwh[rv]
                        selected_row2 = rake_allocated[cw,:]
                        sum5 = sum(selected_row2)
                        sum6 = sum5
                        while(rake_allocated[cw][w]==0 and sum6<monthly_allotment[cw] and dv2<5):
                            rake_allocated[j][w] += 1
                            rake_allocated[cw][w] += 1
                            comb[j][cw][w] += 1
                            comb[cw][j][w] += 1
                            allocated += 2
                            sum4 += 1
                            sum6 += 1
                        count = 1
                        while(dv2>=5 and k>k_shift and count<2 and (sum4+1)<demand[j]):
                            if(terminal_capacity[j]==2 and rake_allocated[j][w]==0):
                                c=1
                                while(sum4<(monthly_allotment[j]-1) and c<2):
                                    rake_allocated[j][w] += 2
                                    allocated += 2
                                    sum4 += 2
                                    c+=1
                            count+=1
                    elif(combnum == 0 and (sum4+1)<demand[j]):
                        rake_allocated[j][w] += 2
                        allocated += 2
                        sum4 += 2
                iteration+=1
            if(k%k_reset == 0):
                rake_allocated = np.zeros((total_warehouses,total_weeks))
                comb = np.zeros((8,8,4))
                allocated=0
                excess = np.array(np.nonzero(demand>4))
                num = np.size(excess)
                excess = excess.reshape(num,)
                for i in excess:
                    dem = demand[i]
                    while(dem > 8-demand[i]):
                        w = np.random.randint(0,4)
                        if(rake_allocated[i][w]==0):
                            rake_allocated[i][w] += 2
                            allocated += 2
                            dem -= 2
            if(k>k_terminate):
                break
            k += 1
        if(allocated == total_rakes):
            half_rakes = np.array(np.nonzero(rake_allocated==1))
            full_rakes = np.array(np.nonzero(rake_allocated==2))
            size1 = np.size(half_rakes)
            size2 = np.size(full_rakes)
            cost1 = size1*rake_penalty_h/2
            cost2 = size2*rake_penalty_f/2
            rake_penalty = cost1+cost2

            alloted_weeks = np.array(np.nonzero(rake_allocated>0))
            week_penalty = 0
            weeknum = np.size(alloted_weeks)/2
            m = 0
            while m < weeknum:
                swh = alloted_weeks[0,m]
                sw = alloted_weeks[1,m]
                week_penalty += weekly_penalty[swh][sw]
                m += 1

            capacity_utilization_penalty = sum(capacity_utilization_pf(initial_stock_level+demand))
            total_penalty = rake_penalty + week_penalty + capacity_utilization_penalty

        if(first ==1 and allocated == total_rakes):
            final_weekly_distribution = rake_allocated
            final_total_penalty = total_penalty
            final_rake_penalty = rake_penalty
            final_week_penalty = week_penalty
            final_cup = capacity_utilization_penalty
            final_comb = comb
            first += 1
        if(allocated == total_rakes and first != 1):
            if(total_penalty<final_total_penalty):
                final_weekly_distribution = rake_allocated
                final_total_penalty = total_penalty
                final_rake_penalty = rake_penalty
                final_week_penalty = week_penalty
                final_cup = capacity_utilization_penalty
                final_comb = comb

    return final_weekly_distribution,final_total_penalty
