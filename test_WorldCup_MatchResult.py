#!/usr/bin/env python

#germany = 7 
#brazil = 1
#x = "credit"
#print('%(x)s-%(germany)d : %(brazil)d' % (vars()))
#credit-7 : 1


#dict_test = {'x':"credit", 'germany':7, 'brazil':1}
#print('{tk[x]}-{tk[germany]} : {tk[brazil]}'.format(tk = dict_test))
#credit-7 : 1


#使用泊松分布模拟比分

from scipy.stats import poisson

r = poisson.rvs(3, size=1000)[0]



#球队攻防能力如下：

#alpha,beta
#Arg,5,2
#Nig,3,3


#模拟比赛得分

from scipy.stats import poisson
import pandas as pd  # 读取球队进球率、失球率参数

team_strength = pd.read_csv('teams.csv')# 每一场球生成几次泊松随机数，次数越多随机因素越小
n_sim = 5

def simulate_match(team_A, team_B, knockout=False):
    '''模拟一场比赛，返回主队进球数、客队进球数'''
# 获取比赛双方进球率、失球率 
    home_scoring_strength = (team_strength.loc[team_A, 'alpha'] + \
        team_strength.loc[team_B, 'beta']) / 2
    away_scoring_strength = (team_strength.loc[team_A, 'beta'] + \
        team_strength.loc[team_B, 'alpha']) / 2 # 模拟n次比赛进球数取众数 

    fs_A = poisson.rvs(home_scoring_strength, size=n_sim)[0]
    fs_B = poisson.rvs(away_scoring_strength, size=n_sim)[0]

    print(team_A, fs_A, team_B, fs_B) # 进入淘汰赛，若平局，点球大战晋级概率50%：50% 
    if knockout:
        if fs_A == fs_B:
            return [team_A, team_B][sp.random.randint(0, 2)]
        elif fs_A > fs_B:
            return team_A
        else:
            return team_B
    return fs_A, fs_B

simulate_match('Arg', 'Nig', knockout=True)


#小组赛 分组及结果模拟 

#fixture_A = [['俄罗斯', '沙特阿拉伯'], ['埃及', '乌拉圭'], ['俄罗斯', '埃及'], ['乌拉圭', '沙特阿拉伯'], ['沙特阿拉伯', '埃及'], ['俄罗斯', '乌拉圭']]
#建一个类，每个组分别各自初始化自己的类，传入参数fixture就是上面创建的赛程，只需调用play函数就可以模拟该小组6场比赛比分。

#self.table是小组积分榜，保存下来每次模拟的小组头两名球队名，后面统计每支队在1000次模拟里出线的次数，即出线概率。
#


class Group: '''模拟小组赛阶段，直接调用.play方法。''' 
    def __init__(self, group_teams, group_name, fixture): 
        self.group_teams = group_teams 
        self.group_name = group_name 
        self.table = pd.DataFrame(0, columns=['场次', '积分', '进球', '失球', '净胜球'], \
            index=self.group_teams) 
        self.fixture = fixture 
        self.result = None 
    def play(self): 
        result = [] 
        for [team_A, team_B] in self.fixture: 
            fs_A, fs_B = simulate_match(team_A, team_B) 
            self.table.loc[team_A, '场次'] += 1 
            self.table.loc[team_B, '场次'] += 1 
            self.table.loc[team_A, '进球'] += fs_A 
            self.table.loc[team_B, '进球'] += fs_B 
            self.table.loc[team_A, '失球'] += fs_B 
            self.table.loc[team_B, '失球'] += fs_A 
            if fs_A > fs_B: 
                self.table.loc[team_A, '积分'] += 3 
            elif fs_A == fs_B: 
                self.table.loc[team_A, '积分'] += 1 
                self.table.loc[team_B, '积分'] += 1 
            elif fs_A < fs_B: 
                self.table.loc[team_B, '积分'] += 3
 
            else: raise ValueError('比赛比分模拟有误！') 
            
            result.append([team_A, team_B, fs_A, fs_B]) 
            self.result = pd.DataFrame(result, columns=['主队', '客队', '主队进球', '客队进球'])
            self.table['净胜球'] = self.table['进球'] - self.table['失球']
            self.table.sort_values(by=['积分', '净胜球', '进球'], ascending=[False, False, False], \ 
               inplace=True)


