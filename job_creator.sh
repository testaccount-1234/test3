counter=1
dmin=3
dmax=5
dskip=2
order_of_tensor=3


for ((legdim=dmin; legdim<=dmax; legdim+=dskip)); do
    mmin=$((legdim*order_of_tensor*6))
    mmax=$((order_of_tensor**legdim))
    mskip=$((($mmax-$mmin)/10))
    for ((meas=mmin; meas<=mmax; meas+=mskip)); do
        echo "python recover_theta.py \"{'measurements': $meas, 'order': '$order_of_tensor','leg_dimension': '$legdim','file_name': './data/legdim=${legdim}_meas=${meas}', 'batchsize': '$((3*${order_of_tensor}*${legdim}))' ,'minimal_l2loss': '0.00000001', 'minimal_step_size': '0.00000001'}\"" > job_rec_$counter.sh
        ((counter++))
    done
done

