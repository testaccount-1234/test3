counter=1
dmin=4
dmax=4
dskip=2
order_of_tensor=3


for ((legdim=dmin; legdim<=dmax; legdim+=dskip)); do
    mmin=$((legdim*order_of_tensor*6))
    mmax=$((order_of_tensor**legdim))
    mskip=$((($mmax-$mmin)/2))
    echo ${legdim}
    echo ${mmin},${mmax}
    for ((meas=mmin; meas<=mmax; meas+=mskip)); do
        echo "python gen_data.py \"{'measurements': $meas, 'order': '$order_of_tensor','leg_dimension': '$legdim','file_name': 'legdim=${legdim}_meas=${meas}', 'batchsize': '$((3*${meas}*${legdim}))' ,'minimal_l2loss': '0.00000001', 'minimal_step_size': '0.00000001'}\"" > job_data_$counter.sh
        ((counter++))
    done
    echo 'ok'
done
