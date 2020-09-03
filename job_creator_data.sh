counter=1
dmin=4
dmax=4
dskip=2
order_of_tensor=3


for ((legdim=dmin; legdim<=dmax; legdim+=dskip)); do
    batchsize=$((legdim**2))
    H=1
    mmin=$((batchsize*order_of_tensor*H+batchsize))
    mmax=$((order_of_tensor**legdim+batchsize))
    mskip=$((batchsize*order_of_tensor))
    echo ${legdim}
    echo ${mmin},${mmax}
    for ((meas=mmin; meas<=mmax; meas+=mskip)); do
        echo "python gen_data.py \"{'measurements': $meas, 'order': '$order_of_tensor','leg_dimension': '$legdim','file_name': 'legdim=${legdim}_meas=${meas}', 'batchsize': ${batchsize} ,'minimal_l2loss': '0.00000001', 'minimal_step_size': '0.00000001'}\"" > job_data_$counter.sh
        ((counter++))
    done
    echo 'ok'
done
