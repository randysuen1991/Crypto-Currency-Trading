import scipy.stats as stats
import numpy as np

class Analysis():
    def Spearman_Rank(X,Y):
        r_s = stats.spearmanr(X,Y)
        return r_s
    def Correlation(X,Y):
        c_c = np.corrcoef(X,Y)
        return c_c