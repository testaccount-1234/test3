import sys # to take parameters when calling gen_data
import ast # to evaluate parameters taken
import numpy as np
import pickle # to save the data 

params = {'measurements': 90, 'order': '3','leg_dimension': '5','file_name': './data/legdim=5_meas=90', 'batchsize': '1350' ,'minimal_l2loss': '0.00000001', 'minimal_step_size': '0.00000001'}
if len(sys.argv) > 1:
	params.update(ast.literal_eval(sys.argv[1]))

theta = np.random.uniform(0,1,(int(params['order']),int(params['leg_dimension'])))
with open(params['file_name']+'_theta','wb') as fp:
	pickle.dump(theta, fp)

A = [np.random.uniform(0,1,(int(params['order']),int(params['leg_dimension']))) for i in range(int(params['measurements']))]
with open(params['file_name']+'_A','wb') as fp:
	pickle.dump(A, fp)
	
b = [np.prod([np.dot(A[i][j],theta[j]) for j in range(int(params['order']))]) for i in range(int(params['measurements']))]
with open(params['file_name']+'_b','wb') as fp:
	pickle.dump(b, fp)

x_init = np.random.uniform(0,1,(int(params['order']),int(params['leg_dimension'])))
with open(params['file_name']+'_x_init','wb') as fp:
	pickle.dump(x_init, fp)
