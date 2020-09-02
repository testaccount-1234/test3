import matplotlib.pyplot as plt
import pickle

def plotl2loss(legdims,measurements):
	'''plots the l2 loss of the emperiments with different numbers of available measurements and legdimesnions'''
	for j in range(len(legdims)):
		for i in range(len(measurements)):
			l2loss_file_name = 'legdim='+str(legdims[j])+'_meas='+str(measurements[i])+'_ALS_l2_loss'
			l2loss_file = open(l2loss_file_name,'rb')
			l2loss = pickle.load(l2loss_file, encoding='latin1')
			print(l2loss)
			X = range(len(l2loss))
			plt.plot(l2loss,X)
	plt.savefig('legdims='+str(legdims)+'_meas='+str(measurements)+'ALS_l2_loss_plot')
	plt.close()

def plotfroloss(legdims, measurements):
	'''plots the l2 loss of the emperiments with different numbers of available measurements and legdimesnions'''
	for j in range(len(legdims)):
		for i in range(len(measurements)):
			froloss_file_name = 'legdim='+str(legdims[j])+'_meas='+str(measurements[i])+'_fro_to_theta'
			froloss_file = open(froloss_file_name,'rb')
			froloss = pickle.load(froloss_file, encoding='latin1')
			print(froloss)
			X = range(len(froloss))
			plt.plot(froloss,X)
	plt.savefig('legdims='+str(legdims)+'_meas='+str(measurements)+'ALS_fro_to_theta_plot')
	plt.close()
