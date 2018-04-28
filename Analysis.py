import scipy.stats as stats

class Analysis():
    def Spearman_Rank(X,Y):
        r_s = stats.spearmanr(X,Y)
        return r_s