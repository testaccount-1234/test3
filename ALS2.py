import numpy as np
import copy as cp
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
#import matplotlib.pyplot as plt

class ALS:
    '''Alternating least squares algorithm for parameter reconstruction from meaurements b = f(A,x)'''
    def __init__(self,A,b,x_init,batchsize= 'd^2',theta='not_known'):
    print("starting ALS")
        self.d = len(A[0][0]) # dimensions of tensor to be recovered
        if batchsize=='d^2':
            self.batchsize = self.d**2
        else:
            self.batchsize = batchsize
        self.A = A[self.batchsize:] # list of measurement tensors A_l = a_1 \otimes ... \otimes a_N, l = 1,...,m
        self.b = b[self.batchsize:] # list of results b_l = f(A_l,x), l = 1,...,m
        self.N = len(self.A[0])
        self.m = len(self.A) # number of measurements available
        self.H = int(self.m/(self.N*self.batchsize)) # number of iterations over whole tensor
        self.x = x_init # initialisation for ALS
        self.validation_data = A[0:self.batchsize]
        self.validation_measurements = b[0:self.batchsize]
        self.l2loss = [self.l2_loss(self.validation_data,self.validation_measurements,self.x)]
        self.term = 'The algorithm terminated after all measurements were used with an l2 loss of '+str(self.l2loss[-1])+' .'
        if np.shape(theta)==np.shape(self.x):
            self.fro_to_theta = [np.linalg.norm([[self.x[i][j]-theta[i][j] for j in range(len(theta[0]))] for i in range(len(theta))],'fro')]
            self.theta = theta
        else:
            self.theta = np.zeros((self.N,self.d))
            self.fro_to_theta = [np.zeros((self.N,self.d))]
        ### initialisation for the stoppin criteria
        self.step = 10*np.linalg.norm(x_init[0],2)
        
        ### parameters for stopping criteria
        self.minimal_step_size = 0.0001
        self.minimal_l2_loss = 0.0005
        
    
    def contract(self,X,Y):
        return np.prod([np.dot(X[i],Y[i]) for i in range(len(X))])
    
    def l2_loss_local_tensor(self, x , y, coeff):
        return np.linalg.norm([y[i] - np.dot(x[i],coeff) for i in range(len(y))],'fro')
    
    def l2_loss(self,x,y,coeff):
        if np.shape(coeff) == (self.N,self.d):
            return np.linalg.norm([y[i] - self.contract(x[i],coeff) for i in range(len(y))],2)/len(y)
        else:
            return self.l2_loss_local_tensor(x,y,coeff)/len(y)
    
    def run_once(self):
        '''H times update all local tensors iteratively over disjoint parts of the measurements A,b'''
        for h in range(self.H):
            print("h=",h)
            '''###iterate local tensors'''
            l = list(range(self.N))
            #np.random.shuffle(l)
            for n in l:
                x_old = cp.deepcopy(self.x)
                '''### check if step size is small enough'''
                self.step = self.step
                if self.step_size_criteria():
                    return self.x
                '''### check if l2 loss is small enough'''
                if self.l2_loss_criteria():
                    return self.x
                '''### update nth local tensor'''
                self.update(h*self.batchsize*self.N + n*self.batchsize,n)
                '''### calculate new l2 loss'''
                self.l2loss.append(self.l2_loss(self.validation_data,self.validation_measurements,self.x))
                '''### calculate Frobenius difference to theta'''
                self.fro_to_theta.append(np.linalg.norm([[self.x[i][j]-self.theta[i][j] for j in range(len(self.theta[0]))] for i in range(len(self.theta))],'fro'))
                '''### update step size that was taken: l2 norm of difference of new and old tensor'''
                self.step = np.linalg.norm([x_old[i][j] - self.x[i][j] for i in range(len(x_old)) for j in range(len(x_old[0]))],2)
        '''### update reason for the algorithms termination'''
        self.term = 'The algorithm terminated after all measurements were used with an l2 loss of '+str(self.l2loss[-1])+' .'

    def update(self,batchstart,n):
        '''update the nth local tensor of self.x by optimizing over the batch of measurements from batchstart to batchstart+self.batchsize'''
        A_data = []
        b_data = []
        for l in range(self.batchsize):
            '''###prepare batch by contracting current x with measurement tensors except for nth leg'''
            X = cp.deepcopy(self.x)
            B = cp.deepcopy(self.A[batchstart + l]).tolist()
            del(X[n])
            measure_vector = B[n]
            del(B[n])
            c = self.contract(X,B)
            A_data.append([measure_vector[i]*c for i in range(len(measure_vector))])
            b_data.append(self.b[batchstart + l])
        '''###solve linear regression for nth local tensor with other local tensors fixed on a measurement batch'''
        rec = LinearRegression(fit_intercept=False).fit(A_data, b_data).coef_.tolist()
        '''### update nth local tensor'''
        self.x[n] = rec
        #plt.matshow(self.x);
        #plt.colorbar()
        #plt.show()

    def step_size_criteria(self):
        if self.step <= self.minimal_step_size:
            self.term = 'The algorithm terminated, because the step size is smaller than the minimal step size '+str(self.minimal_step_size)+'. After '+str((len(str(self.l2loss))-1)*self.batchsize)+' measurements were used, the algorihm finished with an l2 loss of '+str(self.l2loss[-1])+' .'
            return True
        else:
            return False
    def l2_loss_criteria(self):
        if self.l2loss[-1] <= self.minimal_l2_loss:
            self.term = 'The algorithm terminated, because the l2 error is smaller than the minimal l2 loss '+str(self.minimal_l2_loss)+'. '+str((len(self.l2loss)-1)*self.batchsize)+' measurements were used and the algorithm terminated with an l2 error of '+str(self.l2loss[-1])+' .'
            return True
        else:
            return False
