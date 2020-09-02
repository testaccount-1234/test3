import sys # to take parameters when calling gen_data
import ast # to evaluate parameters taken
import pickle # to load data from files
from ALS2 import *

params = {'measurements': '100', 'order': '3','leg_dimension': '3','minimal_l2loss': '0.00000001', 'minimal_step_size': '0.00000001'}
filename = 'legdim='+str(params['leg_dimension'])+'_meas='+str(params['measurements'])
params.update({'file_name': filename})
batchsize = 3*int(params['leg_dimension'])*int(params['order'])
params.update({'batchsize': batchsize})

if len(sys.argv) > 1:
	params.update(ast.literal_eval(sys.argv[1]))
	
print(params)

'''load data from pickle files'''
theta_file_name = params['file_name']+'_theta'
theta_file = open(theta_file_name,'rb')
theta = pickle.load(theta_file, encoding='latin1').tolist()

A_file_name = params['file_name']+'_A'
A_file = open(A_file_name,'rb')
A = pickle.load(A_file, encoding='latin1')

b_file_name = params['file_name']+'_b'
b_file = open(b_file_name,'rb')
b = pickle.load(b_file, encoding='latin1')

x_init_file_name = params['file_name']+'_x_init'
x_init_file = open(x_init_file_name,'rb')
x_init = pickle.load(x_init_file, encoding='latin1').tolist()


'''run ALS for every set of measurements'''
als = ALS(A,b,cp.deepcopy(x_init),batchsize=int(params['batchsize']),theta=theta)

#set stopping criteria
als.minimal_l2_loss = float(params['minimal_l2loss'])
als.minimal_step_size = float(params['minimal_step_size'])
als.batchsize = int(params['batchsize'])

# start algorithm
als.run_once()

'''save result'''
with open(params['file_name']+'_ALS_recovered_tensor_', 'wb') as fp:
	pickle.dump(als.x, fp)

with open(params['file_name']+'_ALS_l2_loss_', 'wb') as fp:
	pickle.dump(als.l2loss, fp)

with open(params['file_name']+'_ALS_term', 'wb') as fp:
	pickle.dump(als.term, fp)

with open(params['file_name']+'_ALS_fro_to_theta', 'wb') as fp:
	pickle.dump(als.fro_to_theta, fp)
	
with open(params['file_name']+'_params', 'wb') as fp:
	pickle.dump(params, fp)
